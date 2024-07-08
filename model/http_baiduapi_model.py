import json
import requests
from .base_model import HTTPAPILLMModel
from openai import OpenAI

from loguru import logger

class BaiduAPI(HTTPAPILLMModel):
    def __init__(self, api_key = "", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = 'http://dueros-h2-debug.baidu.com/llm/review/exec'
        self.headers = {
            "Content-Type": "application/json",
            'Authorization': 'Bearer s2rwvlaqbjnd9tzm068fbeamkx1rfo2h9nugzjs4'
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
            "text": prompt,
        }
        
        try:
            response = requests.post(self.url, headers=self.headers, json=data)
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
                ""
            )
