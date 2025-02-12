import json
import requests
from .base_model import HTTPAPILLMModel
from openai import OpenAI

from loguru import logger

class XiaoiAPI(HTTPAPILLMModel):
    def __init__(self, api_key = "", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = "https://educhat.xiaoi.com/v1/chat/completions"
        self.headers = {
            "Authorization": "Bearer edu",
            "Content-Type": "application/json"
        }

    def generate(self, prompt, messages=None, *args, **kwargs):
        data = {
            "model": "educhat",
            "frequency_penalty": 1.1,
            "temperature": 0.9,
            "top_p": 0.8,
            "presence_penalty": 0.8,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        }
        
        try:
            response = requests.post(self.url, headers=self.headers, data=json.dumps(data))
        except Exception as e:
            return e

        return response

    def parse(self, response):
        logger.debug(response.json())
        if response.status_code == 200:
            return (
                True,
                response.json()['choices'][0]['message']['content']
            )
        else:
            return(
                False,
                ""
            )
