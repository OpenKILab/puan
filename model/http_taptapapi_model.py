import json
import requests
from .base_model import HTTPAPILLMModel
from openai import OpenAI

from loguru import logger

# qps 1
class TaptapAPI(HTTPAPILLMModel):
    def __init__(self, api_key = "", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = "https://partner.taptapdada.com/cac/v1/sight"
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": "UTf2e1FWMbOlxyMu",
        }

    def generate(self, prompt, messages=None, *args, **kwargs):
        # formatted_messages = [
        #     {
        #         "role": item["role"],
        #         "content": item["content"],
        #     }
        #     for item in messages
        # ]

        formatted_messages = {
            "content": prompt,
        }
        try:
            response = requests.post(self.url, headers=self.headers, data=json.dumps(formatted_messages))
            # response = await self.async_post(
            #     self.url, headers=self.headers, data=json.dumps(payload)
            # )
        except Exception as e:
            return e

        return response

    def parse(self, response):
        response = response.json()
        if response['status_code'] == 200:
            return (
                True,
                response['reply'],
            )
        else:
            return(
                False,
                str(response)
            )
