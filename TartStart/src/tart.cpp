/*
 * tart.cpp
 *
 *  Created on: 2012-09-16
 *      Author: phansen
 */

#include <assert.h>
#include <stdio.h>
#include <iconv.h>

#include <Python.h>

#include "tart.hpp"

#include <QObject>
#include <QDebug>
#include <QDir>
#include <QFile>
#include <QByteArray>
#include <QQueue>
#include <QMutex>


//---------------------------------------------------------
// Put a new message string (meant to be JSON-encoded data)
// on a queue for the Tart event loop in Python to retrieve
// using tart_wait().  This must be done in a threadsafe manner.
//
void TartQueue::push(QString msg) {
	// qDebug() << QThread::currentThreadId() << "TartQueue push" << msg;
	m_qmutex.lock();
	m_queue.enqueue(msg);
	m_qmutex.unlock();
	// qDebug() << "queue size" << m_queue.size();
	m_condition.wakeAll();
	// qDebug() << "wakeAll";
}


//---------------------------------------------------------
// Retrieve messages placed on the queue by push(), in a threadsafe
// manner.  Called from tart_wait() in the Python main thread event loop.
//
QString TartQueue::get() {
	// qDebug() << QThread::currentThreadId() << "TartQueue get" << m_queue.size();

	while (!m_queue.size()) {
		// qDebug() << QThread::currentThreadId() << "blocking";
		m_mutex.lock();
		m_condition.wait(&m_mutex);
		m_mutex.unlock();
		// qDebug() << QThread::currentThreadId() << "awake!";
	}

	// qDebug() << "mutex lock";
	m_qmutex.lock();
	// qDebug() << "mutex locked";
	QString msg = m_queue.dequeue();
	m_qmutex.unlock();
	// qDebug() << "mutex unlocked";
    // qDebug() << "dequeued" << msg;

	return msg;
}




//---------------------------------------------------------
// Launch a Python interpreter, with control passed to it until it
// returns during app termination.  This routine is called in a
// separate thread created by Tart::start().
//
// TODO: sort out the shutdown, as for some reason we don't always seem
// to be returning properly from the PyRun_...() routine.
// Maybe it catches and handles SystemExit or other exceptions, and kills
// the whole process?  Investigation is needed.
//
void TartThread::run() {
	qDebug() << QThread::currentThreadId() << "Tart thread running";

	int rc = -1;

	const char * path = Tart::instance()->getScriptPath();
    qDebug() << "script path" << path;
	if (path) {
		FILE * mainfile = fopen(path, "r");

		if (mainfile) {
			// We use the SimpleFileExFlags version so that we can pass closeit=1
			// (second argument) and to set flags to non-NULL so that the
			// code can specify "from __future__ import" if required.
			PyCompilerFlags flags;
			rc = PyRun_SimpleFileExFlags(mainfile, path, 1, &flags);

			qDebug() << "script finished with rc" << rc;
			PyObject * error = PyErr_Occurred();
			if (error && !PyErr_GivenExceptionMatches(error, PyExc_SystemExit)) {
				qDebug() << "PyRun_SimpleFile() of blackberry_tart.py:" << rc;
				PyErr_Print();
			} else if (error) {
				PyErr_Print();
			}

			PyErr_Clear();
		}
		else {
			qDebug() << path << "is missing!\n";
		}
	} else
		qDebug() << "no Python script specified\n";

	qDebug("Tart thread terminating");
}


//---------------------------------------------------------
// Implement asynchronous sending of messages from the Python
// side (any thread) to the main Application via the yieldMessage signal.
// The message data is expected to be JSON-encoded, but that's
// merely a convention shared between Python and JavaScript.
//
static PyObject *
tart_send(PyObject *self, PyObject *args)
{
	char * msg;

    if(!PyArg_ParseTuple(args, "s:send", &msg))
        return NULL;

    // qDebug() << QThread::currentThreadId() << "tart_send" << msg;

    // TODO: sort out more carefully whether the QueuedConnection is required,
    // or whether there are simpler/faster/whatever alternatives.
    //    Tart::instance()->yieldMessage(msg);
    QMetaObject::invokeMethod(Tart::instance(), "yieldMessage",
        Qt::QueuedConnection, Q_ARG(QString, msg));

    return PyLong_FromLong(0);
}


//---------------------------------------------------------
// Blocking call for the Python main thread's Tart event loop
// where it should wait for incoming "events" from elsewhere
// (generally from the QML side).
// TODO: implement a timeout, and timer-support
//
static PyObject *
tart_wait(PyObject *self, PyObject *args)
{
    if(!PyArg_ParseTuple(args, ":wait"))
        return NULL;

    // qDebug() << QThread::currentThreadId() << "tart_wait";

    QString msg;

    // may block indefinitely, so we have to release the interpreter
    // to let other Python threads run until data arrives for us
    Py_BEGIN_ALLOW_THREADS
    msg = Tart::instance()->getQueue()->get();
    Py_END_ALLOW_THREADS

    // The null msg is part of the our shutdown processing, where
    // Tart::cleanup() will set the termination flag, and then "kick"
    // us awake by sending a null message, in case we're not already
    // processing other messages. To ensure prior messages are processed,
    // we only check for the termination flag when we've got a null
    // message, since otherwise termination would be "out of band" and
    // we might exit unexpectedly early.
    if (msg.isNull())
        qDebug() << "msg is null";

    if (Tart::instance()->isTerminating())
        qDebug() << "Tart is terminating...";

    // Flag indicates Python should terminate, but we check for the
    // terminating flag only when we see the null string, so we
    // will consume earlier messages before exiting.
    if (msg.isNull() && Tart::instance()->isTerminating()) {
        qDebug() << "raising SystemExit";
    	PyErr_SetString(PyExc_SystemExit, "Tart exiting");
    	return NULL;
    }
    else {
        // qDebug() << "tart_wait got" << msg;

        QByteArray bytes = msg.toUtf8();
        // qDebug() << "tart_wait bytes" << bytes.size();
        PyObject * result = Py_BuildValue("s#", bytes.constData(), bytes.size());
        // qDebug() << "tart_wait built" << result;

        return result;
    }
}


