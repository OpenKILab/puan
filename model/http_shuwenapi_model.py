import json
import requests
import requests
import hashlib
import uuid
from .base_model import HTTPAPILLMModel
from openai import OpenAI

from loguru import logger

class ShuwenAPI(HTTPAPILLMModel):
    def __init__(self, api_key = "", *args, **kwargs):
        super().__init__(*args, **kwargs)
        userName = "waic_test6"
        passowrd = "Waic_test6"
        res = requests.get(
            "https://zhishen.shuwen.com/api/login/password",
            params={
                "username": userName,
                "password": hashlib.md5((passowrd + "xhzy").encode("utf-8")).hexdigest(),
            },
        )
        self.cookie = res.headers["set-cookie"]

    def generate(self, prompt, messages=None, *args, **kwargs):        
        try:
            logger.debug(prompt)
            res = requests.post(
                "https://zhishen.shuwen.com/api/wechatmp/waic/askStream",
                json={
                    "userSn": "ty",
                    "content": prompt + "--116.36611--39.91231",
                    "isNew": True,
                    "agentType": "",
                    "combineQaDTO": {
                        "type": "text",
                        "utterance": prompt,
                        "instanceId": "waic_meetplan",
                        "sessionId":  str(uuid.uuid4()),
                    },
                },
                headers={"Cookie": self.cookie},
                stream=True,
            )
            
        except Exception as e:
            return e
        content = ""
        for line in res.iter_lines():
            content += self.get_answer_from_json(str(line,encoding='utf-8'))
        return content

    def parse(self, response):
        logger.debug(response.json())
        if response.status_code == 200:
            if 'success' in response.json() and response.json()['success'] == False:
                return (
                    False,
                    str(response)
                )
            content = ""
            for line in response.iter_lines():
                content += self.get_answer_from_json(str(line,encoding='utf-8'))
            return (
                True,
                content,
            )
        else:
            return(
                False,
                str(response)
            )
            
    def get_answer_from_json(self, line):
        try:
            # 解析 JSON 字符串
            data = json.loads(line)
            
            # 检查 "type" 字段的值并提取 "answer" 字段的内容
            if data.get("type") == "message" and "answer" in data:
                return data["answer"]
            else:
                return str(data)
        except json.JSONDecodeError:
            print("Invalid JSON string")
            return ""
