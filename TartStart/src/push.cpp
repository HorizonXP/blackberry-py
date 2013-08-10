/*
 * push.cpp
 *
 *  Created on: 2013-08-09
 *      Author: phansen
 */

#include <assert.h>
#include <stdio.h>
#include <iconv.h>
#include <time.h>

#include <Python.h>

#include <QObject>
#include <QDebug>
#include <QByteArray>

#include "push.hpp"


static struct {
    PushService *   service;
    PushHandler *   handler;

    PyObject *      dispatcher;
}   _push;


//---------------------------------------------------------
// Initialize the PushService.
//
static PyObject *
push_initialize(PyObject * self, PyObject * args)
{
    Q_UNUSED(self);
    char * appId;
    char * invokeId;
    PyObject * dispatcher;

    if(!PyArg_ParseTuple(args, "ssO:initialize", &appId, &invokeId, &dispatcher))
        return NULL;
    Py_XINCREF(dispatcher);  // because we'll keep it

    PyObject * dispatcher_repr = PyObject_Repr(dispatcher);
    PyObject * dispatcher_bytes = PyUnicode_AsASCIIString(dispatcher_repr);
    Py_XDECREF(dispatcher_repr);

    qDebug() << QThread::currentThreadId() << "push_initialize" << appId << invokeId << PyBytes_AsString(dispatcher_bytes);
    Py_XDECREF(dispatcher_bytes);

    _push.service = new PushService(QString::fromUtf8(appId), QString::fromUtf8(invokeId));
    _push.handler = new PushHandler(_push.service);
    _push.dispatcher = dispatcher;

    Py_RETURN_NONE;
}


//---------------------------------------------------------
// Create a session.
//
static PyObject *
push_createSession(PyObject *self, PyObject *args)
{
    Q_UNUSED(self);

    if(!PyArg_ParseTuple(args, ":createSession"))
        return NULL;

    qDebug() << QThread::currentThreadId() << "push_createSession";

    _push.service->createSession();

    Py_RETURN_NONE;
}


//---------------------------------------------------------
// Create a channel.
//
static PyObject *
push_createChannel(PyObject *self, PyObject *args)
{
    Q_UNUSED(self);
    char * ppg_url;

    if(!PyArg_ParseTuple(args, "s:createChannel", &ppg_url))
        return NULL;

    qDebug() << QThread::currentThreadId() << "push_createChannel" << ppg_url;

    _push.service->createChannel(QUrl(QString::fromUtf8(ppg_url)));

    Py_RETURN_NONE;
}


//---------------------------------------------------------
// Register to launch app via invocation when push received.
//
static PyObject *
push_registerToLaunch(PyObject *self, PyObject *args)
{
    Q_UNUSED(self);

    if(!PyArg_ParseTuple(args, ":registerToLaunch"))
        return NULL;

    qDebug() << QThread::currentThreadId() << "push_registerToLaunch";

    _push.service->registerToLaunch();

    Py_RETURN_NONE;
}


//---------------------------------------------------------
// Unregister from launch app via invocation when push received.
//
static PyObject *
push_unregisterFromLaunch(PyObject *self, PyObject *args)
{
    Q_UNUSED(self);

    if(!PyArg_ParseTuple(args, ":unregisterFromLaunch"))
        return NULL;

    qDebug() << QThread::currentThreadId() << "push_unregisterFromLaunch";

    _push.service->unregisterFromLaunch();

    Py_RETURN_NONE;
}


//---------------------------------------------------------
// Accept a push payload.
//
static PyObject *
push_acceptPush(PyObject *self, PyObject *args)
{
    Q_UNUSED(self);
    char * id;  // will be UTF-8 if input is a string, else bytes

    if(!PyArg_ParseTuple(args, "s:acceptPush", &id))
        return NULL;

    qDebug() << QThread::currentThreadId() << "push_acceptPush" << id;

    _push.service->acceptPush(QString::fromUtf8(id));

    Py_RETURN_NONE;
}


