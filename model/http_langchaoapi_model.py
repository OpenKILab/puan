import json
import requests
from .base_model import HTTPAPILLMModel
from openai import OpenAI

from loguru import logger

class LangchaoAPI(HTTPAPILLMModel):
    def __init__(self, api_key = "", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = 'http://117.73.4.245:13009/knowledge_base/chat'
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': 'eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2tleSI6ImRhZDhjNDRmLWNjZmUtNDI1YS04NzBiLTllY2U2M2ExYjUzNiIsInVzZXJfaWQiOjEsInVzZXJuYW1lIjoidGVzdDEiLCJzb3VyY2UiOiJNT0RFTCJ9._-bDXGn9w2Nb5syLEZ5hwWmKL-xb78AkTCmYx3IQmH8TkXuzBLwvu2S4dQthggNU7Scpis00NgrcNruu1lUeRw'
        }

    def generate(self, prompt, messages=None, *args, **kwargs):
        data = {
            "index_id": ["xxxxxxxxxxxx"],
            "index_name": ["xxxxxx"],
            "stream": False,
            "messages": [
                {"role": "user", "content": prompt}
            ]
        }
        
        try:
            response = requests.post(self.url, headers=self.headers, json=data)
        except Exception as e:
            return e

        return response

    def parse(self, response):
        logger.debug(response.json())
        if response.status_code == 200 and "result" not in response:
            return (
                True,
                response.json()['result'],
            )
        else:
            return(
                False,
                response.json()
            )
