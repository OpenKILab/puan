import json
import requests
import time
import hashlib
from .base_model import HTTPAPILLMModel
from openai import OpenAI

from loguru import logger

class MobvoiAPI(HTTPAPILLMModel):
    def __init__(self, api_key = "", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = 'https://open-ka.mobvoi.com/api/chat/v2/chat'
        self.headers = {
            "Content-Type": "application/json"
        }
        # 输入账户对应的appkey
        self.appkey = 'EF830CBF0BCC88175ABC9CBC8832249D'
        # 输入账号对应的secret
        self.secret = 'DC97D999ED4726EB8FBCFD1D596A3EFC'


    def generate(self, prompt, messages=None, *args, **kwargs):
        timestamp = str(int(time.time()))
        message = '+'.join([self.appkey, self.secret, timestamp])
        m = hashlib.md5()
        m.update(message.encode('utf-8'))
        signature = m.hexdigest()
        try:
            data = {
                'appkey': self.appkey,
                'signature': signature,
                'timestamp': timestamp,
                'model': 'uclai-large',
                'stream': False,
                'messages': [
                    {
                        "content": prompt,
                        "role": "user"
                    }
                ]
            }
            result = requests.post(self.url, headers=self.headers, data=json.dumps(data))
            return result
        except Exception as e:
            return e

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
