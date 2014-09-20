from PIL import Image, ImageDraw, ImageFont
from models import EventManager
from io import BytesIO

class ParameterImage(object):

    __PADDING__ = 10
    __HEADERFONT__ = '/Library/Fonts/Arial Bold.ttf'
    __BODYFONT__ = '/Library/Fonts/Arial Bold.ttf'

    def get_image(self, tank_id, as_of):
        parameters = EventManager().get_latest_measurements(tank_id, as_of)
        header = 'Parameters as of {}:'.format(as_of.strftime('%Y-%m-%d'))
        text = []
        for parameter in parameters:
            text.append('{}: {} {}'.format(parameter.label, parameter.value, parameter.units))
        
        headerfont = ImageFont.truetype(ParameterImage.__HEADERFONT__, 18)
        font = ImageFont.truetype(ParameterImage.__BODYFONT__, 16)
        
        maxwidth, maxheight = (x + ParameterImage.__PADDING__ for x in headerfont.getsize(header))
        totalheight = maxheight

        for line in text:
            width, height = (x + ParameterImage.__PADDING__ for x in font.getsize(line))
            maxwidth = (width if width > maxwidth else maxwidth)
            maxheight = (height if height > maxheight else maxheight)
            totalheight += height

        totalheight += ParameterImage.__PADDING__

        img = Image.new('RGBA', (maxwidth, totalheight))
        draw = ImageDraw.Draw(img)
        draw.rectangle([0, 0, maxwidth - 1, totalheight - 1], outline='#000000')
        
        draw.text((5, 2), header, fill='#000000', font=headerfont)
        y = maxheight + 2
        for line in text:
            draw.text((15, y), line, fill='#000000', font=font)
            y += maxheight

        return img

    def get_image_stream(self, tank_id, as_of):
        stream = BytesIO()
        self.get_image(tank_id, as_of).save(stream, 'PNG')
        stream.seek(0)
        return stream
