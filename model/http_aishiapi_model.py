import json
import requests
from .base_model import HTTPAPILLMModel
from openai import OpenAI

from loguru import logger

class AishiAPI(HTTPAPILLMModel):
    def __init__(self, api_key = "", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = "https://app-api.aishiai.com/creative_platform/generation"
        self.headers = {
            "Token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJBY2NvdW50SWQiOjI4MjY3MjY3NzQ5MTExMiwiRXhwaXJlVGltZSI6MTcyMzQ2MDI2NywiVXNlcm5hbWUiOiIxODcxMDM0OTg0OSJ9.L8Ala9j3B0SLAkXGL7p1cX0x5ufANiInh5mv__qaW2Q",
            "Content-Type": "application/json"
        }

    def generate(self, prompt, messages=None, *args, **kwargs):
        data = {
            "model": "aishi_0.0.1",
            "prompt": "随意输入任意文字提示词"
        }
        
        try:
            response = requests.post(self.url, headers=self.headers, json=data)
        except Exception as e:
            return e

        return response

    def parse(self, response):
        logger.debug(response.json())
        if response.status_code == 200 and "Resp" in response.json() and "reply" in response.json()['Resp']:
            return (
                True,
                response.json()['Resp']['reply'],
            )
        else:
            return(
                False,
                response.json()
            )
