import json
import requests
from .base_model import HTTPAPILLMModel
from openai import OpenAI

from loguru import logger

class KingnetaiAPI(HTTPAPILLMModel):
    def __init__(self, api_key = "", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = 'https://chat.kingnetai.com/v1/chat/completions'  
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": "04d2548f18a842e5b97a0e248467ebea",
        }

    def generate(self, prompt, messages=None, *args, **kwargs):
        data = {
            "model": "dream-maker",
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature":0.3,  
            "top_p": 0.9
        }  
        
        try:
            response = requests.post(self.url, headers=self.headers, json=data)
        except Exception as e:
            return e

        return response

    def parse(self, response):
        logger.debug(response.json())
        if response.status_code == 200 and "choices" in response.json():
            return (
                True,
                response.json()['choices'][0]['message']['content'],
            )
        else:
            return(
                False,
                response.json()
            )
