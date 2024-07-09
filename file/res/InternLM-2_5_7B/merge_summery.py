
import pandas as pd

# 定义文件路径列表
file_paths = [
    '/Users/mac/Documents/pjlab/repo/puan/file/res/InternLM-2_5_7B/1、违反社会主义核心价值观/result_summary_InternLM-2_5_7B.xlsx',
    '/Users/mac/Documents/pjlab/repo/puan/file/res/InternLM-2_5_7B/2、歧视/result_summary_InternLM-2_5_7B.xlsx',
    '/Users/mac/Documents/pjlab/repo/puan/file/res/InternLM-2_5_7B/3、商业违法违规/result_summary_InternLM-2_5_7B.xlsx',
    '/Users/mac/Documents/pjlab/repo/puan/file/res/InternLM-2_5_7B/4、侵害他人合法权益/result_summary_InternLM-2_5_7B.xlsx',
    '/Users/mac/Documents/pjlab/repo/puan/file/res/InternLM-2_5_7B/5、无法满足特定服务类型的安全需求/result_summary_InternLM-2_5_7B.xlsx',
    '/Users/mac/Documents/pjlab/repo/puan/file/res/InternLM-2_5_7B/6、模型应拒答的问题/result_summary_InternLM-2_5_7B.xlsx',
    '/Users/mac/Documents/pjlab/repo/puan/file/res/InternLM-2_5_7B/7、不应该拒答问题/result_summary_InternLM-2_5_7B.xlsx'
]

# 读取和处理每个文件
dataframes = []
for i, file_path in enumerate(file_paths, start=1):
    df = pd.read_excel(file_path)
        # 分割路径并进行检查
    path_parts = file_path.split('/')
    if len(path_parts) > 2:
        directory_with_description = path_parts[-2]
        if '、' in directory_with_description:
            file_description = directory_with_description.split('、')[1]
        else:
            file_description = "Description Not Found"
    else:
        file_description = "Invalid Path Structure"

    # 在每个DataFrame的开头添加文件名行
    filename_row = pd.DataFrame([['' + str(i) + '、' + file_description] + [None] * (df.columns.size - 1)], columns=df.columns)
    df = pd.concat([filename_row, df], ignore_index=True)
    dataframes.append(df)

# 合并所有DataFrame
combined_df = pd.concat(dataframes, ignore_index=True)

# 计算总体汇总
numeric_columns = combined_df.columns[2:]  # 假设数值列从第三列开始
summary_rows = combined_df[combined_df['Unnamed: 0'].str.contains('整体结果', na=False)]
summary_totals = summary_rows[numeric_columns].sum()
total_summary_row = ['总体汇总'] + [None] + summary_totals.tolist()
combined_df.loc[len(combined_df)] = total_summary_row


output_path = './combined_output.xlsx'
combined_df.to_excel(output_path, index=False)

print(f'文件已保存到 {output_path}')
