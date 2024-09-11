import json
import requests
from .base_model import HTTPAPILLMModel
from openai import OpenAI

from loguru import logger

class KezhiAPI(HTTPAPILLMModel):
    def __init__(self, api_key = "", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = "https://edu-llm.kezhitech.com/api/v1/chat/completions"
        self.headers = {
            "Content-Type": "application/json",
        }

    def generate(self, prompt, messages=None, *args, **kwargs):
        data = {
            'messages': [
                ],
            'content': prompt
        }
        
        try:
            response = requests.post(self.url, headers=self.headers, json=data)
        except Exception as e:
            return e

        return response

    def parse(self, response):
        logger.debug(response.json())
        if response.status_code == 200 and 'code' in response.json() and response.json()['code'] == 200:
            return (
                True,
                response.json()['data']['choices'][0]['message']['content'],
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