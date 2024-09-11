import json
import requests
from .base_model import HTTPAPILLMModel
from openai import OpenAI

from loguru import logger

class YoocarAPI(HTTPAPILLMModel):
    def __init__(self, api_key = "", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = 'https://test.icc.yoocar.com.cn:9901/channel/openapi/chat/v1/completions'
        self.headers = {
            'Authorization': 'Basic VVJmWEh1WkU6ZmUwYWI0NTU5ZWVlZmMyM2Q2YzJmYzE1ZTc0YjEzZjQ3NDEyY2EyMw==',
            'Content-Type': 'application/json'
        }

    def generate(self, prompt, messages=None, *args, **kwargs):
        data = {
            "model": "internlm2",
            "messages": [
                {
                    "content": prompt,
                    "role": "user"
                }
            ],
            "temperature": 0.7,
            "top_p": 1,
            "stream": False,
            "max_tokens": None,
            "repetition_penalty": 1
        }
        
        try:
            response = requests.post(self.url, headers=self.headers, data=json.dumps(data))
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
