import json
import requests
from .base_model import HTTPAPILLMModel
from openai import OpenAI

from loguru import logger

class ShukunAPI(HTTPAPILLMModel):
    def __init__(self, api_key = "", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = "https://service-gpt.shukun.net/gpt/consultation"
        self.headers = {  
            'Content-Type': 'application/json',  
            'Authorization': 'whpskyv14t0TDXP4GSHMoJAirQsbqvfLKh/v4pBQWPSyGrNgcMReqR7dEaS85wpaMmLhVZ6lrsBw7pD5PcT+VOroT7KfOyiNd5dwC7wzMRCvNWS5zwwkIFuFxv7ya3kJU/n3WYb6cZZ9rvKpZ4IzoHQz5tL68q70Eg1PgVB5Vc0BiNf0GTthBA=='  
        }

    def generate(self, prompt, messages=None, *args, **kwargs):
        data = {"query": prompt, "task_history": [], "query_type": 1}  
        
        try:
            response = requests.post(self.url, headers=self.headers, json=data, stream=True)
        except Exception as e:
            return e

        return response

    def parse(self, response):
        logger.debug(response.status_code)
        if response.status_code == 200:
            content = ""
            for line in response.iter_lines():
                if line:
                    content += json.loads(line.decode("utf-8")[5:])["response"]
            logger.debug(content)
            return (
                True,
                content
            )
        else:
            return(
                False,
                ""
            )
