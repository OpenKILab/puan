# test_dataset.py

import pytest
import json
from unittest.mock import mock_open, patch
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from dataset.dataset import QARecord

def test_parse_qa_records():
    # Mock JSON data
    mock_json_data = json.dumps([
        {
            "question": "What is the capital of France?",
            "answer": "Paris",
            "label": 1,
            "model_cate": "geography"
        },
        {
            "question": "Who wrote '1984'?",
            "answer": "George Orwell",
            "label": 1,
            "model_cate": "literature"
        }
    ])

    # Use patch to mock open function
    with patch("builtins.open", mock_open(read_data=mock_json_data)):
        # Call the function to test
        result = QARecord.read_json("mock_file_path.json")

        # Define expected result
        expected = [
            QARecord(question="What is the capital of France?", answer="Paris", model_cate="geography", sheet_name = ""),
            QARecord(question="Who wrote '1984'?", answer="George Orwell", model_cate="literature", sheet_name = "")
        ]

        # Assert the result matches the expected output
        for r, e in zip(result, expected):
            assert r.question == e.question
            assert r.answer == e.answer
            assert r.model_cate == e.model_cate