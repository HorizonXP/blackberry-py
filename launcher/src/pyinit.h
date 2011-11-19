/*
 * pyinit.h
 *
 *  Created on: 2011-11-17
 *      Author: phansen
 */

#ifndef PYINIT_H_
#define PYINIT_H_

// initialize Python subsystem, loading library
int py_initialize(int argc, char ** argv);

// cleanup when we're done
void py_finalize();

// test
const char * py_test();

// launch bbxmain.py
void py_runmain();

#endif /* PYINIT_H_ */
