from PIL import Image, ImageDraw, ImageFont
from models import EventManager
from io import BytesIO

class ParameterImage(object):

    __PADDING__ = 10

    def get_image(self, tank_id, as_of):
        parameters = EventManager().get_latest_measurements(tank_id)
        text = ['Parameters as of {}:'.format(as_of.strftime('%Y-%m-%d'))]
        for parameter in parameters:
            text.append('    {}: {} {}'.format(parameter.label, parameter.value, parameter.units))
        
        font = ImageFont.truetype('resources/winamp.ttf', 18)
        maxwidth = 0
        maxheight = 0
        totalheight = 0
        for line in text:
            width, height = (x + ParameterImage.__PADDING__ for x in font.getsize(line))
            maxwidth = (width if width > maxwidth else maxwidth)
            maxheight = (height if height > maxheight else maxheight)
            totalheight += height

        totalheight += ParameterImage.__PADDING__

        img = Image.new('RGBA', (maxwidth, totalheight))
        draw = ImageDraw.Draw(img)
        draw.rectangle([0, 0, maxwidth - 1, totalheight - 1], outline='#000000')
        
        y = 2
        for line in text:
            draw.text((2, y), line, fill='#000000', font=font)
            y += maxheight

        return img

    def get_image_stream(self, tank_id, as_of):
        stream = BytesIO()
        self.get_image(tank_id, as_of).save(stream, 'PNG')
        stream.seek(0)
        return stream
