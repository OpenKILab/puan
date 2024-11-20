import json
import requests
from .base_model import HTTPAPILLMModel
from openai import OpenAI

from loguru import logger

class ChemistryAPI(HTTPAPILLMModel):
    def __init__(self, api_key = "", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = "http://chemvlm.1761768484581117.cn-wulanchabu.pai-eas.aliyuncs.com/v1/chat/completions"
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer OTBlZTI5YjlkOTg1YjgyNDc4MGUzYjZkMGM3ZDhkOWIzODZhZGZmYw==",
        }

    def generate(self, prompt, messages=None, *args, **kwargs):
        data = {
            "model": "ChemLLM-20B-Chat-DPO-Tool-LoRA",
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
        if response.status_code == 200 and "choices" in response.json():
            return (
                True,
                response.json()['choices'][0]['message']['content'],
            )
        else:
            return(
                False,
                response.json()
            )
