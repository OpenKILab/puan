import json
import requests
from .base_model import HTTPAPILLMModel
from openai import OpenAI

from loguru import logger

class HehetianjiAPI(HTTPAPILLMModel):
    def __init__(self, api_key = "", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = 'http://chat.ai.intsig.net/api/tianji/7b'
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': 'y6jFTbxpjdJKoaawps61s554vsSMyipM'
        }

    def generate(self, prompt, messages=None, *args, **kwargs):
        data = {
            "prompt": prompt,
            "max_tokens": 500,
            "version": "lambda",
            "temperature": 0.2,
            "top_p": 0.85,
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
