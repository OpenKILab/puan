import json
import requests
from .base_model import HTTPAPILLMModel
from openai import OpenAI

from loguru import logger

class XingzhiAPI(HTTPAPILLMModel):
    def __init__(self, api_key = "", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = "http://101.230.144.208:31620/generate"
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer 7f6cd4662cffb99bd51b61ed75b5e138",
        }

    def generate(self, prompt, messages=None, *args, **kwargs):
        data = {
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "history": [
                
            ],
            "session_id": 1,
            "stop": False,
            "stream": False,
            "max_token_length": 1024,
            "top_p": 0.8,
            "temperature": 0.7
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
                response.json()
            )
