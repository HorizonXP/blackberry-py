#ifndef APP_H
#define APP_H

#include <QObject>
#include <QString>

#include <bb/cascades/Application>
#include <bb/system/LocaleHandler>
#include <bb/system/InvokeManager>
#include <bb/system/InvokeRequest>
#include <bb/cascades/InvokeQuery>

#include "tart.hpp"


/*!
 * @brief Application GUI object
 */
class App : public QObject
{
    Q_OBJECT
public:
    App(bb::cascades::Application * app, Tart * tart, QString qmlpath);

    // This wasn't here before Gold SDK but the new Momentics project template
    // puts it in, so here it is for now.  Do we need it?  Something else?
    virtual ~App() {}

    Q_INVOKABLE QString getLocaleInfo(const QString & name);
    Q_INVOKABLE int displayAspectType();
    Q_INVOKABLE void composeEmail(bb::cascades::InvokeQuery * query);

signals:
    void pushReceived(const QString & id, const QByteArray & bytes, bool wantsAck);

private slots:
    void onInvoked(const bb::system::InvokeRequest &request);

private:
    bb::system::LocaleHandler * localeHandler;
    bb::system::InvokeManager * m_invokeManager;
};

#endif // ifndef APP_H
