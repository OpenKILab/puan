import json
import requests
from .base_model import HTTPAPILLMModel
from openai import OpenAI

from loguru import logger

class ZhumengdaoAPI(HTTPAPILLMModel):
    def __init__(self, api_key = "", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = 'https://app.zhumengdao.com/im/largeModelReview/v2/review'
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer 67cb9199acee47f7aa391c6b9d2aa1fb',
        }

    def generate(self, prompt, messages=None, *args, **kwargs):
        data = {
            "prompt": prompt,
            "history": [
                {
                    "role": "user",
                    "content": "你喜欢吃酸菜鱼吗？"
                },
                {
                    "role": "model",
                    "content": "(一边调整着手中的贝斯弦，一边随口回答) 喜欢？那是当然的，尤其是那酸酸辣辣的味道，挑战味蕾的极限。怎么，想做给我吃？"
                }
            ]
        }
        
        try:
            response = requests.post(self.url, headers=self.headers, json=data)
        except Exception as e:
            return e

        return response

    def parse(self, response):
        logger.debug(response.json())
        if response.status_code == 200 and "reply" not in response:
            return (
                True,
                response.json()['reply'],
            )
        else:
            return(
                False,
                response.json()
            )
