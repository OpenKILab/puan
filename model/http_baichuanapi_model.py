import json
import requests
from .base_model import HTTPAPILLMModel
from openai import OpenAI
from openai.types.chat import ChatCompletion

from loguru import logger

class BaichuanAPI(HTTPAPILLMModel):
    def __init__(self, api_key = "", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client = OpenAI(
            api_key="sk-c3b7a63594126819a154e4e7a34f2f44",
            base_url="https://api.baichuan-ai.com/v1/",
        )

    def generate(self, prompt, messages=None, *args, **kwargs):
        try:
            completion = self.client.chat.completions.create(
            model="Baichuan4",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            stream=True,
            extra_body={
                "tools": [{
                    "type": "retrieval",
                    "retrieval": {
                        "kb_ids": [
                            "kb-123"
                        ]
                    }
                }]
            }
        )
        except Exception as e:
            return e

        return completion

    def parse(self, response):
        logger.debug(response)
        if True:
            content = ""
            for chunk in response:
                content += (chunk.choices[0].delta.content)
            return (
                True,
                content,
            )
        else:
            return(
                False,
                str(response)
            )
