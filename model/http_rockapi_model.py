import json
import requests
from .base_model import HTTPAPILLMModel
from openai import OpenAI

from loguru import logger

class RockAPI(HTTPAPILLMModel):
    def __init__(self, api_key = "", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = "https://kb.rockai.net/open/api/dialogue/v2/syncChat"
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer JKuYPJV5d3Imcs8tNYd8PaztmgakNZxn"
        }

    def generate(self, prompt, messages=None, *args, **kwargs):
        data = {
            "prompt": prompt,
            "appId": 75,
            "historyDialogues": [
            ]
        }
        
        try:
            response = requests.post(self.url, headers=self.headers, json=data)
        except Exception as e:
            return e

        return response

    def parse(self, response):
        logger.debug(response.json())
        if response.status_code == 200 and "data" in response.json() and "reply" in response.json()['data']:
            return (
                True,
                response.json()['data']['reply'],
            )
        else:
            return(
                False,
                ""
            )
