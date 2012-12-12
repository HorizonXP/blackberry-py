/*
 * tart.hpp
 *
 *  Created on: 2012-09-16
 *      Author: phansen
 */

#ifndef TART_HPP_
#define TART_HPP_

#include <QObject>
#include <QQueue>
#include <QVariant>
#include <QThread>
#include <QWaitCondition>
#include <QMutex>


//---------------------------------------------------------
// Thread-safe queue to hold messages sent from anywhere in
// the Application to the Python interpreter, where they'll
// be picked up via the tart.wait() call in the Tart event loop.
//
class TartQueue : public QObject
{
	Q_OBJECT

public:
	TartQueue() {}

    QString get();

public slots:
    void push(QString msg);

private:
    QQueue<QString> m_queue;
    QMutex			m_qmutex;

    QWaitCondition 	m_condition;
    QMutex			m_mutex;
};


//---------------------------------------------------------
// Secondary thread used to run the Python interpreter,
// which can itself start any number of tertiary threads as required.
//
class TartThread : public QThread
{
    Q_OBJECT
public:
    void run();
};


//---------------------------------------------------------
// Main object that implements the mechanisms provided by
// Tart to allow a Cascades app to instantiate a Python interpreter
// and communicate asynchronously with it.  Provides additional
// supporting routines as required.
//
class Tart : public QObject
{
    Q_OBJECT

private:
	static Tart * sm_instance;

public:
    static Tart * instance() { return sm_instance; }

    Tart(int argc, char ** argv);
//    ~Tart();

    const char * getScriptPath() { return (m_argc && m_argv) ? m_argv[m_argc - 1] : NULL; }

	void start();
	TartThread * getThread() { return m_thread; }
    TartQueue * getQueue() { return m_queue; }
	bool isTerminating() { return m_terminating; }

    Q_INVOKABLE QString writeImage(const QString & name, const QString & data);

public slots:
	void postMessage(QString msg);
	void yieldMessage(QString msg);
	void cleanup();

signals:
    void messageYielded(QString msg);
	void pythonTerminated(QString msg);

private:
    // storage for argument list converted from multibyte to Unicode
    //    wchar_t ** m_wargv;
    //    int m_wargc;
	TartThread *    m_thread;
	TartQueue *     m_queue;
    bool            m_terminating;
    int				m_argc;
    char ** 		m_argv;
};


#endif /* TART_HPP_ */
