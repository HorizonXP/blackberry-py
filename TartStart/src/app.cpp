#include "app.hpp"
#include "tart.hpp"

#include <bb/cascades/Application>
#include <bb/cascades/QmlDocument>
#include <bb/cascades/AbstractPane>

#include <bb/cascades/pickers/ContactPicker>

#include <bb/cascades/pickers/FilePicker>
#include <bb/cascades/pickers/FilePickerMode>
#include <bb/cascades/pickers/FilePickerSortFlag>
#include <bb/cascades/pickers/FilePickerSortOrder>
#include <bb/cascades/pickers/FileType>
#include <bb/cascades/pickers/FilePickerViewMode>
#include <bb/cascades/advertisement/Banner>

#include <bb/cascades/SceneCover>
#include <bb/cascades/AbstractCover>
#include <bb/cascades/ActiveTextHandler>
#include <bb/platform/HomeScreen>
#include <bb/data/DataSource>
#include <bb/device/DisplayInfo>
#include <bb/device/DisplayAspectType>
#include <bb/system/LocaleType>

#include <bb/platform/Notification>
#include <bb/platform/NotificationDialog>
#include <bb/platform/NotificationError>
#include <bb/platform/NotificationResult>

#include <bb/system/ApplicationStartupMode>

#include <bb/network/PushPayload>

#include <bb/system/InvokeManager>
#include <bb/system/InvokeRequest>

#include <QString>
#include <QTimer>
#include <QLocale>
#include <QDebug>

using namespace bb::cascades;

//---------------------------------------------------------
// Set up a general-purpose object to hold stuff for the
// Cascades Application. Since we plan to implement all
// app-specific "backend" or business logic in Python, this
// object has a much lesser purpose than the equivalent in
// pure C++ Cascades apps, but for now we're keeping it here
// anyway.  It installs several names in the QML context,
// registers a bunch of types that aren't provided there by
// default, and does the usual QML-root object setup.
// Ideas for doing this differently are welcome.  It could
// probably be flipped around and done with calls from
// Python, maybe pushing all of these pieces into library
// routines that Tart makes available as separate packages,
// with the advantage that it wouldn't be so monolithic either.
//
App::App(Application * app, Tart * tart, QString qmlpath)
: QObject(app)
, localeHandler(NULL)
, m_invokeManager(new bb::system::InvokeManager(this))
{
    bool ok;
    Q_UNUSED(ok);

    ok = connect(m_invokeManager, SIGNAL(invoked(const bb::system::InvokeRequest&)),
        this, SLOT(onInvoked(const bb::system::InvokeRequest&)));
    Q_ASSERT(ok);

    bb::system::ApplicationStartupMode::Type mode = m_invokeManager->startupMode();
    // LaunchApplication = 0
    // InvokeApplication = 1
    // InvokeCard = 3
    qDebug() << "startupMode" << mode;

    ok = connect(this,
        SIGNAL(pushReceived(const QString &, const QByteArray &, bool)),
        tart,
        SLOT(pushReceived(const QString &, const QByteArray &, bool))
        );
    Q_ASSERT(ok);

    // Register the DataSource class as a QML type so that it's accessible in QML
    bb::data::DataSource::registerQmlTypes();

    // register lots of stuff that at least prior to beta 4 wasn't done for us
    // TODO: check this again now that Gold SDK is out
    qmlRegisterType<SceneCover>("bb.cascades", 1, 0, "SceneCover");
    qmlRegisterUncreatableType<AbstractCover>("bb.cascades", 1, 0, "AbstractCover", "");
    qmlRegisterType<bb::platform::HomeScreen>("bb.platform", 1, 0, "HomeScreen");
    qmlRegisterType<QTimer>("bb.cascades", 1, 0, "QTimer");
    qmlRegisterType<ActiveTextHandler>("bb.cascades", 1, 0, "ActiveTextHandler");
    qmlRegisterType<bb::device::DisplayInfo>("bb.device", 1, 0, "DisplayInfo");
    qRegisterMetaType<bb::device::DisplayAspectType::Type>("bb::device::DisplayAspectType::Type");
    // qmlRegisterUncreatableType<bb::device::DisplayAspectType>("bb.device", 1, 0, "DisplayAspectType", "");

    qmlRegisterType<advertisement::Banner>("bb.cascades.advertisement", 1, 0, "Banner");

    qmlRegisterType<bb::platform::Notification>("bb.platform", 1, 0, "Notification");
    qmlRegisterType<bb::platform::NotificationDialog>("bb.platform", 1, 0, "NotificationDialog");
    qmlRegisterUncreatableType<bb::platform::NotificationError>("bb.platform", 1, 0, "NotificationError", "");
    qmlRegisterUncreatableType<bb::platform::NotificationResult>("bb.platform", 1, 0, "NotificationResult", "");

    qmlRegisterType<bb::cascades::InvokeQuery>("bb.cascades", 1, 0, "InvokeQuery");

    // create scene document from main.qml asset
    // set parent to created document to ensure it exists for the whole application lifetime
	QmlDocument *qml = QmlDocument::create(qmlpath).parent(this);

    //-- setContextProperty expose C++ object in QML as an variable
    qml->setContextProperty("app", this);
    if (tart)
    	qml->setContextProperty("_tart", tart);

    // create root object for the UI
    AbstractPane *root = qml->createRootObject<AbstractPane>();

    // set created root object as a scene
    app->setScene(root);
}


