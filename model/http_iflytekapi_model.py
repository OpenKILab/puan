import json
import requests
from .base_model import HTTPAPILLMModel
from openai import OpenAI

from loguru import logger

class IflytekAPI(HTTPAPILLMModel):
    def __init__(self, api_key = "", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = "https://spark-api-open.xf-yun.com/v1/chat/completions"
        self.header = {
            "Authorization": "Bearer mDcGbqrIWofVavEJYuyG:ZcgxdLTZGsLILFKONuWB" # 注意此处替换自己的APIPassword
        }

    def generate(self, prompt, messages=None, *args, **kwargs):
        data = {
                "model": "4.0Ultra", # 指定请求的模型
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
            }
        
        try:
            response = requests.post(self.url, headers=self.header, json=data)
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
