import json
import requests
from .base_model import HTTPAPILLMModel
from openai import OpenAI

from loguru import logger

class YunbenAPI(HTTPAPILLMModel):
    def __init__(self, api_key = "", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = 'https://mgmt.icyh.com/app-api/largemodel/sse/llm'
        self.headers = {
            "Content-Type": "application/json",
            'Authorization': 'yb-0a96130c-f2d4-4f3d-85ae-570ba65e6416'
        }

    def generate(self, prompt, messages=None, *args, **kwargs):
        data = {
            "messages": prompt
        }
        
        try:
            response = requests.post(self.url, headers=self.headers, json=data)
        except Exception as e:
            return e

        return response

    def parse(self, response):
        logger.debug(response.json())
        if response.status_code == 200 and "reply" in response.json():
            return (
                True,
                response.json()['reply'],
            )
        else:
            return(
                False,
                ""
            )
