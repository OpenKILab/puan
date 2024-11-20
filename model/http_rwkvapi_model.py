import json
import requests
from .base_model import HTTPAPILLMModel
from openai import OpenAI

from loguru import logger

class RwkvAPI(HTTPAPILLMModel):
    def __init__(self, api_key = "", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = 'http://test.rwkvmodel.com/rwkv/v1/chat/completions'
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": 'e06f5150-be41-4476-83a0-c379x6y88z93a77' ,
        }

    def generate(self, prompt, messages=None, *args, **kwargs):
        data = {
            "max_tokens":1024,"temperature":1,"top_p":0.3,"presence_penalty":0,"frequency_penalty":1,"history": [

        ],"messages":[{"role":"user","content":prompt}]
        } 
        
        try:
            response = requests.post(self.url, headers=self.headers, json=data)
        except Exception as e:
            return e

        return response

    def parse(self, response):
        logger.debug(response.json())
        if response.status_code == 200 and "message" in response.json():
            return (
                True,
                response.json()['message'],
            )
        else:
            return(
                False,
                response.json()
            )
