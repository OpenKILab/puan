import json
import requests
from .base_model import HTTPAPILLMModel
from openai import OpenAI
import base64
from io import BytesIO
from PIL import Image
import time
import hashlib
import os


from loguru import logger

class MobvoivoiceAPI(HTTPAPILLMModel):
    def __init__(self, api_key = "", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = 'https://open.mobvoi.com/api/tts/v1'
        self.headers = {
            "Content-Type":"application/json",
        }

    def generate(self, prompt, messages=None, *args, **kwargs):
        timestamp = str(int(time.time()))
        # 输入账户对应的appkey
        appkey = 'EF830CBF0BCC88175ABC9CBC8832249D'
        # 输入账号对应的secret
        secret = 'DC97D999ED4726EB8FBCFD1D596A3EFC'

        message = '+'.join([appkey, secret, timestamp])

        m = hashlib.md5()
        m.update(message.encode('utf-8'))
        signature = m.hexdigest()
        # 请求的数据
        data = {
            'appkey':appkey,
            'signature':signature,
            'timestamp':timestamp,
            'text':prompt,
            'speaker':'huazai_meet_24k',
            'ignore_limit':'true',
            'gen_srt': True,
            'audio_type':'wav',
            'merge_symbol':'true'
        }
        self.prompt = prompt
        self.music_style = data['audio_type']
        
        try:
            response = requests.post(self.url, headers=self.headers, data=json.dumps(data))
        except Exception as e:
            return e

        return response

    def parse(self, response):
        if response.status_code == 200:
            data1 = response.content
            adress = response.headers
            with open(os.path.join("/Users/mac/Documents/pjlab/repo/puan/file/res/Mobvoivoice/voice", f"{self.prompt[:32]}.{self.music_style}"), "wb") as f:
                f.write(data1)
            
            return (
                True,
                f"{self.prompt[:32]}.{self.music_style}",
            )
        else:
            return(
                False,
                response.json()
            )
