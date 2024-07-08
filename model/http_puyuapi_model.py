import json
import requests
from .base_model import HTTPAPILLMModel
from openai import OpenAI

from loguru import logger

class PuyuAPI(HTTPAPILLMModel):
    def __init__(self, api_key = "", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = 'https://puyu.openxlab.org.cn/puyu/api/v1/chat/completions'
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer eyJ0eXBlIjoiSldUIiwiYWxnIjoiSFM1MTIifQ.eyJqdGkiOiIxNjMwMTkiLCJyb2wiOiJST0xFX1JFR0lTVEVSIiwiaXNzIjoiT3BlblhMYWIiLCJpYXQiOjE3MTg4NTUyNTEsImNsaWVudElkIjoibXF6a3BsbW53OTdvcGtvMzZqcWoiLCJwaG9uZSI6IjE1OTg4MTM1NjI0IiwidXVpZCI6IjU2ZGI5MDdjLTg5ZjQtNGM3OC04ZDVlLWE0NGYzMTgwYTlmMyIsImVtYWlsIjoibGVpc2hhbnpoZUBwamxhYi5vcmcuY24iLCJleHAiOjE3MzQ0MDcyNTF9.6fY3o_9HCU7wGSGFgc1YFEC-8AIPb_qtL1zxvkQMXLJ8OLdmy3ayh8wg1QDckHqUV6Dr7vFGlefTkAgiarRnyA"
        }

    def generate(self, prompt, messages=None, *args, **kwargs):
        payload = {
            "model": "internlm2-for-game", 
            "messages": [{
                "role": "user",
                "text": prompt,
            }],
            "temperature": 0.8,
            "top_p": 0.9
        }
        logger.debug(payload)
        try:
            response = requests.post(self.url, headers=self.headers, data=json.dumps(payload))
        except Exception as e:
            return e

        return response

    def parse(self, response):
        if "success" not in response and "code" not in response:
            return (
                True,
                response.json()["choices"][0]["message"]["content"],
            )
        else:
            return(
                False,
                # response.json()["msg"] 
                str(response.json())
            )
