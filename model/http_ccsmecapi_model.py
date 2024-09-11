import json
import requests
from .base_model import HTTPAPILLMModel
from openai import OpenAI

from loguru import logger

class CcsmecAPI(HTTPAPILLMModel):
    def __init__(self, api_key = "", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = 'http://conscious.ccsmec.com/v1/chat/completions'
        self.headers = {
            'Authorization': '5a105e8b9d40e1329780d62ea2265d8a',
            'Content-Type': 'application/json'
        }

    def generate(self, prompt, messages=None, *args, **kwargs):
        data = {
            "model": "xawz_llm",
            "messages": [
                {
                    "content": prompt,
                    "role": "user"
                }
            ],
            "temperature": 0.7,
            "top_p": 1,
            "stream": False,
            "max_tokens": None,
            "repetition_penalty": 1
        }
        
        try:
            response = requests.post(self.url, headers=self.headers, data=json.dumps(data))
        except Exception as e:
            return e

        return response

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
                ""
            )
