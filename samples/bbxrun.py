import time
import qnx.dialog
import os.path
import os
def run():
    #Directory which holds additional scripts
    basedir = "/accounts/1000/shared/documents/scripts/"

    #Setup for file picker dialog
    buttonOkay = qnx.dialog.make_button("OK")
    buttonCancel = qnx.dialog.make_button("Cancel")
    buttonYes = qnx.dialog.make_button("Yes")
    buttonNo = qnx.dialog.make_button("No")
    buttonCont = qnx.dialog.make_button("Run another script", icon=qnx.dialog.Dialog.ICON_OPEN_LINK)
    buttonExit = qnx.dialog.make_button("Exit", icon=qnx.dialog.Dialog.ICON_DELETE)

    #Setup additional dialogs
    dialogRun = qnx.dialog.Dialog(42, qnx.dialog.Dialog.TYPE_ALERT, buttons=[buttonCancel, buttonOkay])
    dialogFail = qnx.dialog.Dialog(42, qnx.dialog.Dialog.TYPE_ALERT, buttons=[buttonOkay])

    #Main loop to allow multiple scripts to be run
    run = 1
    while run:
        #Get list of scripts
        files = []
        dirlist = os.listdir(basedir)
        for fname in dirlist:
            if fname.endswith(".py") and not fname.startswith("."):
                files.append(fname)
        files.sort()
        dialogPicker = qnx.dialog.Dialog(42, qnx.dialog.Dialog.TYPE_POPUP, buttons=[buttonCancel, buttonOkay], items=files)

        #Prompt for script to run
        results = dialogPicker.show_for_response(titleText="Select a script", messageText="Enter a file to run")
        if results['selectedIndex'] == 1:
            script = basedir + files[results['selectedIndices'][0]]

            #Check if file exists
            if os.path.isfile(script):
                results = dialogRun.show_for_response(titleText="Confirm launch", messageText="Press OK to run: " + script)
                if results['selectedIndex'] == 1:
                    namespace = {}
                    exec(open(script).read(), namespace)
                    namespace['run']()
            else:
                dialogFail.show_for_response(titleText="Error", messageText="File not found")

            #Prompt for additional run
            dialogContinue = qnx.dialog.Dialog(42, qnx.dialog.Dialog.TYPE_CONTEXT_MENU, buttons=[buttonExit, buttonCont])
            results = dialogContinue.show_for_response(titleText="Loop", messageText="Run another script?")
            if results['selectedIndex'] == 0:
                run = 0
        else:
            run = 0
