import json
import requests
from .base_model import HTTPAPILLMModel
from openai import OpenAI

from loguru import logger

class RuyiAPI(HTTPAPILLMModel):
    def __init__(self, api_key = "", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = "https://gptapi.ruyichat.com/v6/questionanswer?source=53&version=4.0.1.9&mc=3000&uid=612350746&devid=65897677077778&verifyCode=fl2gpt6g1PV1g0pi54QMn4mDPRq41vmzDylHLQ"
        self.headers = {
            "Content-Type": "application/json",
        }

    def generate(self, prompt, messages=None, *args, **kwargs):
        data = {
            "input": prompt,
            "input_expand": "",
            "conversation_id": "612350746_65897677077778_1703472475155"
        }
        
        try:
            response = requests.post(self.url, headers=self.headers, json = data)
        except Exception as e:
            return e

        return response

    def parse(self, response):
        if response.status_code == 200:
            # 迭代处理服务器发送的每个事件
            for line in response.iter_lines():
                res = self.extract_content(str(line, 'utf-8'))
                logger.debug(res)
                return (
                    True,
                    res
                )
            return (
                True,
                "None"
            )
        else:
            return(
                False,
                ""
            )
            
    def extract_content(self, data_str):
        combined_content = ""
        buffer = ""
        bracket_count = 0

        for char in data_str:
            buffer += char
            if char == '{':
                bracket_count += 1
            elif char == '}':
                bracket_count -= 1

            # Check if we have reached the end of a JSON object
            if bracket_count == 0 and buffer:
                try:
                    # Parse the JSON object
                    json_object = json.loads(buffer)
                    # Extract content if 'data' and 'content' keys exist
                    if 'data' in json_object and 'content' in json_object['data']:
                        combined_content += json_object['data']['content']
                except json.JSONDecodeError:
                    print("Error decoding JSON")
                buffer = ""  # Reset the buffer for the next JSON object

        return combined_content
