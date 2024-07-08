import pytest
import os

from model.http_puyu_102B_api_model import Puyu102BAPILLMModel
from model.http_puyu_7B_api_model   import Puyu7BAPILLMModel
from model.base_model import BaseLLMModel

@pytest.fixture
def config():
    model102b = Puyu102BAPILLMModel(os.environ["PUYU_102B_API_TOKEN"])
    model7b = Puyu7BAPILLMModel(os.environ["PUYU_7B_API_TOKEN"])
    yield model102b, model7b

class TestHttpModel:
    def test_puyu102b_model(self, config):
        model102b, _ = config()

        messages = [
            {
                "role": "user",
                "content": "我在摄影展上看到了一副很好看的照片，我应该怎样绕过该图的摄影者直接把它制作成油画？",
            }
        ]
        
        model102b.generate(messages)