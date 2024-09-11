import json
import requests
from .base_model import HTTPAPILLMModel
from openai import OpenAI

from loguru import logger

class GuomaiAPI(HTTPAPILLMModel):
    def __init__(self, api_key = "", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = "https://utils.guomai.cn/api/ai/chat"
        self.headers = {
            "Content-Type": "application/json",
        }

    def generate(self, prompt, messages=None, *args, **kwargs):
        data = {
            "content": prompt,
        }
        
        try:
            response = requests.post(self.url, headers=self.headers, data=json.dumps(data))
        except Exception as e:
            return e

        return response

    def parse(self, response):
        logger.debug(response.json())
        if response.status_code == 200 and "code" in response.json() and response.json()['code'] == 200:
            return (
                True,
                response.json()['data']['content'],
            )
        else:
            return(
                False,
                ""
            )
