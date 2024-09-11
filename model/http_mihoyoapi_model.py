import json
import requests
from .base_model import HTTPAPILLMModel
from openai import OpenAI

from loguru import logger

class MihoyoAPI(HTTPAPILLMModel):
    def __init__(self, api_key = "", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = 'http://114.94.15.97:4567/api/v1/chat'
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': '8229388d-37ff-41c3-b0ef-0435c5b8abbd'
        }

    def generate(self, prompt, messages=None, *args, **kwargs):
        # formatted_messages = [
        #     {
        #         "role": item["role"],
        #         "content": item["content"],
        #     }
        #     for item in messages
        # ]
        
        data = {
            "temperature": 1,
            "top_p": 1,
            "content": prompt,
            "tokens_to_generate": 1000,
            "history": [
                {"role": "user", "content": "好久不见"},
                {"role": "assistant", "content": "你好呀！"}
            ]
        }

        # 将数据转换为 JSON 格式
        json_data = json.dumps(data)
        
        try:
            response = requests.post(self.url, headers=self.headers, data=json_data)
        except Exception as e:
            return e

        return response

    def parse(self, response):
        logger.debug(response.json())
        if response.status_code == 200:
            return (
                True,
                response.json()['reply'],
            )
        else:
            return(
                False,
                response.json()
            )
