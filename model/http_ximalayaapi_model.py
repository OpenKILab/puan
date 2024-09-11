import json
import requests
from .base_model import HTTPAPILLMModel
from openai import OpenAI
import http.client

from loguru import logger

class XimalayaAPI(HTTPAPILLMModel):
    def __init__(self, api_key = "", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = "http://150.158.80.200:18888/xiaoe/chat"
        self.headers = {
            'Content-Type': 'application/json',
        }

    def generate(self, prompt, messages=None, *args, **kwargs):
        payload = json.dumps({
                    "messages": [
                            { "role":"user", "content": prompt}
                        ]
                    })
        
        headers = {
            'access-token': '84183829e53f48fc8778f9512e700ee1',
            'User-Agent': 'Apifox/1.0.0 (https://www.apifox.cn)',
            'Content-Type': 'application/json',
            'Accept': '*/*',
            'Host': 'yitian.ximalaya.com',
            'Connection': 'keep-alive'
            }
        conn = http.client.HTTPSConnection("yitian.ximalaya.com", timeout = 24)
        try:
            conn.request("POST", "/llm-proxy/ximalaya/openapi/chat/completions_pro", payload, headers)
            res = conn.getresponse()
            data = res.read()
            json_data = json.loads(data.decode("utf-8"))
        except Exception as e:
            conn.close()
            return str(e)
        conn.close()
        return json_data

    def parse(self, response):
        logger.debug(response)
        if "result" in response:
            return (
                True,
                response['result']
            )
        else:
            return(
                False,
                response
            )
