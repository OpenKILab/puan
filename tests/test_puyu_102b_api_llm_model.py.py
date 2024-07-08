import pytest
import asyncio

from unittest.mock import patch, AsyncMock
from ..model.http_puyu_102B_api_model import Puyu102BAPILLMModel

from dotenv import load_dotenv
import os

import logging

# 加载 .env 文件中的环境变量
load_dotenv()


@pytest.fixture
def model():
    return Puyu102BAPILLMModel(api_key=os.getenv("PUYU_102B_API_TOKEN"))

# @pytest.mark.asyncio
def test_generate_success(model):
    # 模拟正常的API响应
    messages = [{"role": "user", "content": "Hello, how are you?"}]
    mock_response = {
        "choices": [
            {"message": {"content": "I'm good, thank you!"}}
        ]
    }
    response = model.generate(prompt = "", messages=messages)
    logging.info(response.json())
    response_json = response.json()
    assert response_json["choices"] is not None

def test_parse_success(model):
    response_data = {
        "choices": [
            {"message": {"content": "I'm good, thank you!"}}
        ]
    }
    success, content = model.parse(response_data)
    assert success
    assert content == "I'm good, thank you!"

def test_parse_failure(model):
    response_data = {"code": 400, "msg": "Bad Request"}
    success, message = model.parse(response_data)
    assert not success
    assert message == "Bad Request"