//---------------------------------------------------------
// Define callables for the "_tart" builtin module in Python.
//
static PyMethodDef TartMethods[] = {
    {"send", tart_send, METH_VARARGS, "Send msg/results to QML."},
    {"wait", tart_wait, METH_VARARGS, "Wait for events from QML."},
    {NULL, NULL, 0, NULL}
};

//---------------------------------------------------------
// Define the "_tart" builtin module for Python code to use.
//
static PyModuleDef TartModule = {
    PyModuleDef_HEAD_INIT, "_tart", NULL, -1, TartMethods,
    NULL, NULL, NULL, NULL
};

//---------------------------------------------------------
// More boilerplate code to set up builtin module.
//
static PyObject*
PyInit_tart(void)
{
    return PyModule_Create(&TartModule);
}


//---------------------------------------------------------
// Singleton, so we can "find" Tart globally when required.
//
Tart * Tart::sm_instance;


//---------------------------------------------------------
// Construct the Tart object. This should be called from the
// main C++ code, probably after the Application is constructed.
// It prepares but does not yet launch the Python interpreter,
// as that has to be done in a separate thread.
// For now we do nothing with the arguments, but may want to
// extract useful info from them later.
//
Tart::Tart(int argc, char ** argv) {
	if (sm_instance)
		throw "Singleton already exists";

	sm_instance = this;

    // We may want to do stuff with these later... used to pass it
    // to the Python interpreter when it was the primary thing, but
    // now the Cascades Application gets it and maybe we don't care.
	m_argc = argc;
	m_argv = argv;

	m_queue = new TartQueue();
	m_thread = NULL;

    m_terminating = false;

	PyImport_AppendInittab(TartModule.m_name, &PyInit_tart);

	// only Py_SetProgramName and Py_SetPath may come before this
	Py_Initialize();

	qDebug("Python initialized");

	//    m_wargv = args_to_wargv(args.size(), argv);
	//    m_wargc = argc;
	//    PySys_SetArgvEx(argc, m_wargv, 0);

	qDebug() << QThread::currentThreadId() << "Tart initialized";
}


//---------------------------------------------------------
// Shut down Tart, requesting and waiting for termination of the
// Python interpreter thread, and cleaning up.
// It may be best if this call comes via a connection to the
// Application::aboutToQuit() signal.
//
void Tart::cleanup() {
	qDebug() << QThread::currentThreadId() << "Tart cleanup";

    // Flag indicates Python should terminate, but we need to send
    // a message to unblock. The tart.wait() call checks for the
    // terminating flag only when it sees the null string, so it
    // will consume earlier messages before exiting.
    m_terminating = true;
	m_queue->push(QString());  // send null string to unblock

	if (m_thread) {
		qDebug() << "thread wait";
		m_thread->wait();
		qDebug() << "thread wait done";
		m_thread = NULL;
	}

	// will block until any non-daemon threads terminate
    // TODO: sort out the shutdown sequence since for now this fails
	// qDebug() << "Python finalizing";
	// Py_Finalize();
	// qDebug() << "Python finalized";

//	free_wargv(m_wargc, m_wargv);

	delete m_queue;
	m_queue = NULL;

	sm_instance = NULL;
	qDebug() << "Tart destroyed";

	return;
}


//---------------------------------------------------------
// Launch the secondary thread in which the Python interpreter
// is executed, since this call comes from the main Application thread.
//
void Tart::start() {
	if (m_thread)
		return;

    qDebug() << "starting Tart in thread";
    m_thread = new TartThread();

    m_queue->moveToThread(m_thread);
    m_thread->start();
    qDebug() << "Tart thread started";
}


//---------------------------------------------------------
// Signal that a message has been sent from the Python side,
// currently implemented using a handler for this signal in the
// tart.js JavaScript code that's used in the QML.
//
void Tart::yieldMessage(QString msg) {
	// qDebug() << QThread::currentThreadId() << "Tart yieldMessage" << msg;
	emit messageYielded(msg);
}


//---------------------------------------------------------
// Pass messages into the Python interpreter main thread,
// which is expected to implement an event loop around calls
// to tart_wait() to retrieve these messages.
//
void Tart::postMessage(QString msg) {
	// qDebug() << QThread::currentThreadId() << "Tart postMessage" << msg;
	m_queue->push(msg);
	// qDebug() << "Tart postMessage done";
//	QMetaObject::invokeMethod(m_queue, "push", Qt::QueuedConnection, Q_ARG(QString, msg));
}


//---------------------------------------------------------
// Experimental utility routine to write image data to a file.
// This is intended to work with data retrieved from an HTML
// canvas running in a WebView, where canvas.toDataURL() retrieves
// the raw PNG data, so we can ultimately put this into an ImageView.
// Clearly there are numerous more direct and simpler paths possible.
//
QString Tart::writeImage(const QString & name, const QString & data)
{
	// qDebug() << "writeImage" << name;
	QString dataFolder = QDir::homePath();
	QFile file(dataFolder + '/' + name);
	// qDebug() << "path" << file.fileName();
	if (file.open(QIODevice::WriteOnly | QIODevice::Truncate)) {
		file.write(QByteArray::fromBase64(data.toAscii()));
		file.close();
		return file.fileName();
	}
	else
		return QString();
}


// EOF
