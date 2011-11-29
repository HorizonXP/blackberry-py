'''Demonstrate flashing screen different colours'''

import time
import random


def run():
    import bbxrun

    start = time.time()
    while time.time() - start < 5:
        colour = random.randint(0, 2**32-1)
        bbxrun.screen.fill_screen(colour)
        bbxrun.screen.redraw()
        time.sleep(0.04)


# EOF
