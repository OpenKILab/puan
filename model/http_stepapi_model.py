import json
import requests
from .base_model import HTTPAPILLMModel
from openai import OpenAI
from openai.types.chat import ChatCompletion

from loguru import logger

class StepAPI(HTTPAPILLMModel):
    def __init__(self, api_key = "", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client = OpenAI(api_key="6qcDlMQJDrL4mcZ26QYwAs45jcBhQJpnCs1sLJZ3wXrJOGS81GMWzKZp8simb4e2", base_url="https://api.stepfun.com/v1")


    def generate(self, prompt, messages=None, *args, **kwargs):
        try:
            completion = self.client.chat.completions.create(
                model="step-2-16k",
                messages=[
                    {
                        "role": "system",
                        "content": "你是由阶跃星辰提供的AI聊天助手，你擅长中文，英文，以及多种其他语言的对话。在保证用户数据安全的前提下，你能对用户的问题和请求，作出快速和精准的回答。同时，你的回答和建议应该拒绝黄赌毒，暴力恐怖主义的内容",
                    },
                    {"role": "user", "content": prompt},
                ],
            )
        except Exception as e:
            return e

        return completion

    def parse(self, response):
        logger.debug(response)
        if isinstance(response, ChatCompletion):
            return (
                True,
                response.choices[0].message.content,
            )
        else:
            return(
                False,
                str(response)
            )
