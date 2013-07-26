'''Make a quick crude icon from simple text.'''

import os
import sys

from PIL import Image, ImageDraw, ImageFont

from .. import command


ICON_HEIGHT = 114
ICON_WIDTH = 114


# rounded rectangle code from:
# http://nadiana.com/pil-tutorial-basic-advanced-drawing#Drawing_Rounded_Corners_Rectangle
def round_corner(radius, fill):
    """Draw a round corner"""
    corner = Image.new('RGBA', (radius, radius), (0, 0, 0, 0))
    draw = ImageDraw.Draw(corner)
    draw.pieslice((0, 0, radius * 2, radius * 2), 180, 270, fill=fill)
    return corner

def round_rectangle(size, radius, fill):
    """Draw a rounded rectangle"""
    width, height = size
    rectangle = Image.new('RGBA', size, fill)
    corner = round_corner(radius, fill)
    rectangle.paste(corner, (0, 0))
    rectangle.paste(corner.rotate(90), (0, height - radius)) # Rotate the corner and paste it
    rectangle.paste(corner.rotate(180), (width - radius, height - radius))
    rectangle.paste(corner.rotate(270), (width - radius, 0))
    return rectangle



class Command(command.Command):
    def add_arguments(self, parser):
        '''Add arguments for this command to an argparse.ArgumentParser.'''
        # parser = argparse.ArgumentParser(description='Auto-generate icon from text')
        parser.add_argument('-o', '--output', default='icon.png',
            help='output filename (default: %(default)s)')
        parser.add_argument('-f', '--force', action='store_true',
            help='force overwriting of output file')
        parser.add_argument('text',
            help='text to place in icon')


    def run(self, args):
        img = round_rectangle((ICON_WIDTH, ICON_HEIGHT), radius=ICON_WIDTH // 8, fill='skyblue')
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype('c:/windows/fonts/DejaVuSans.ttf', ICON_HEIGHT // 4)
        def draw_centered(y, text):
            size = font.getsize(text)
            x = (ICON_WIDTH - size[0]) // 2
            draw.text((x, y), text, font=font, fill='black')
            return size[1]

        # decoding as string-escape allows embedding \n and such
        text = args.text.encode('utf-8').decode('unicode_escape')
        lines = text.split('\n')

        #~ row_height = font.getsize('m')[1]
        # This would be better figured out automatically but I don't know how yet.
        # The getsize() routine doesn't show me inter-line spacing so I can't
        # compensate for that. For now just hardcode the starting vertical position.
        y = {1: 40, 2: 18, 3: 5}[len(lines)]
        height = {1: 0, 2: 49, 3: 35}[len(lines)]

        for line in text.split('\n'):
            draw_centered(y, line)
            y += height

        if os.path.exists(args.output):
            if not args.force:
                sys.exit('error: output file already exists (use --force to overwrite)')

        img.save(args.output)
