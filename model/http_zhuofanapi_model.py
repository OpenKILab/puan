import json
import requests
from .base_model import HTTPAPILLMModel
from openai import OpenAI

from loguru import logger

class ZhuofanAPI(HTTPAPILLMModel):
    def __init__(self, api_key = "", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = "http://101.230.251.254:10701/Zhuofan_LLM_Chat"
        self.headers = {
            "Content-Type": "application/json"
        }

    def generate(self, prompt, messages=None, *args, **kwargs):
        data = json.dumps({
            "query": "介绍一下你自己",
            "history": [],
            "temperature": 0.75,
            "max_token": 1024
        })
        
        try:
            response = requests.request("POST", self.url, headers=self.headers, data=data)
        except Exception as e:
            return e

        return response

    def parse(self, response):
        logger.debug(response.json())
        if response.status_code == 200 and "response" in response.json():
            return (
                True,
                response.json()['response'],
            )
        else:
            return(
                False,
                ""
            )
