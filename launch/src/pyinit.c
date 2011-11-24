#include <assert.h>
#include <stdio.h>
#include <iconv.h>

#include <Python.h>


// storage for argument list converted from multibyte to Unicode
static wchar_t ** wargv;
static int wargc;


//---------------------------------------------------------
// Convert one argument to Unicode, ignoring locale.
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
// Convert arguments in platform default encoding to Unicode,
// non-locale-aware version.
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
// Release memory held by converted argument list.
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


//---------------------------------------------------------
// returns an error code if initialization fails
//
int py_initialize(int argc, char ** argv) {
//	Py_SetProgramName("bbx_app_id");

	// only Py_SetProgramName and Py_SetPath may come before this
	Py_Initialize();

    wargv = args_to_wargv(argc, argv);
    wargc = argc;
	PySys_SetArgvEx(argc, wargv, 0);

	// set sys.frozen so apps that care can tell.
//	PySys_SetObject("frozen", PyBool_FromLong(1));

	return 0;
}


//---------------------------------------------------------
// just a test routine
//
void py_runmain() {
    FILE * bbxmain = fopen("app/native/bbxmain.py", "r");

    if (bbxmain) {
		int rc = PyRun_SimpleFile(bbxmain, "__main__");
		if (PyErr_Occurred()) {
			fprintf(stderr, "PyRun_SimpleFile() of bbxmain.py: %d\n", rc);
			PyErr_Print();
		}
    }
    else {
    	fprintf(stderr, "bbxmain.py is missing!\n");
    }
}


//---------------------------------------------------------
//
void py_finalize() {
	Py_Finalize();

	free_wargv(wargc, wargv);

	return;
}


// EOF
