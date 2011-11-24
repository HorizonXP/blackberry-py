import sys
import time
import os

from qnx.dialog import make_button, Dialog
from bbxpy.screen import Screen


def _run():
    # Directory which holds additional scripts
    basedir = 'shared/documents/scripts'

    # Setup for file picker dialog
    buttonOkay = make_button("OK")
    buttonCancel = make_button("Cancel")
    buttonYes = make_button("Yes")
    buttonNo = make_button("No")
    buttonCont = make_button("Run another script", icon=Dialog.ICON_OPEN_LINK)
    buttonExit = make_button("Exit", icon=Dialog.ICON_DELETE)

    # Setup additional dialogs
    dialogRun = Dialog(42, Dialog.TYPE_ALERT, buttons=[buttonCancel, buttonOkay])
    dialogFail = Dialog(42, Dialog.TYPE_ALERT, buttons=[buttonOkay])

    # Main loop to allow multiple scripts to be run
    run = 1
    while run:
        # Get list of scripts
        files = []
        dirlist = os.listdir(basedir)
        for fname in dirlist:
            if fname.endswith(".py") and not fname.startswith("."):
                files.append(fname)
        files.sort()
        dialogPicker = Dialog(42, Dialog.TYPE_POPUP, buttons=[buttonCancel, buttonOkay], items=files)

        # Prompt for script to run
        results = dialogPicker.show_for_response(titleText="Select a script", messageText="Enter a file to run")
        if results['selectedIndex'] == 1:
            script = os.path.join(basedir, files[results['selectedIndices'][0]])

            # Check if file exists
            if os.path.isfile(script):
                results = dialogRun.show_for_response(titleText="Confirm launch", messageText="Press OK to run: " + script)
                if results['selectedIndex'] == 1:
                    namespace = {}
                    try:
                        exec(open(script).read(), namespace)
                        namespace['run']()
                    finally:
                        # flush print output buffer
                        sys.stdout.flush()
            else:
                dialogFail.show_for_response(titleText="Error", messageText="File not found")

            #Prompt for additional run
            dialogContinue = Dialog(42, Dialog.TYPE_CONTEXT_MENU, buttons=[buttonExit, buttonCont])
            results = dialogContinue.show_for_response(titleText="Loop", messageText="Run another script?")
            if results['selectedIndex'] == 0:
                run = 0
        else:
            run = 0


def run():
    screen = Screen()
    screen.setup()
    try:
        _run()
    finally:
        screen.cleanup()
