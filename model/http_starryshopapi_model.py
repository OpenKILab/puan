import json
import requests
from .base_model import HTTPAPILLMModel
from openai import OpenAI

from loguru import logger

class StarryshopAPI(HTTPAPILLMModel):
    def __init__(self, api_key = "", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = 'https://xiaoin-model.starringshop.com/chat'
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer sk-uo8Tdou93tuRm1pA'
        }

    def generate(self, prompt, messages=None, *args, **kwargs):
        data = {
            "model": "xiaoin-v3-4090",
            "content": prompt,
            "temperature": 0.9,
            "tokens_to_generate": 100
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
                response.json()['reply']
            )
        else:
            return(
                False,
                ""
            )
