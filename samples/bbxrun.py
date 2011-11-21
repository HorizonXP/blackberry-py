import time
from qnx import audio

def run():
    print('redefine run() for fun and profit')
    import os
    print('pwd is', os.getcwd())
    import os
    # os.system('waitfor shared/misc/missing 15 &')
    time.sleep(1)

def run_svn():
    time.sleep(3)
    data = open('/base/svnrev').read()
    print('Your OS has SVN revision:', data)

def run_volume():
    time.sleep(1)
    vol = audio.AudioVolume()
    before = vol.get_output_level()
    print('Volume was previously', before)
    vol.set_output_level(0)
    print('Now it should be muted.')

def run():
    vol = audio.AudioVolume()
    v = vol.get_output_level()
    if v < 1:
        v.set_output_level(25)
    player = audio.AudioPlayer()
    player.play('shared/misc/warbly.wav')
    time.sleep(1)
