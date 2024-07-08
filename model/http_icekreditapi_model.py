import json
import requests
from .base_model import HTTPAPILLMModel
from openai import OpenAI
import hashlib
import uuid

from loguru import logger

class IcekreditAPI(HTTPAPILLMModel):
    def __init__(self, api_key = "", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = 'https://ai.icekredit.com/originone/chat'
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer sk-c7jgdqs3oqgdtbgk",
        }

    def generate(self, prompt, messages=None, *args, **kwargs):
        phone = "apitest5"
        password = "123456"
        sessionid = self.login_and_get_session_id(phone, password)
        chat_uuid = str(uuid.uuid4())

        data = {
            "content": prompt
        }

        json_data = json.dumps(data)

        # 定义 URL
        url = "https://ai.icekredit.com/originone/chat"
        try:
            # 发送 POST 请求
            response = requests.post(url, data=json_data, headers={"Content-Type": "application/json" , "Sessionid":  sessionid})
        except Exception as e:
            return e

        return response


    def parse(self, response):
        logger.debug(response.json())
        if response.status_code == 200:
            return (
                True,
                response.json()['data']['content'],
            )
        else:
            return(
                False,
                response.json()
            )

    def login_and_get_session_id(self, phone, password):
        # URL to which the request will be sent
        url = 'https://ai.icekredit.com/originone/user/login'

        # Hash the password using MD5
        hashed_password = hashlib.md5(password.encode()).hexdigest()

        # JSON data to be sent in the POST request
        data = {
            "phone": phone,
            "password": hashed_password
        }

        # Headers for the request
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }

        # Sending the POST request with the JSON data
        response = requests.post(url, data=json.dumps(data), headers=headers)

        # Checking the response
        if response.status_code == 200:
            response_json = response.json()
            if response_json.get('code') == '0000000' and 'data' in response_json:
                return response_json['data'].get('sessionId')
            else:
                raise ValueError("Login failed: {}".format(response_json.get('message')))
        else:
            response.raise_for_status()