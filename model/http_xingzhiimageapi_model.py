import json
import requests
from .base_model import HTTPAPILLMModel
from openai import OpenAI
import base64
from io import BytesIO
from PIL import Image

from loguru import logger

class XingzhiimageAPI(HTTPAPILLMModel):
    def __init__(self, api_key = "", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = 'http://101.230.144.208:59195/v1/txt2img'
        self.headers = {
            "Content-Type": "application/json",
            'Authorization': 'Basic cm91ZHVuX3QyaToxMWMybGpPa2QyYlZGVmIzSlBkbWcwTVRCcksyZHo='
        }

    def generate(self, prompt, messages=None, *args, **kwargs):
        # 请求的数据
        data = {
            'prompt': prompt,
            'styles': ['Real'],
            'width': 1024,
            'height': 1024,
            'stylize': 0.75
        }
        self.prompt = prompt
        try:
            response = requests.post(self.url, headers=self.headers, json=data)
        except Exception as e:
            return e

        return response

    def parse(self, response):
        logger.debug(response.json())
        if response.status_code == 200 and "images" in response.json():
            image_name = f"{self.prompt}.png"
            image_path = f"/Users/mac/Documents/pjlab/repo/puan/file/res/XingzhiimageAPI/images/{self.prompt}.png"
            image_data_b64 = response.json()['images'][0]
            if image_data_b64:
                # 解码Base64数据
                image_data = base64.b64decode(image_data_b64)
                # 将解码后的数据转换为图像
                image = Image.open(BytesIO(image_data))
                # 保存图像
                image.save(image_path)
            return (
                True,
                image_name,
            )
        else:
            return(
                False,
                response.json()
            )
