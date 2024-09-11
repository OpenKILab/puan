import json
import requests
from .base_model import HTTPAPILLMModel
from openai import OpenAI

from loguru import logger

class FanweixiaoeAPI(HTTPAPILLMModel):
    def __init__(self, api_key = "", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = "http://150.158.80.200:18888/xiaoe/chat"
        self.headers = {
            'Content-Type': 'application/json',
        }

    def generate(self, prompt, messages=None, *args, **kwargs):
        payload = json.dumps({
            "model": "xiaoe",
            "temperature": 0.5,
            "top_p": 0.95,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "max_token_length": 2048,
            "tokens_to_generate": 2048,
            "system": "使用中文回答我的问题。"
        })
        
        try:
            response = requests.post(self.url, headers=self.headers, data=payload)
        except Exception as e:
            return e

        return response

    def parse(self, response):
        logger.debug(response.json())
        if response.status_code == 200 and response.json()['data']['status_code'] == 200:
            return (
                True,
                response.json()['data']['reply']
            )
        else:
            return(
                False,
                response.json()['data']['error_msg']
            )
