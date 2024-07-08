import json
import requests
from .base_model import HTTPAPILLMModel
from openai import OpenAI

from loguru import logger

# qps : 0.24
class CaiyueAPI(HTTPAPILLMModel):
    def __init__(self, api_key = "", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = 'https://b-openapi.basemind.com/openapi/v1/chat/completions'
        api_key = "AI-ONE-3YdwXiSymztnqrd5krlt3NAMJ0l1N7Fk"
        self.headers = {"Content-Type": "application/json", "Authorization": "Bearer {}".format(api_key)}

    def generate(self, prompt, messages=None, *args, **kwargs):
        # formatted_messages = [
        #     {
        #         "role": item["role"],
        #         "content": item["content"],
        #     }
        #     for item in messages
        # ]
        
        data = {"model": "caiyue", "messages": [
            {"role": "system", "content": "你是 StepChat，由 FinStep 开发。"},
            {"role": "user", "content": prompt}
            ],
        "stream":False,
        "temperature": 0.5,
        "top_p": 0.9,
        "frequency_penalty": 0.05,
        "max_tokens": 10000
        }

        try:
            response = requests.post(self.url, headers=self.headers, data=json.dumps(data))
        except Exception as e:
            return e

        return response

    def parse(self, response):
        logger.debug(response.json())
        if response.status_code == 200 and 'choices' in response.json():
            return (
                True,
                response.json()['choices'][0]['message']['content'],
            )
        else:
            return(
                False,
                response.json()
            )
