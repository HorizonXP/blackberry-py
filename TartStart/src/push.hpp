#ifndef PUSH_H
#define PUSH_H

#include <QObject>
#include <QString>

#include <bb/network/PushService>
#include <bb/network/PushStatus>
#include <bb/network/PushCommand>
#include <bb/network/PushErrorCode>


// initialize the push extension module so we can "import _push"
void init_push(void);

using namespace bb::network;

class PushHandler : public QObject
{
    Q_OBJECT
public:
    PushHandler(PushService * pushService);

    // This wasn't here before Gold SDK but the new Momentics project template
    // puts it in, so here it is for now.  Do we need it?  Something else?
    virtual ~PushHandler() {}

private slots:
    void onCreateSessionCompleted(const bb::network::PushStatus &status);
    void onCreateChannelCompleted(const bb::network::PushStatus &status, const QString &token);
    void onDestroyChannelCompleted(const bb::network::PushStatus &status);
    void onRegisterToLaunchCompleted(const bb::network::PushStatus &status);
    void onUnregisterFromLaunchCompleted(const bb::network::PushStatus &status);
    void onSimChanged();
    void onPushTransportReady(bb::network::PushCommand::Type command);

private:
    PushService *   m_pushService;
};

#endif // ifndef PUSH_H

