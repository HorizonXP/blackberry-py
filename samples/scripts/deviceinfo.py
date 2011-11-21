import time
import qnx.dialog
import qnx.device
def run():
    buttonOkay = qnx.dialog.make_button("OK")
    dialog = qnx.dialog.Dialog(42, qnx.dialog.Dialog.TYPE_ALERT, buttons=[buttonOkay])
    text = "device_os=" + bytes.decode(qnx.device.device_os())
    text += "\nhardware_id=" + bytes.decode(qnx.device.hardware_id())
    text += "\npin=" + bytes.decode(qnx.device.pin())
    text += "\nscm_bundle=" + bytes.decode(qnx.device.scm_bundle())
    text += "\nserial_number=" + bytes.decode(qnx.device.serial_number())
    text += "\nvendor_id=" + bytes.decode(qnx.device.vendor_id())

    dialog.show_for_response(titleText="Device Info", messageText=text)
