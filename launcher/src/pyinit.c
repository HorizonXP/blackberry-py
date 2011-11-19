#include <assert.h>
#include <screen/screen.h>
#include <bps/navigator.h>
#include <bps/screen.h>
#include <bps/bps.h>
#include <bps/event.h>
#include <stdarg.h>
#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>
#include <limits.h>
//#include <dlfcn.h>

#undef _DEBUG
#include <Python.h>


//---------------------------------------------------------
//
static wchar_t * char2wchar(const char * arg) {
    wchar_t * res = NULL;
    size_t count;
    size_t argsize = strlen(arg);

    if (argsize != (size_t) -1) {
        res = (wchar_t *) malloc((argsize + 1) * sizeof(wchar_t));
        if (res) {
			count = mbstowcs(res, arg, argsize + 1);
			if (count == (size_t)-1) {
				free(res);
				res = NULL;
			}
        }
    }

    return res;
}


//---------------------------------------------------------
//
static wchar_t ** args_to_wargv(int argc, char ** argv) {
    int i;
    wchar_t ** wargv = NULL;

    wargv = (wchar_t **) malloc(argc * sizeof(wchar_t *));
    if (!wargv)
        return wargv;

    for (i = 0; i < argc; i++) {
        wargv[i] = char2wchar(argv[i]);
    }

    return wargv;
}


//---------------------------------------------------------
//
static void free_wargv(int wargc, wchar_t ** wargv) {
    int i = 0;
    if (wargv) {
    	for (i = 0; i < wargc; i++)
            free(wargv[i]);

        free(wargv);
    }

    return;
}


static wchar_t ** wargv;
static int wargc;

//---------------------------------------------------------
// returns an error code if initialization fails
//
int py_initialize(int argc, char ** argv) {
	fprintf(stderr, "py_initialize\n");

//	if (!LoadPythonLibrary())
//		return 255;

//	fprintf(stderr, "python DLL loaded\n");

	Py_VerboseFlag = 0;

//	Py_SetProgramName("bbx_app_id");

	// only Py_SetProgramName and Py_SetPath may come before this
	Py_Initialize();

    wargv = args_to_wargv(argc, argv);
    wargc = argc;
	PySys_SetArgvEx(argc, wargv, 0);

	// set sys.frozen so apps that care can tell.
//	PySys_SetObject("frozen", PyBool_FromLong(1));

	fprintf(stderr, "py_initialize done\n");

	return 0;
}


//---------------------------------------------------------
// just a test routine
//
int py_tested;
const char * msg = "";
const char * py_test() {
	if (!py_tested) {
		py_tested = 1;

		fprintf(stderr, "Py_VerboseFlag is %d\n", Py_VerboseFlag);

        PyRun_SimpleString("import sys\nsys.myver = ('BBX Python! v%s on %s' % (sys.version, sys.platform)).replace('\\n', '')\n");
        if (PyErr_Occurred())
        	PyErr_Print();

        wchar_t * tmpwide;
        const char * tmpstr;

        tmpwide = Py_GetPath();
        if (PyErr_Occurred())
        	PyErr_Print();
		fprintf(stderr, "Py_GetPath %ls\n", tmpwide);

        tmpwide = Py_GetProgramName();
        if (PyErr_Occurred())
        	PyErr_Print();
		fprintf(stderr, "Py_GetProgramName %ls\n", tmpwide);

        tmpwide = Py_GetExecPrefix();
        if (PyErr_Occurred())
        	PyErr_Print();
		fprintf(stderr, "Py_GetExecPrefix %ls\n", tmpwide);

        tmpwide = Py_GetProgramFullPath();
        if (PyErr_Occurred())
        	PyErr_Print();
		fprintf(stderr, "Py_GetProgramFullPath %ls\n", tmpwide);

        tmpwide = Py_GetPythonHome();
        if (PyErr_Occurred())
       	    PyErr_Print();
        if (tmpwide)
        	fprintf(stderr, "Py_GetPythonHome %ls\n", tmpwide);

        tmpstr = Py_GetVersion();
        if (PyErr_Occurred())
        	PyErr_Print();
		fprintf(stderr, "Py_GetVersion %s\n", tmpstr);

        PyObject * sysver = PySys_GetObject("myver");
        if (PyErr_Occurred())
        	PyErr_Print();

        sysver = PyUnicode_AsASCIIString(sysver);
        if (PyErr_Occurred())
        	PyErr_Print();

        msg = PyBytes_AsString(sysver);
		fprintf(stderr, "sys.version %s\n", msg);
        if (PyErr_Occurred())
        	PyErr_Print();

		fprintf(stderr, "PyRun_SimpleString done\n");
	}

	return msg;
}


//---------------------------------------------------------
// just a test routine
//
void py_runmain() {
    char * pwd = getcwd(NULL, 0);
    fprintf(stderr, "pwd is %s\n", pwd);
    free(pwd);

    FILE * bbxmain = fopen("app/native/bbxmain.py", "r");

    if (bbxmain) {
		int rc = PyRun_SimpleFile(bbxmain, "__main__");
		fprintf(stderr, "PyRun_SimpleFile() on bbxmain.py: %d\n", rc);
		if (PyErr_Occurred())
			PyErr_Print();
    }
    else {
    	fprintf(stderr, "bbxmain.py is missing\n");
    }
}


//---------------------------------------------------------
//
void py_finalize() {
	fprintf(stderr, "py_finalize\n");

	Py_Finalize();

	free_wargv(wargc, wargv);

//	dlclose(pylib);

	return;
}


// EOF
