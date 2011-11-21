'''Demonstrate different types of notification'''

import time
import qnx.notification as qn
import qnx.dialog as dlg

def run():
    # simple notification does not block program flow
    # sound names available are:
    #   input_keypress
    #   notification_general
    #   notification_sapphire
    #   alarm_battery
    #   event_recording_start
    #   event_recording_stop
    #   event_device_lock
    #   event_device_unlock
    #   event_device_tether
    #   event_device_untether
    #   event_video_call
    #   event_video_call_outgoing
    #   system_master_volume_reference

    notify = qn.SimpleNotification('Feel the power!',
        icon='/accounts/1000/shared/documents/scripts/logo35x35.png',
        soundName='event_video_call_outgoing',
        timeout=20,
        showTimeFlag=True,
        )
    print('simple', notify)
    time.sleep(2)

    notify2 = qn.SimpleHTTPNotification('Feel the <b><font color="#ff0000">power</font></b>!',
        timeout=20,
        )
    print('simplehttp', notify2)
    time.sleep(5)

    prompt = qn.NotificationWithPrompt('Did you feel the power?',
        optionsList=['Yes', 'No', 'Maybe a little'],
        timeout=10,
        )
    # response will be -1 if timeout, or the index of the response in the optionsList
    # e.g. 1 for 'No'
    result = prompt.GetResult()
    print('prompt', prompt, 'result', result)

    # if first is still active, this will remove it
    notify.CancelNotification()

    # All notifications will be removed once the objects are garbage-collected
    # but if you keep a global reference it will stay as long as the app runs
    # or until it times out.  This isn't how you'd do this in most real code.
    import bbxrun
    bbxrun.keepthisalive = notify2
