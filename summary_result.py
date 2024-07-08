import os
import pandas as pd

# 定义根目录
root_dir = './file/res/InternLM-2_5_7B/'

# 目标文件名
target_file = 'result_summary_InternLM-2_5_7B.xlsx'

# 创建一个空的DataFrame来存储合并的数据
merged_df = pd.DataFrame()

# 遍历每个文件夹并合并数据
for folder in os.listdir(root_dir):
    folder_path = os.path.join(root_dir, folder)
    if os.path.isdir(folder_path):
        file_path = os.path.join(folder_path, target_file)
        if os.path.exists(file_path):
            df = pd.read_excel(file_path)
            merged_df = pd.concat([merged_df, df], ignore_index=True)

# 将合并的数据保存到一个新的Excel文件
output_path = root_dir + 'merged_result_summary_InternLM-2_5_7B.xlsx'
merged_df.to_excel(output_path, index=False)

print(f"合并后的结果保存到 {output_path}")

import pandas as pd
import os

root_dir = './file/res/InternLM-2_5_7B/'
# 定义数据目录和文件
directories = [
    "1、违反社会公德和中华民族优秀文化传统",
    "2、歧视",
    "3、商业违法违规",
    "4、侵害他人合法权益",
    "5、无法满足客户安全需求",
    "6、模型应拒答的问题",
    "7、不应该拒答问题"
]
file_name = "result_summary_InternLM-2_5_7B.xlsx"
output_file = "merged_result_summary.xlsx"

# 初始化一个空的 DataFrame 列表
all_data = []

# 遍历目录并读取 Excel 文件
for directory in directories:
    file_path = os.path.join(root_dir + directory, file_name)
    if os.path.exists(file_path):
        df = pd.read_excel(file_path)
        all_data.append(df)

# 合并所有 DataFrame
merged_df = pd.concat(all_data, ignore_index=True)

# 将合并后的数据写入新的 Excel 文件
merged_df.to_excel(root_dir + output_file, index=False)

print(f"Merged data saved to {output_file}")
