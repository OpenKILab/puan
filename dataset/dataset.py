import json
from typing import List, Dict, Union, Optional, TypeVar, Tuple

import pandas as pd
import uuid
import os

import csv
import re

from loguru import logger

# 安全种类评分
category_map = {
    '1': 'politics',
    '2': 'bias',
    '3': 'finance',
    '4': 'violation',
    '5': 'special_service',
    '6': 'to_refuse',
    '7': 'not_refuse',
    '8': 'diversity'
}

class ID(str):
    def __new__(cls):
        return super().__new__(cls, uuid.uuid4())

class QARecord():
    sheet_name: Optional[str] = None # 问答属于数据集的哪个分页子集
    question: str
    answer: Optional[str] = None
    critic: Optional[str] = None  # critic模型的评测结果
    reason: Optional[str] = None    # critic模型的评测理由
    annotation: Optional[str] = None  # QARecord对应的人工标注结果
    model_cate: Optional[str] = None # puan model api 所需字段, 用于单个api内调用不同模型
    
    qa_records: Optional[
        Dict[str, "QARecord"]
    ] = None  # key是每条QARecord的唯一id, 也是Dataset类中的实际内容存储
    
    def __init__(self, sheet_name: str, question: str, answer: str, model_cate: str):
        self.sheet_name = sheet_name
        self.question = question
        self.answer = answer
        self.model_cate = model_cate
        
    @staticmethod
    def read_excel(filename: str) -> Tuple[Dict[str, "QARecord"], List[str]]:
        index = QARecord.extract_number_from_filename(filename)
        if index < '1' or index > '8':
            index = '2'
        category = category_map[index]
        qa_records = {}
        xls = pd.ExcelFile(filename)
        # Loop through all the sheets
        for sheet_name in xls.sheet_names:
            # Read the sheet into a DataFrame
            df = pd.read_excel(xls, sheet_name=sheet_name)
            for index, row in df.iterrows():
                question_str = str(row[0])
                answer_str = str(row[1]) if len(row) > 1 else ''
                qa_records[ID()] = QARecord(
                    sheet_name=sheet_name,
                    question=question_str,
                    answer=answer_str,
                    model_cate = category
                )
            # key = df.keys()[0]  ### change for complex
            ####### change togather ####
        return qa_records
    
    @staticmethod
    def write_dict_list_to_excel(qa_records: Dict[str, "QARecord"], filename: str):
        # 创建一个Excel写入器
        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            # 按sheet_name分组QA记录
            grouped_records = QARecord.group_by_sheet_name(qa_records)
            
            # 遍历分组记录
            for sheet_name, records in grouped_records.items():
                # 将QA记录转换为DataFrame
                data = {
                    'Question': [record.question for record in records],
                    'Answer': [record.answer for record in records],
                    'Critic': [record.critic for record in records],
                    'Reason': [record.reason for record in records],
                    'Annotation': [record.annotation for record in records]
                }
                df = pd.DataFrame(data)
                
                # 写入到指定的sheet
                df.to_excel(writer, sheet_name=sheet_name, index=False)
    
    @staticmethod
    def group_by_sheet_name(qa_records: Dict[str, "QARecord"]) -> Dict[str, list]:
        grouped_records = {}
        for record in qa_records.values():
            sheet_name = record.sheet_name or 'Default'
            if sheet_name not in grouped_records:
                grouped_records[sheet_name] = []
            grouped_records[sheet_name].append(record)
        return grouped_records
    
    @staticmethod
    def extract_number_from_filename(path: str) -> str:
        # 从完整路径中提取文件名
        filename = os.path.basename(path)
        # 正则表达式搜索文件名中的第一组数字
        match = re.search(r'\d+', filename)
        if match:
            return match.group(0)  # 返回匹配的第一个结果
        return '1' # 默认 politics
    
    @staticmethod
    def read_json(file_path: str) -> Tuple[Dict[str, "QARecord"], List[str]]:
        qa_records = {}
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                try:
                    item = json.loads(line.strip())
                    qa_records[ID()] = QARecord(
                        question=item.get("question"),
                        answer=item.get("answer"),
                        model_cate=item.get("model_cate"),
                        sheet_name=""
                    )
                except json.JSONDecodeError as e:
                    logger.error(f"Error decoding JSON: {e}")
        return qa_records









