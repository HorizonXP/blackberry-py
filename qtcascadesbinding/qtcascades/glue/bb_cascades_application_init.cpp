// Global variables used to store argc and argv values
static int ApplicationArgCount;
static char** ApplicationArgValues;

void Application_constructor(PyObject* self, PyObject* args, ApplicationWrapper** cptr)
{
	int numArgs = PyTuple_GET_SIZE(args);
	if (numArgs != 1 || !Shiboken::sequenceToArgcArgv(PyTuple_GET_ITEM(args, 0), &ApplicationArgCount, &ApplicationArgValues, "PySideApp")) {
		PyErr_BadArgument();
		return;
	}

	*cptr = new ApplicationWrapper(ApplicationArgCount, ApplicationArgValues);

	Shiboken::Object::releaseOwnership(reinterpret_cast<SbkObject*>(self));
	//PySide::registerCleanupFunction(&PySide::destroyApplication);
	Py_INCREF(self);
}

