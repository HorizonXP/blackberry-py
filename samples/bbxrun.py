import time
import qnx.dialog
import os.path
import os
def run():
    basedir = "/accounts/1000/shared/documents/scripts/"
    buttonOkay = qnx.dialog.make_button("OK")
    buttonCancel = qnx.dialog.make_button("Cancel")
    files = []
    dirlist = os.listdir(basedir)
    for fname in dirlist:
        if fname.endswith(".py") and not fname.startswith("."):
            files.append(fname)
    dialog = qnx.dialog.Dialog(42, qnx.dialog.Dialog.TYPE_POPUP, buttons=[buttonCancel, buttonOkay], items=files)
    results = dialog.show_for_response(messageText="Enter a file to run")
    script = basedir + files[results['selectedIndices'][0]]
    print(results)
    print(script)
    dialog = qnx.dialog.Dialog(42, qnx.dialog.Dialog.TYPE_ALERT, buttons=[buttonOkay])
    if os.path.isfile(script):
        dialog.show_for_response(messageText="Press OK to run:" + script)
        namespace = {}
        exec(open(script).read(), namespace)
        namespace['run']()
    else:
        dialog.show_for_response(messageText="File not found")
