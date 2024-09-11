import requests
import json
from tqdm import tqdm
import time
import os

from loguru import logger

from celery import Celery
import requests
import json

from celery import Celery, group
from celery.signals import task_postrun
import requests
import json
from loguru import logger

from post_url_task import puyu_qa_query, critic_query, multi_lora_post_url, gpt4_critic_post_url
from auto_table import auto_table
import pandas as pd

import glob

from model.http_puyuapi_model import PuyuAPI
from model.http_taptapapi_model import TaptapAPI
from model.http_infiniapi_model import InfiniAPI
from model.http_bilibiliapi_model import BilibiliAPI
from model.http_eastmoneyapi_model import EastMoneyAPI
from model.http_jiaanapi_model import JiaanAPI
from model.http_wangyifuxiapi_model import WangyifuxiAPI
from model.http_baiduapi_model import BaiduAPI
from model.http_xiaohongshuapi_model import XiaohongshuAPI
from model.http_ruyiapi_model import RuyiAPI
from model.http_infiniapi_model import InfiniAPI
from model.http_icekreditapi_model import IcekreditAPI
from model.http_caiyueapi_model import CaiyueAPI
from model.http_shuwenapi_model import ShuwenAPI
from model.http_mihoyoapi_model import MihoyoAPI
from model.http_langchaoapi_model import LangchaoAPI
from model.http_zhumengdaoapi_model import ZhumengdaoAPI
from model.http_hehetianjiapi_model import HehetianjiAPI
from model.http_aishiapi_model import AishiAPI
from model.http_fanweixiaoeapi_model import FanweixiaoeAPI
from model.http_ximalayaapi_model import XimalayaAPI
from model.http_hantaoapi_model import HantaoAPI
from model.http_rockapi_model import RockAPI
from model.http_ccsmecapi_model import CcsmecAPI
from model.http_shaueapi_model import ShaueAPI
from model.http_kezhiapi_model import KezhiAPI
from model.http_guomaiapi_model import GuomaiAPI
from model.http_miliapi_model import MiliAPI
from model.http_yoocarapi_model import YoocarAPI
from model.http_paradigmapi_model import ParadigmAPI
from model.http_ailinapi_model import AilinAPI
from model.http_zhuofanapi_model import ZhuofanAPI

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

from celery import Celery, chain
import requests
from dataset.dataset import QARecord
from typing import List

app = Celery('tasks', broker='redis://localhost:6379/0', backend='redis://localhost:6379/0')

def qa(records: List[QARecord], cls_name) -> QARecord:
    # 创建任务列表
    tasks = [multi_lora_post_url.s(data = data.question, cls_name = cls_name).set(priority=5) for data in records.values()]
    
    # 使用 Celery 的 group 功能并行调度任务
    task_group = group(tasks)
    results = task_group.apply_async()

    # 收集结果
    answers = results.get()
    for (record, answer) in zip(records.values(), answers):
        record.answer = answer
    return records

def gpt4_critic(records: List[QARecord]) -> QARecord:
    # 创建任务列表
    tasks = [gpt4_critic_post_url.s({'question': data.question, 'answer': data.answer, 'model_cate': data.model_cate,'sample_cate': data.sheet_name}).set(priority=5) for data in records.values()]
    
    # 使用 Celery 的 group 功能并行调度任务
    task_group = group(tasks)
    results = task_group.apply_async()

    # 收集结果
    responses_json =  results.get()
    for (record, response) in zip(records.values(), responses_json):
        logger.debug(response)
        response = json.loads(response)
        record.critic = response
        record.reason = ""
    return records

def critic(records: List[QARecord]) -> QARecord:
    # 创建任务列表
    tasks = [critic_query.s({'question': data.question, 'answer': data.answer, 'model_cate': data.model_cate,'sample_cate': data.sheet_name}).set(priority=5) for data in records.values()]
    
    # 使用 Celery 的 group 功能并行调度任务
    task_group = group(tasks)
    results = task_group.apply_async()

    # 收集结果
    responses_json =  results.get()
    for (record, response) in zip(records.values(), responses_json):
        logger.debug(response)
        response = json.loads(response)
        record.critic = response['score']
        record.reason = response['reason']
    return records

def multi_lora_qa(records: List[QARecord], cls_name) -> QARecord:
    # 创建任务列表
    tasks = [multi_lora_post_url.s(data = data.question, cls_name = cls_name).set(priority=5) for data in records.values()]
    
    # 使用 Celery 的 group 功能并行调度任务
    task_group = group(tasks)
    results = task_group.apply_async()
    # 收集结果
    answers = results.get()
    for (record, answer) in zip(records.values(), answers):
        record.answer = answer
    return records
    
def multi_lora():
    model_cls = ZhuofanAPI
    model = model_cls.__name__

    # 检查文件夹是否存在
    if not os.path.exists(f"./file/res/{model}"):
        # 如果不存在,则创建文件夹
        os.makedirs(f"./file/res/{model}")
        print(f"已创建文件夹: {model}")
    else:
        print(f"文件夹 {model} 已存在, 不需要再次创建。")
    
    # TODO 针对不同任务更改待测文件
    # folder_path = '/Users/mac/Documents/pjlab/评测需求/puan/file/1-2月测试题'
    # folder_path = '/Users/mac/Documents/pjlab/评测需求/puan/file/64_office'
    # folder_path = "/Users/mac/Documents/pjlab/评测需求/puan/file/第六轮+64/第六批/4.0"
    # folder_path = "/Users/mac/Documents/pjlab/评测需求/puan/file/第六轮+64/第六批专项"
    folder_path = "/Users/mac/Documents/pjlab/评测题目/第八批/文生文4.1"
    # folder_path = "/Users/mac/Documents/pjlab/评测题目/7.8_4.0"
    # 使用 glob.glob() 获取所有 .xlsx 文件,并排除隐藏文件和 Microsoft Office 临时文件
    file_paths = [f for f in glob.glob(os.path.join(folder_path, '*.xlsx')) 
                if not os.path.basename(f).startswith('.') 
                and not os.path.basename(f).startswith('~$')]


    # 遍历所有找到的文件
    for file_path in file_paths:
        # 获取文件名，不包括路径
        base_name = os.path.basename(file_path)
        # 分割文件名和扩展名
        file_name, _ = os.path.splitext(base_name)
        records = QARecord.read_excel(file_path)
        qa_records = multi_lora_qa(records, model)
        # 检查文件夹是否存在
        if not os.path.exists(f"./file/res/{model}/{file_name}"):
            # 如果不存在,则创建文件夹
            os.makedirs(f"./file/res/{model}/{file_name}")
            print(f"已创建文件夹: {model}/{file_name}")
        else:
            print(f"文件夹 {model}/{file_name} 已存在, 不需要再次创建。")

        QARecord.write_dict_list_to_excel(qa_records, f"./file/res/{model}/{file_name}/qa_records_{model}.xlsx")
        
        critic_records = critic(qa_records)
        QARecord.write_dict_list_to_excel(critic_records, f"./file/res/{model}/{file_name}/critic_records_{model}.xlsx")
        
        # 读取 Excel 文件
        excel_path = f"./file/res/{model}/{file_name}/critic_records_{model}.xlsx"
        all_sheets = pd.read_excel(excel_path, sheet_name=None)

        # 处理数据
        results_df = auto_table(all_sheets)

        # 将结果写入新的 Excel 文件
        output_path = f'./file/res/{model}/{file_name}/result_summary_{model}.xlsx'
        results_df.to_excel(output_path, index=True)

if __name__ == '__main__':
    multi_lora()