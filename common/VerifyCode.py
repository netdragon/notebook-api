from captcha.image import ImageCaptcha
import random
import string
import base64
from io import BytesIO


class VerifyCode:
    random_str = None
    img_data = None

    def __init__(self):
        characters = '2345689ACEFGHJKMNPQRSTUVWXY'
        width, height, n_len, n_class = 160, 65, 4, len(characters)

        generator = ImageCaptcha(width=width, height=height)
        self.random_str = ''.join(
            [random.choice(characters) for j in range(4)])
        img = generator.create_captcha_image(
            self.random_str, (153, 153, 153), (255, 255, 255))

        f = BytesIO()
        img.save(f, 'png')
        data = f.getvalue()
        f.close()

        encode_data = base64.b64encode(data)
        data = str(encode_data, encoding='utf-8')
        self.img_data = "data:image/jpeg;base64,{data}".format(data=data)
        # print(self.random_str)
        # print(self.img_data)

    def get(self):
        return self.random_str, self.img_data
