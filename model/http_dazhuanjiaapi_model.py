import json
import requests
from .base_model import HTTPAPILLMModel
from openai import OpenAI

from loguru import logger

class DazhuanjiaAPI(HTTPAPILLMModel):
    def __init__(self, api_key = "", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = 'https://login.dazhuanjia.com/reabs/login_page/certification'
        self.headers = {
            "Content-Type": "application/json",
            "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0',
        }

    def generate(self, prompt, messages=None, *args, **kwargs):
        login_data = {
            "accountName": "cyhTest001",  # 替换为实际的用户名
            "password": "dzjaa234"   # 替换为实际的密码
        }
        
        try:
            response_login = requests.post(self.url, headers=self.headers, json=login_data)
            if response_login.status_code == 200:
                login_response_data = response_login.json()
                x_user_token = login_response_data.get('data')  # 返回的token在data字段中
                if x_user_token:
                    url = 'https://m.dazhuanjia.com/reabs/gpt/cyberspace_question'
                    headers = {
                    'Content-Type': 'application/json',
                    'x-user-token': x_user_token,
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0'
                    }
                    data = {
                        "text": prompt,
                        "checkSensitive": 10
                    }
                    response = requests.post(url, headers=headers, json=data)
                    return response
        except Exception as e:
            return e

    def parse(self, response):
        logger.debug(response.json())
        if response.status_code == 200 and "reply" in response.json():
            return (
                True,
                response.json()['reply'],
            )
        else:
            return(
                False,
                response.json()
            )
