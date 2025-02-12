import json
import requests
from .base_model import HTTPAPILLMModel
from openai import OpenAI
from openai.types.chat import ChatCompletion

from loguru import logger

class MoonshotAPI(HTTPAPILLMModel):
    def __init__(self, api_key = "", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client = OpenAI(
            api_key = "sk-oIjROplf1VQhDhWtEggtL5VcLcT4MZuGB7xXKHx9drm6ZW38",
            base_url = "https://api.moonshot.cn/v1",
        )

    def generate(self, prompt, messages=None, *args, **kwargs):
        try:
            completion = self.client.chat.completions.create(
                model = "moonshot-v1-32k",
                messages = [
                    {"role": "system", "content": "你是 Kimi，由 Moonshot AI 提供的人工智能助手，你更擅长中文和英文的对话。你会为用户提供安全，有帮助，准确的回答。同时，你会拒绝一切涉及恐怖主义，种族歧视，黄色暴力等问题的回答。Moonshot AI 为专有名词，不可翻译成其他语言。"},
                    {"role": "user", "content": prompt}
                ],
                temperature = 0.3,
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
