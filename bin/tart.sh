#!/bin/bash

# We need this to mirror the tart.cmd script which updates
# the PYTHONPATH with the folder in which the script resides,
# so the -m option can find the tartutil package. Or something.
python3.2 -m tartutil "$@"
