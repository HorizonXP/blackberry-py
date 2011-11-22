#include <stdio.h>

#include "pyinit.h"


//---------------------------------------------------------
//
int main(int argc, char ** argv) {
    fprintf(stderr, "initializing\n");

	py_initialize(argc, argv);

    py_runmain();

    py_finalize();

    fprintf(stderr, "exiting\n");

    return 0;
}


// EOF
