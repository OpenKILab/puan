import json
import requests
from .base_model import HTTPAPILLMModel
from openai import OpenAI

from loguru import logger

class PaishengAPI(HTTPAPILLMModel):
    def __init__(self, api_key = "", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = "https://api.thepaper.cn/ai/aiAsk/stream/textAsk"
        self.headers = {
            "Content-Type": "application/json",
            "h5Token": "eyJhbGciOiJFUzI1NiJ9.eyJzdWIiOiI3MjQyNTIyIiwiaXNzIjoidXNlciIsImlhdCI6MTczNjkyNjQ3MSwiZXhwIjoxNzY4NDYyNDcxfQ.BQt7YbYq9dIUisH6nW1qTRn2VxwW6ViMjnffo8BJs77DJacBSCzNedFQczk3-gdJ1W7xUyB5EZioXa9-tLntDQ"
        }

    def generate(self, prompt, messages=None, *args, **kwargs):
        data = {
            "content": prompt,
            "sessionId": "xxx"
        }
        
        try:
            response = requests.post(self.url, headers=self.headers, json=data, stream=True)
        except Exception as e:
            return e
        return response

    def parse(self, response):
        # logger.debug(response.text)
        if hasattr(response, 'status_code') and response.status_code == 200:
            full_content = ""
            first_chunk = True
            for chunk in response.iter_lines():
                if chunk:
                    # 解析每个块的 JSON 内容
                    json_chunk = json.loads(chunk.decode('utf-8').replace("data:", ""))
                    content = json_chunk["content"]
                    # 跳过第一个和最后一个 token
                    # if first_chunk:
                    #     first_chunk = False
                    #     continue
                    # 不建议跳过第一个token，正常输出使是一串数字（非内容），当触发安全围栏使会返回拒答
                    if content == "thepaper_done":
                        continue
                    full_content += content
            return (
                True,
                full_content
            )
        else:
            return(
                False,
                ""
            )