//---------------------------------------------------------
// Reject a push payload.
//
static PyObject *
push_rejectPush(PyObject *self, PyObject *args)
{
    Q_UNUSED(self);
    char * id;

    if(!PyArg_ParseTuple(args, "s:rejectPush", &id))
        return NULL;

    qDebug() << QThread::currentThreadId() << "push_rejectPush" << id;

    _push.service->rejectPush(QString::fromUtf8(id));

    Py_RETURN_NONE;
}


//---------------------------------------------------------
// processing and cleanup after a dispatch call, to reduce duplicate code
//
static void _dispatched(PyGILState_STATE & gil_state, PyObject * result)
{
    // TODO handle exceptions from the call, either by exiting the event
    // loop (maybe only during development?) or by dumping a traceback,
    // setting a flag, and continuing on.
    bool is_SystemExit = false;

    if (result == NULL) {   // exception during call
        // see http://computer-programming-forum.com/56-python/a81eae52ca74e6c1.htm
        // Calling PyErr_Print() will actually terminate the process if
        // SystemExit is the exception!
        if (PyErr_ExceptionMatches(PyExc_SystemExit))
            is_SystemExit = true;
        else
            PyErr_Print();
    }
    else
        Py_DECREF(result);

    PyGILState_Release(gil_state);

    if (is_SystemExit)
        {
        qDebug() << QThread::currentThreadId() << "_push: SystemExit";
        QThread::currentThread()->exit(4);
        }

    return;
}


//---------------------------------------------------------
// Define callables for the "_tart" builtin module in Python.
//
static PyMethodDef PushMethods[] = {
    {"initialize", push_initialize,  METH_VARARGS,
        PyDoc_STR("initialize(obj)")},
    {"createSession", push_createSession, METH_VARARGS,
        PyDoc_STR("PushService.createSession()")},
    {"createChannel", push_createChannel, METH_VARARGS,
        PyDoc_STR("PushService.createChannel(ppg_url='')")},
    {"registerToLaunch", push_registerToLaunch, METH_VARARGS,
        PyDoc_STR("PushService.registerToLaunch()")},
    {"unregisterFromLaunch",  push_unregisterFromLaunch, METH_VARARGS,
        PyDoc_STR("PushService.unregisterFromLaunch()")},
    {"acceptPush",  push_acceptPush, METH_VARARGS,
        PyDoc_STR("PushService.acceptPush(payload_id)")},
    {"rejectPush",  push_rejectPush, METH_VARARGS,
        PyDoc_STR("PushService.rejectPush(payload_id)")},
    {NULL, NULL, 0, NULL}
};


//---------------------------------------------------------
// Define the "_tart" builtin module for Python code to use.
//
static PyModuleDef PushModule = {
    PyModuleDef_HEAD_INIT, "_push", NULL, -1, PushMethods,
    NULL, NULL, NULL, NULL
};


//---------------------------------------------------------
// More boilerplate code to set up builtin module.
//
PyMODINIT_FUNC
PyInit_push(void)
{
    return PyModule_Create(&PushModule);
}

void init_push(void) {
    PyImport_AppendInittab(PushModule.m_name, &PyInit_push);
}


PushHandler::PushHandler(PushService * pushService)
: m_pushService(pushService)
{
    bool ok;
    Q_UNUSED(ok);

    // Connect the signals
    ok = connect(m_pushService, SIGNAL(createSessionCompleted(const bb::network::PushStatus&)),
        this, SLOT(onCreateSessionCompleted(const bb::network::PushStatus&)));
    Q_ASSERT(ok);
    ok = connect(m_pushService, SIGNAL(createChannelCompleted(const bb::network::PushStatus&, const QString)),
        this, SLOT(onCreateChannelCompleted(const bb::network::PushStatus&, const QString)));
    Q_ASSERT(ok);
    ok = connect(m_pushService, SIGNAL(destroyChannelCompleted(const bb::network::PushStatus&)),
        this, SLOT(onDestroyChannelCompleted(const bb::network::PushStatus&)));
    Q_ASSERT(ok);
    ok = connect(m_pushService, SIGNAL(registerToLaunchCompleted(const bb::network::PushStatus&)),
        this, SLOT(onRegisterToLaunchCompleted(const bb::network::PushStatus&)));
    Q_ASSERT(ok);
    ok = connect(m_pushService, SIGNAL(unregisterFromLaunchCompleted(const bb::network::PushStatus&)),
        this, SLOT(onUnregisterFromLaunchCompleted(const bb::network::PushStatus&)));
    Q_ASSERT(ok);
    ok = connect(m_pushService, SIGNAL(simChanged()),
        this, SLOT(onSimChanged()));
    Q_ASSERT(ok);
    ok = connect(m_pushService, SIGNAL(pushTransportReady(bb::network::PushCommand::Type)),
        this, SLOT(onPushTransportReady(bb::network::PushCommand::Type)));
    Q_ASSERT(ok);
}


