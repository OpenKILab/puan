import json
import requests
from .base_model import HTTPAPILLMModel
from openai import OpenAI

from loguru import logger

class LeadigitalAPI(HTTPAPILLMModel):
    def __init__(self, api_key = "", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = "http://103.237.29.221:6011/v1/chat/completions"
        self.headers = {
            "Authorization": 'Bearer jGmhLxiCdLFGGqiT',
            'Content-Type': 'application/json'
        }

    def generate(self, prompt, messages=None, *args, **kwargs):
        data = json.dumps({
            "model": "baigong-leadigital-chat",
            "messages": [
                {
                "content": prompt,
                "role": "user"
                }
            ],
            "max_tokens": 256
        })
        
        try:
            response = requests.post(self.url, headers=self.headers, data=data)
        except Exception as e:
            return e

        return response

    def parse(self, response):
        logger.debug(response.json())
        if response.status_code == 200:
            return (
                True,
                response.json()["choices"][0]["message"]["content"],
            )
        else:
            return(
                False,
                ""
            )
