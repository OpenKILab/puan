import json
import requests
from .base_model import HTTPAPILLMModel
from openai import OpenAI

from loguru import logger

# qps : 0.24
class InfiniAPI(HTTPAPILLMModel):
    def __init__(self, api_key = "", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = 'https://cloud.infini-ai.com/maas/infini-megrez-72b-32k/infini/chat/completions'
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer sk-c7jgdqs3oqgdtbgk",
        }

    def generate(self, prompt, messages=None, *args, **kwargs):
        # formatted_messages = [
        #     {
        #         "role": item["role"],
        #         "content": item["content"],
        #     }
        #     for item in messages
        # ]
        
        data = {"model": "infini-megrez-72b-32k", "messages": [{"role": "user", "content": prompt}]}

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
                response.json()['choices'][0]['message']['content'],
            )
        else:
            return(
                False,
                response.json()
            )