//---------------------------------------------------------
// A presumably provisional way to get at this info, until we find
// a better API for it.  Can be called from JavaScript as
// app.getLocaleInfo(somestring) to retrieve various bits as required.
//
QString App::getLocaleInfo(const QString & name) {
	if (!localeHandler)
		localeHandler = new bb::system::LocaleHandler(bb::system::LocaleType::Region, this);

	QLocale locale = localeHandler->locale();
	if (name == "currencySymbol")
		return locale.currencySymbol(QLocale::CurrencySymbol);
	else
	if (name == "currencyCode")
		return locale.currencySymbol(QLocale::CurrencyIsoCode);
	else
	if (name == "currencyName")
		return locale.currencySymbol(QLocale::CurrencyDisplayName);
	else
	if (name == "country")
		return QLocale::countryToString(locale.country());
	else
	if (name == "name")
		return locale.name();
	else
	if (name == "measurementSystem") {
		return QString(localeHandler->measurementSystem() ? "imperial" : "metric");
	}
	else
		return QString("?");
}


int App::displayAspectType() {
    bb::device::DisplayInfo displayInfo;

    return (int) displayInfo.aspectType();
}


//---------------------------------------------------------
// Another provisional routine. This one allows creating an
// InvokeQuery in QML, populating it with the required properties,
// and sending via app.composeEmail(queryId) to have the Composer
// brought up with prepopulated fields including attachments.
// See SendEmail sample.
//
void App::composeEmail(bb::cascades::InvokeQuery * query) {
    bb::system::InvokeRequest request;
    request.setAction(query->invokeActionId());
    request.setMimeType(query->mimeType());

    // See http://supportforums.blackberry.com/t5/Cascades-Development/Invoke-Email-with-Attachment/m-p/2251453#M17589
    // for the source of this particular magic, and note that even the trailing
    // newline is required or this won't work.
    request.setData("data:json:" + query->data() + "\n");
    // qDebug() << "PPS data" << request.data();

    m_invokeManager->invoke(request);
}


//---------------------------------------------------------
// This one for now handles just invocation via bb.action.PUSH, and
// dispatches the payload to Python via Tart's pushReceived() slot.
//
void App::onInvoked(const bb::system::InvokeRequest &request)
{
    // qDebug() << "request" << request.action();
    // qDebug() << "metadata" << request.metadata();
    // qDebug() << "mimeType" << request.mimeType();
    // qDebug() << "fileTransferMode" << request.fileTransferMode();
    // // qDebug() << "listId" << request.listId(); 10.2 only
    // qDebug() << "perimeter" << request.perimeter();
    // qDebug() << "target" << request.target();
    // qDebug() << "source" << request.source().groupId() << request.source().installId();
    // qDebug() << "targetTypes" << (int) request.targetTypes();
    // qDebug() << "uri" << request.uri();
    // qDebug() << "data" << request.data();
    // request "bb.action.PUSH"
    // metadata QMap()
    // mimeType "application/vnd.push"
    // fileTransferMode 0
    // perimeter 2
    // target "com.whatever.YourApp"
    // source 361 "sys.service.internal.361"
    // targetTypes 0
    // uri  QUrl( "" )
    // data "pushData:json:{"pushId":"<app id here>","pushDataLen":22,
    //      "appLevelAck":0,"httpHeaders":{"OST / HTTP/1.1":"POST / HTTP/1.1",
    //          "Content-Type":"text/plain","Connection":"close",
    //          "X-RIM-PUSH-SERVICE-ID":"<app id here>",
    //          "x-rim-deviceid":"<PIN here>","Content-Length":"22"}}

    if (request.action().compare(BB_PUSH_INVOCATION_ACTION) == 0) {
        // Received an incoming push
        // Extract it from the invoke request and then process it
        bb::network::PushPayload payload(request);
        if (payload.isValid()) {
            qDebug() << "payload:" << payload.id() << "headers:" << payload.headers();
            // qDebug() << "data:" << payload.data();
            emit pushReceived(payload.id(), payload.data(), payload.isAckRequired());
        } else {
            // Should we be checking isAckRequired() here, and rejectPush()?
            // Not sure the docs are clear on how isValid() relates to those.
            // Could also pass isValid() down to Python to take into account.
            qDebug() << "invalid payload!";
        }
    }
}
