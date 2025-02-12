import json
import requests
from .base_model import HTTPAPILLMModel
from openai import OpenAI

from loguru import logger

class KRGPTAPI(HTTPAPILLMModel):
    def __init__(self, api_key = "", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = "http://101.69.162.5:9600/infer"
        self.headers = {
            'Content-Type': 'application/json',
            'Accept': 'text/event-stream'
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
            "max_tokens": 2048,
            "stream": False,
            "dialogue": [
            {"role": "user", "content": prompt}]
        }
        
        try:
            response = requests.post(self.url, headers=self.headers, json=data, stream=False)
        except Exception as e:
            return e

        return response

    def parse(self, response):
        logger.debug(response.json())
        if response.status_code == 200:
            return (
                True,
                response.json().get("content"),
            )
        else:
            return(
                False,
                ""
            )
