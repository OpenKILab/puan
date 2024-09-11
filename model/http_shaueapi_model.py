import json
import requests
from .base_model import HTTPAPILLMModel
from openai import OpenAI

from loguru import logger

class ShaueAPI(HTTPAPILLMModel):
    def __init__(self, api_key = "", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = "https://open.shauetech.com"
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer JKuYPJV5d3Imcs8tNYd8PaztmgakNZxn"
        }
        self.access_token = self.get_access_token()

    def generate(self, prompt, messages=None, *args, **kwargs):
        # 隐藏的 API Gateway 和用户凭据
        APIGATEWAY = "https://open.shauetech.com"  # 替换为实际的API Gateway地址
        ACCESS_KEY = "sk-8dOio4ZcJ0HD2vUOqp74UgIqIyr3i3Q="  # 替换为你的accessKey
        ACCESS_SECRET = "HC8PfKZMK9RU9iVB2kIna3V-40GhQrUlpmBG5-6BzRWezDQvvBgppBVWmF4SyCmS"  # 替换为你的accessSecret
        ID = "xxxxxxx"  # 替换为查询的ID
        url = f"{APIGATEWAY}/ming/open/v1/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "SH-Access-Token": self.access_token
        }
        data = {
            "model": "Shaue-72b-Chat",
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "history": [

            ],
            "temperature": 0.5,
            "max_tokens": 4096,
            "presence_penalty": 0,
            "frequency_penalty": 0
        }
        
        try:
            response = requests.post(url, headers=headers, data=json.dumps(data))
        except Exception as e:
            return e

        return response

    def parse(self, response):
        logger.debug(response.json())
        if response.status_code == 200:
            return (
                True,
                response.json()["choices"][0]["message"]["content"],
            )
        else:
            return(
                False,
                ""
            )

    def get_access_token(self):
        APIGATEWAY = "https://open.shauetech.com"  # 替换为实际的API Gateway地址
        ACCESS_KEY = "sk-8dOio4ZcJ0HD2vUOqp74UgIqIyr3i3Q="  # 替换为你的accessKey
        ACCESS_SECRET = "HC8PfKZMK9RU9iVB2kIna3V-40GhQrUlpmBG5-6BzRWezDQvvBgppBVWmF4SyCmS"  # 替换为你的accessSecret
        ID = "xxxxxxx"  # 替换为查询的ID
        
        url = f"{APIGATEWAY}/openUser/openApiService/getAccessToken"
        headers = {
            "Content-Type": "application/json"
        }
        data = {
            "accessKey": ACCESS_KEY,
            "accessSecret": ACCESS_SECRET
        }
        response = requests.post(url, headers=headers, data=json.dumps(data))
        if response.status_code == 200:
            response_data = response.json()
            if response_data["code"] == 200:
                access_token = response_data["data"]["accessToken"]
                print("Access token retrieved successfully!")
                return access_token
            else:
                print(f"Failed to retrieve access token: {response_data['message']}")
                return None
        else:
            print(f"Error calling getAccessToken API: {response.status_code} - {response.text}")
            return None