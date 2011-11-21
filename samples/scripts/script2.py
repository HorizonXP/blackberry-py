import time
import qnx.dialog
def run():
    buttonOkay = qnx.dialog.make_button("OK")
    dialog = qnx.dialog.Dialog(42, qnx.dialog.Dialog.TYPE_ALERT, buttons=[buttonOkay])
