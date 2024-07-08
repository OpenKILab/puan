import json
import requests
from .base_model import HTTPAPILLMModel
from openai import OpenAI

from loguru import logger

class WangyifuxiAPI(HTTPAPILLMModel):
    def __init__(self, api_key = "", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = "https://wangyifuxi.apps-cae.danlu.netease.com/"
        self.headers = {
            "Content-Type": "application/json",
        }

    def generate(self, prompt, messages=None, *args, **kwargs):
        # formatted_messages = [
        #     {
        #         "role": item["role"],
        #         "content": item["content"],
        #     }
        #     for item in messages
        # ]
        cookies = { 
            'RBAC_USER':'yuyan_test19@163.com', 
            'RBAC_TOKEN': 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjoieXV5YW5fdGVzdDE5QDE2My5jb20iLCJleHBpcmUiOjE4MDAyNTYxNjN9.DsAG3lFsiI_RI5JhBitG6E1tBgwjlcMBqTYURDEpj0gshTAmbfe0-bYLlHxlgQCFHAy5u9GaD5Tk7fnEKhkip37uaMmob5P4ZNE82yKMfthyRGqkz5EKbX6xES4TpIhLRKJfiP7RqPX43yOTHLx5seNcPzI-pj2fkpJ0GEn4Iq1VEl2kZTRNUCDOb5FyBBh83NfbTKFiM-ZBAy3UKvLXWzExwSajMzhmne7xtJxxVgPMrYBR7rMkxDYA6ZFfBsTLLTzj6QfnrUY5pp34pdjOandw23VzHl-vGE-3jk0NbAUeA6NOaE9J6WxgieZdqKrPO8HcjfmlBpxJr34rks-BgA ' } 

        data = { "content": [{"role": "user", "content": prompt}], "type": 0 } 
        
        try:
            response = requests.post(url="https://wangyifuxi.apps-cae.danlu.netease.com/wangxindaily/api/v1/msg", json=data, cookies=cookies) 
        except Exception as e:
            return e

        return response

    def parse(self, response):
        logger.debug(response.json())
        if response.status_code == 200:
            return (
                True,
                response.json()['content'],
            )
        else:
            return(
                False,
                ""
            )
