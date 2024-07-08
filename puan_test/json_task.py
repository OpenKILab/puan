import json
import time
import os
from celery import Celery, group
from tqdm import tqdm

from post_url_task import post_url
from loguru import logger

import redis

app = Celery('tasks', broker='redis://localhost:6379/0', backend='redis://localhost:6379/0')

redis_client = redis.Redis(host='localhost', port=6379, db=0)
redis_client.set("pause_tasks", "False")

def read_json_lines(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            yield json.loads(line.strip())

def write_json(data, file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

# def fetch_data_and_process(json_input_path, json_output_path):
#     data_list = read_json_lines(json_input_path)
#     results = []
#     for data in data_list:
#         while True:
#             logger.info(data)
#             result = post_url.delay('http://10.140.0.184:22222', data)
#             while not result.ready():
#                 time.sleep(0.25)  # 等待任务完成或失败
#             result_value = result.get()
#             if result_value == "Blocked by retrying task.":
#                 time.sleep(10)  # 如果任务被阻塞，等待10秒后再次尝试
#                 continue  # 重新尝试当前任务
#             results.append(result_value)
#             break  # 成功完成任务后跳出循环

#     write_json(results, json_output_path)

def fetch_data_and_process(json_input_path, json_output_path):
    data_list = read_json_lines(json_input_path)
    
    # 创建任务列表
    tasks = [post_url.s('http://10.140.0.184:22222', data).set(priority=5) for data in data_list]
    
    # 使用 Celery 的 group 功能并行调度任务
    task_group = group(tasks)
    results = task_group.apply_async()

    # 收集结果
    output_results = results.get()

    # 写入结果到 JSON 文件
    write_json(output_results, json_output_path)

def process_all_files(input_dir, output_dir):
    files = [f for f in os.listdir(input_dir) if f.endswith('.json')]
    start_time = time.time()
    with tqdm(total=len(files), desc="Processing files", unit="file") as pbar:
        for filename in files:
            input_file = os.path.join(input_dir, filename)
            output_file = os.path.join(output_dir, filename)
            fetch_data_and_process(input_file, output_file)
            pbar.update(1)
    elapsed_time = time.time() - start_time
    print(f"All tasks completed in {elapsed_time:.2f} seconds")

if __name__ == "__main__":
    input_dir = './multi_lora_50'
    output_dir = './processed_responses'
    os.makedirs(output_dir, exist_ok=True)  # 确保输出目录存在
    process_all_files(input_dir, output_dir)
