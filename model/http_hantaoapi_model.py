import json
import requests
from .base_model import HTTPAPILLMModel
from openai import OpenAI

from loguru import logger

class HantaoAPI(HTTPAPILLMModel):
    def __init__(self, api_key = "", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = 'https://platsearch-openapi.meituan.com/api/interact/getinteractresult'
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': '88831adbea7d',
        }

    def generate(self, prompt, messages=None, *args, **kwargs):
        data = {
            "message": prompt,
        }
        
        try:
            response = requests.post(self.url, headers=self.headers, json=data)
        except Exception as e:
            return e

        return response

    def parse(self, response):
        if response.status_code == 200:
            response_data = response.json()
        
            def extract_text(data):
                texts = []
                for module in data['reply']['moduleItemList']:
                    for record in module['recordList']:
                        value_map = record.get('valueMap')
                        if value_map:
                            text_json = value_map.get('text')
                            if text_json:
                                try:
                                    richtextlist = json.loads(text_json).get('richtextlist', [])
                                    for item in richtextlist:
                                        if 'text' in item:
                                            texts.append(item['text'])
                                except json.JSONDecodeError:
                                    # 打印错误信息并继续
                                    # print(f"Skipping invalid JSON: {text_json}")
                                    ...
                return texts

            # 提取文本
            extracted_texts = extract_text(response_data)
            result = ""
            # 打印提取的文本
            for text in extracted_texts:
                result += text
            logger.info(result)
            return {
                True,
                result
            }
        else:
            return {
                False,
                str(response)
            }