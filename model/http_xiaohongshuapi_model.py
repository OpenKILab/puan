import json
import requests
from .base_model import HTTPAPILLMModel
from openai import OpenAI

from loguru import logger

class XiaohongshuAPI(HTTPAPILLMModel):
    def __init__(self, api_key = "", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = 'https://test823.xiaohongshu.com/xhs_llm_v202404/http_simple/generate'
        self.headers = {
            "Content-Type": "application/json",
            'Authorization': "Bearer c667f9aa0099487b09292a848f0fafe7"
        }

    def generate(self, prompt, messages=None, *args, **kwargs):
        # formatted_messages = [
        #     {
        #         "role": item["role"],
        #         "content": item["content"],
        #     }
        #     for item in messages
        # ]

        req_body = {
            "conversation_id": "",
            "message": prompt
        }
        
        try:
            resp = requests.post(self.url, json=req_body, headers=self.headers)
            resp.encoding = 'utf-8'
            
        except Exception as e:
            return e

        return resp

    def parse(self, response):
        logger.debug(response.json())
        if response.status_code == 200:
            return (
                True,
                response.json()['reply'],
            )
        else:
            return(
                False,
                ""
            )
