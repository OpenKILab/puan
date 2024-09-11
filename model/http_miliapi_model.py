import json
import requests
from .base_model import HTTPAPILLMModel
from openai import OpenAI

from loguru import logger

class MiliAPI(HTTPAPILLMModel):
    def __init__(self, api_key = "", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = 'https://affgate.ppdai.com/csbff/affgate/callRobotQA4'
        self.headers = {
            "Content-Type": "application/json",
            'Authorization': 'W9VSuPpt2Ch2rnEKE4qQ2s5Z4WzgGfM5'  # Authorization参考附件API_Authorization.txt
        }

    def generate(self, prompt, messages=None, *args, **kwargs):
        data = {
            "input_value": prompt,
            "access_token": "123",  # session id
            "recommend": "0",  # 固定为 0 即可
            "user_id": "abc"  # 用户ID，固定为 abc 即可
        }
        
        try:
            response = requests.post(self.url, headers=self.headers, json=data)
        except Exception as e:
            return e

        return response

    def parse(self, response):
        logger.debug(response.json())
        if response.status_code == 200 and "data" in response.json() and "data" in response.json()['data']:
            return (
                True,
                response.json()['data']['data']['text'],
            )
        else:
            return(
                False,
                ""
            )
