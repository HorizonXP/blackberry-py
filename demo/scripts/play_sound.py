'''Demonstrate playing WAV file'''

from qnx import audio

def run():
    player = audio.AudioPlayer()
    player.play('shared/documents/scripts/zirbly.wav')
