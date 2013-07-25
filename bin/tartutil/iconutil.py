'''Utilities for manipulating app icon files.'''

import os
import argparse

from PIL import Image, ImageEnhance


ICON_HEIGHT = 114
ICON_WIDTH = 114
OVERLAY = Image.open(os.path.join(os.path.dirname(__file__), 'draftoverlay.png'))


def draft_overlay(iconpath):
    icon = Image.open(iconpath)
    dimmer = ImageEnhance.Brightness(icon).enhance(0.7)
    dimmer.paste(OVERLAY, (0, 0), OVERLAY)
    return dimmer


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Overlay DRAFT on icon')
    parser.add_argument('input',
        help='input filename')
    parser.add_argument('output',
        help='output filename')
    args = parser.parse_args()

    newimage = draft_overlay(args.input)
    newimage.save(args.output)

