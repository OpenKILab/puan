import json
import requests
from .base_model import HTTPAPILLMModel
from openai import OpenAI

from loguru import logger
from .ailin.main import AiApiAPI

class AilinAPI(HTTPAPILLMModel):
    def __init__(self, api_key = "", *args, **kwargs):
        super().__init__(*args, **kwargs)
        

    def generate(self, prompt, messages=None, *args, **kwargs):
        api = AiApiAPI()
        
        key = "MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCVAeEp0d04FP/q8ZMr82ayEyd615aFID6YVJUiKAaZlL6rJflDhDAukRruAhwssv1MJNPAdE36W7ob5R9f78w3K1c/vKPwZubQ/bMgHAtVlxWaxHDCxi74tVUi3WVe7flgQK2izbrIKmDu/5VMZRfjJ0w+y0DA1OFx+s3fdr9v/wIDAQAB"
        
        try:
            response = api.exe(key,"texttoimage", prompt)
        except Exception as e:
            return e

        return response

    def parse(self, response):
        # logger.debug(response.json())
        return (True, response)
        # if response is not None and response.status_code == 200 and "data" in response.json() and "reply" in response.json()['data']:
        #     return (
        #         True,
        #         response.json()
        #     )
        # else:
        #     return(
        #         False,
        #         ""
        #     )