################################################################

class SummerQARecord():
    sheet_name: Optional[str] = None # 问答属于数据集的哪个分页子集
    question: str
    answer: Optional[str] = None
    critic: Optional[str] = None  # critic模型的评测结果
    reason: Optional[str] = None    # critic模型的评测理由
    annotation: Optional[str] = None  # SummerQARecord
    model_cate: Optional[str] = None # puan model api 所需字段, 用于单个api内调用不同模型
    
    qa_records: Optional[
        Dict[str, "SummerQARecord"]
    ] = None  # key是每条SummerQARecord的唯一id, 也是Dataset类中的实际内容存储
    
    modified_prompt: str
    response: Optional[str] = None
    score: Optional[str] = None
    raw_prompt: Optional[str] = None
    
    def __init__(self, sheet_name: str, question: str, answer: str, model_cate: str):
        self.sheet_name = sheet_name
        self.question = question
        self.answer = answer
        self.model_cate = model_cate
        
    def __init__(self,sheet_name: str, modified_prompt: str, raw_prompt: str):
        self.modified_prompt = modified_prompt
        self.raw_prompt = raw_prompt
        
    @staticmethod
    def read_excel(filename: str) -> Tuple[Dict[str, "SummerQARecord"], List[str]]:
        qa_records = {}
        xls = pd.ExcelFile(filename)
        # Loop through all the sheets
        for sheet_name in xls.sheet_names:
            # Read the sheet into a DataFrame
            df = pd.read_excel(xls, sheet_name=sheet_name)
            for index, row in df.iterrows():
                modified_prompt = str(row[0])
                raw_prompt = str(row[3])
                qa_records[ID()] = SummerQARecord(
                    sheet_name=sheet_name,
                    modified_prompt=modified_prompt,
                    raw_prompt=raw_prompt,
                )
            # key = df.keys()[0]  ### change for complex
            ####### change togather ####
        return qa_records
    
    @staticmethod
    def write_dict_list_to_excel(qa_records: Dict[str, "SummerQARecord"], filename: str):
        # 创建一个Excel写入器
        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            # 按sheet_name分组QA记录
            grouped_records = SummerQARecord.group_by_sheet_name(qa_records)
            
            # 遍历分组记录
            for sheet_name, records in grouped_records.items():
                # 将QA记录转换为DataFrame
                data = {
                    'modified_prompt': [record.modified_prompt for record in records],
                    'response': [record.response for record in records],
                    'score': [record.score for record in records],
                    'raw_prompt': [record.raw_prompt for record in records],
                }
                df = pd.DataFrame(data)
                
                # 写入到指定的sheet
                df.to_excel(writer, sheet_name=sheet_name, index=False)
    
    @staticmethod
    def group_by_sheet_name(qa_records: Dict[str, "SummerQARecord"]) -> Dict[str, list]:
        grouped_records = {}
        for record in qa_records.values():
            sheet_name = record.sheet_name or 'Default'
            if sheet_name not in grouped_records:
                grouped_records[sheet_name] = []
            grouped_records[sheet_name].append(record)
        return grouped_records
    
    @staticmethod
    def extract_number_from_filename(path: str) -> str:
        # 从完整路径中提取文件名
        filename = os.path.basename(path)
        # 正则表达式搜索文件名中的第一组数字
        match = re.search(r'\d+', filename)
        if match:
            return match.group(0)  # 返回匹配的第一个结果
        return '1' # 默认 politics