void PushHandler::onCreateSessionCompleted(const bb::network::PushStatus &status)
{
    qDebug() << QThread::currentThreadId() << "PushService: onCreateSessionCompleted, status" << status.code();
    if (status.isError()) {
        qDebug() << "Push error" << status.errorDescription();
    }
    // else {
    //     m_pushService->registerToLaunch();

    //     m_pushService->createChannel(QUrl(PPG_URL));
    // }
    PyGILState_STATE gil_state = PyGILState_Ensure();
    _dispatched(gil_state,
        PyObject_CallMethod(_push.dispatcher,
            "onCreateSessionCompleted",
            "i", status.code(), NULL));
}

void PushHandler::onCreateChannelCompleted(const bb::network::PushStatus &status, const QString &token)
{
    qDebug() << QThread::currentThreadId() << "PushService: onCreateChannelCompleted, status" << status.code() << "token" << token;
    if (status.isError()) {
        qDebug() << "Push error" << status.errorDescription();
    }

    PyGILState_STATE gil_state = PyGILState_Ensure();
    _dispatched(gil_state,
        PyObject_CallMethod(_push.dispatcher,
            "onCreateChannelCompleted",
            "is", status.code(), token.toUtf8().constData(), NULL));
}

void PushHandler::onDestroyChannelCompleted(const bb::network::PushStatus &status)
{
    qDebug() << QThread::currentThreadId() << "PushService: onDestroyChannelCompleted, status" << status.code();
    if (status.isError()) {
        qDebug() << "Push error" << status.errorDescription();
    }

    PyGILState_STATE gil_state = PyGILState_Ensure();
    _dispatched(gil_state,
        PyObject_CallMethod(_push.dispatcher,
            "onDestroyChannelCompleted",
            "i", status.code(), NULL));
}

void PushHandler::onRegisterToLaunchCompleted(const bb::network::PushStatus &status)
{
    qDebug() << QThread::currentThreadId() << "PushService: onRegisterToLaunchCompleted, status" << status.code();
    if (status.isError()) {
        qDebug() << "Push error" << status.errorDescription();
    }

    PyGILState_STATE gil_state = PyGILState_Ensure();
    _dispatched(gil_state,
        PyObject_CallMethod(_push.dispatcher,
            "onRegisterToLaunchCompleted",
            "i", status.code(), NULL));
}

void PushHandler::onUnregisterFromLaunchCompleted(const bb::network::PushStatus &status)
{
    qDebug() << QThread::currentThreadId() << "PushService: onUnregisterFromLaunchCompleted, status" << status.code();
    if (status.isError()) {
        qDebug() << "Push error" << status.errorDescription();
    }

    PyGILState_STATE gil_state = PyGILState_Ensure();
    _dispatched(gil_state,
        PyObject_CallMethod(_push.dispatcher,
            "onUnregisterFromLaunchCompleted",
            "i", status.code(), NULL));
}

void PushHandler::onSimChanged()
{
    qDebug() << QThread::currentThreadId() << "PushService: onSimChanged";

    PyGILState_STATE gil_state = PyGILState_Ensure();
    _dispatched(gil_state,
        PyObject_CallMethod(_push.dispatcher,
            "onSimChanged", "s",
            NULL));
}

void PushHandler::onPushTransportReady(bb::network::PushCommand::Type command)
{
    qDebug() << QThread::currentThreadId() << "PushService: onPushTransportReady, command" << command;

    PyGILState_STATE gil_state = PyGILState_Ensure();
    _dispatched(gil_state,
        PyObject_CallMethod(_push.dispatcher,
            "onPushTransportReady",
            "i", static_cast<int>(command), NULL));
}


// EOF
