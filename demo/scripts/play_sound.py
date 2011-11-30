'''Demonstrate playing WAV file'''

import os
from qnx import audio

WAV_FILE = 'app/python/scripts/zirbly.wav'

def run():
    player = audio.AudioPlayer()
    player.play(WAV_FILE)
