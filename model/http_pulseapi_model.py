import json
import requests
from .base_model import HTTPAPILLMModel
from openai import OpenAI

from loguru import logger

class PulseAPI(HTTPAPILLMModel):
    def __init__(self, api_key = "", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = "https://mchatgpt-internal.dev.6ccloud.com/v1/api/completion/generate_json"
        self.headers = {
            'accept': 'application/json',
            'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI4NWQ1MTU0Ny0wMmM2LTRlMjItYmM2Mi0wZjQwNWE0MTM5MWEiLCJleHAiOjIwMzYzOTIxOTcsInNjb3BlcyI6WyJ1c2VyIl19.vK9766zSPP7scda-QlInmO3VK8WPt4P2lBeraG1mMkE',
            'Content-Type': 'application/json'
        }

    def generate(self, prompt, messages=None, *args, **kwargs):
        payload = json.dumps({
            "action": "To user",
            "parent_messages": [
                {
                    "action": "From user",
                    "content": prompt
                }
            ],
            "gen_kwargs": {
                "model": "102bv15_1_no_tools",
                "num_return_sequences": 1
            }
        })
        
        try:
            response = requests.request("POST", self.url, headers=self.headers, data=payload).json()
        except Exception as e:
            return e

        return response

    def parse(self, response):
        logger.debug(response)
        if "messages" in response:
            return (
                True,
                response['messages'][0]['content']['parts'][0],
            )
        else:
            return(
                False,
                response.json()
            )
