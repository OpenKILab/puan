import json
import requests
from .base_model import HTTPAPILLMModel
from openai import OpenAI
import uuid

from loguru import logger

class QisimiaoxiangAPI(HTTPAPILLMModel):
    def __init__(self, api_key = "", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = 'https://llm-platform.eastmoney.com/api/verify2/apiAsk'
        self.headers = {
            "Content-Type": "application/json",
            'Authorization': 'yb-0a96130c-f2d4-4f3d-85ae-570ba65e6416'
        }

    def generate(self, prompt, messages=None, *args, **kwargs):
        request_param = {
            "randomCode": str(uuid.uuid4()),
            "token": "buH07uli",
            "question": prompt,
            "history": [
            ],
        }
        
        try:
            response = requests.post(self.url, headers=self.headers, json=request_param)
        except Exception as e:
            return e

        return response

    def parse(self, response):
        logger.debug(response.json())
        if response.status_code == 200 and "data" in response.json():
            return (
                True,
                response.json()['data'],
            )
        else:
            return(
                False,
                ""
            )
