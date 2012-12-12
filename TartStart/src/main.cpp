#include <bb/cascades/Application>

#include <QLocale>
#include <Qt>
#include <QTranslator>
#include <QMetaObject>
#include <QDebug>
#include <Qt/qdeclarativedebug.h>

#include "app.hpp"
#include "tart.hpp"


using namespace bb::cascades;

Q_DECL_EXPORT
int main(int argc, char **argv)
{
    //-- this is where the server is started etc
    Application app(argc, argv);

    //-- localization support
    // QTranslator translator;
    // QString locale_string = QLocale().name();
    // QString filename = QString( "TartStart_%1" ).arg( locale_string );
    // if (translator.load(filename, "app/native/qm")) {
    //     app.installTranslator( &translator );
    // }

    Tart tart(argc, argv);
    tart.start();
    QObject::connect(&app, SIGNAL(aboutToQuit()), &tart, SLOT(cleanup()));

    // tart.postMessage("Foo bar");

    // TODO: learn the final state of things with Gold SDK, where there are
    // major changes in how asset: and file: are handled with QML and
    // related stuff.  For now, leaving this as it is here: asset:///main.qml
    // by default but whatever you pass on the command line otherwise.
    QString qmlpath = "asset:///main.qml";
    int i;
    for (i = 0; i < argc; i++) {
    	// qDebug() << "arg" << i << "is" << argv[i];
    	if (!strcmp("-qml", argv[i]) && (i < argc - 1)) {
    		qmlpath = argv[i + 1];
    		break;
    	}
    }
    qDebug() << "qmlpath" << qmlpath;

    // Prior to Gold SDK this was allocated on the stack, but for some
    // unexplained reason they changed the template so it's heap-allocated
    // now, which begs the question... how does the cleanup work, what
    // was wrong with it before, and is there anything wrong with it now?
    new App(&app, &tart, qmlpath);

    //-- we complete the transaction started in the app constructor and start
    // the client event loop here
    int rc = Application::exec();
    //-- when loop is exited the Application deletes the scene which deletes all
    // its children (per qt rules for children)
    qDebug() << "exec() returned" << rc;

    return rc;
}
