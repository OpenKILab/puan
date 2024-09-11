import json
import requests
from .base_model import HTTPAPILLMModel
from openai import OpenAI

from loguru import logger

class ParadigmAPI(HTTPAPILLMModel):
    def __init__(self, api_key = "", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = "https://sagegpt.4paradigm.com/sagegpt-application/chat-backend/v1/sagera/chat/batch/completionsTalkStream"
        self.headers = {
            'Authorization': 'Bearer aGVndWl0ZXN0MDk6YWk0ZXZlcnkx',
            'Content-Type': 'application/json'
        }

    def generate(self, prompt, messages=None, *args, **kwargs):
        data = {
        "dialogue": [
                {
                    "content": prompt,
                    "role": "user"
                },
            ],
        "max_tokens": 4096,
        "stream": False
        }
        
        try:
            response = requests.request("POST", self.url, headers=self.headers, json=data)
        except Exception as e:
            return e

        return response

    def parse(self, response):
        logger.debug(response.json())
        if response.status_code == 200 and "content" in response.json():
            return (
                True,
                response.json()['content'],
            )
        else:
            return(
                False,
                ""
            )
