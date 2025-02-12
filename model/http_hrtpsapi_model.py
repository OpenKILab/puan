import json
import requests
from .base_model import HTTPAPILLMModel
from openai import OpenAI

from loguru import logger

class HrtpsAPI(HTTPAPILLMModel):
    def __init__(self, api_key = "", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = "https://ai-demo-bot.hrtps.com/v1/chat-messages"
        self.headers = {
            "Authorization": "Bearer app-6c9j1K65OsOE0gF18HHqgyIn",
            "Content-Type": "application/json"
        }

    def generate(self, prompt, messages=None, *args, **kwargs):
        data = {
            "inputs": {},
            "query": prompt,
            "response_mode": "blocking",
            "user": "caili_test1",
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
                response.json()['answer'],
            )
        else:
            return(
                False,
                ""
            )
