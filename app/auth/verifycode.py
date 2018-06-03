from PIL import Image, ImageDraw, ImageFont, ImageFilter
import random
import os

class verifycode:


    # 随机字母:
    def rndChar(self):
        return chr(random.randint(65, 90))

    # 随机颜色1:
    def rndColor(self):
        return (random.randint(64, 255), random.randint(64, 255), random.randint(64, 255))

    # 随机颜色2:
    def rndColor2(slef):
        return (random.randint(32, 127), random.randint(32, 127), random.randint(32, 127))


    def generate_img(self, text=None):
        # 240 x 60:
        width = 60 * 4
        height = 60
        image = Image.new('RGB', (width, height), (255, 255, 255))
        # 创建Font对象:
        font = ImageFont.truetype('/Library/Fonts/Arial.ttf', 36)
        # 创建Draw对象:
        draw = ImageDraw.Draw(image)
        # 填充每个像素:
        for x in range(width):
            for y in range(height):
                draw.point((x, y), fill=self.rndColor())
        text = ''
        # 输出文字:
        for t in range(4):
            a = self.rndChar()
            text += a
            draw.text((60 * t + 10, 10), a, font=font, fill=self.rndColor2())
        # 模糊:
        # image = image.filter(ImageFilter.BLUR)

        filepath = os.getcwd()
        filepath = filepath + "/app/static/code.jpg"
        image.save(filepath, 'jpeg')

        return filepath, text

