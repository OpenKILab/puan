import json
import requests
from .base_model import HTTPAPILLMModel
from openai import OpenAI

from loguru import logger

class EastMoneyAPI(HTTPAPILLMModel):
    def __init__(self, api_key = "", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = "https://llm-platform.eastmoney.com/api/verify/ask2"
        self.headers = {
            "Content-Type": "application/json",
        }

    def generate(self, prompt, messages=None, *args, **kwargs):
        # formatted_messages = [
        #     {
        #         "role": item["role"],
        #         "content": item["content"],
        #     }
        #     for item in messages
        # ]

        data_single_round = {
            "messages": [
                {
                "role": "user",
                "content": prompt
                }
            ],
            "token": "mocr5dqn2c0isrdzqxwuiud18uldz97z"
        }
        data = json.dumps(data_single_round)
        try:
            response = requests.post(self.url, headers=self.headers, data=data, timeout=300)
        except Exception as e:
            return e

        return response

    def parse(self, response):
        logger.debug(response.json())
        if response.status_code == 200:
            if response.json()['data'] != None:
                return (
                    True,
                    response.json()['data'],
                )
            elif response.json()['message'] != None:
                return (
                    True,
                    response.json()['message'],
                )
            else:
                return (
                    True,
                    response.json()
                )
        else:
            return(
                False,
                response.json(),
            )
