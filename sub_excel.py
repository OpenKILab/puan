import os
import pandas as pd

def split_excel_sheets(input_directory, output_directory, max_rows_per_file=10):
    # 确保输出目录存在
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # 遍历输入目录下的所有文件
    for filename in os.listdir(input_directory):
        if filename.endswith('.xlsx'):
            file_path = os.path.join(input_directory, filename)
            # 读取 Excel 文件
            excel_file = pd.ExcelFile(file_path)
            
            # 遍历每个子表
            for sheet_name in excel_file.sheet_names:
                # 读取子表
                df = pd.read_excel(file_path, sheet_name=sheet_name)
                
                # 计算需要多少个文件
                num_files = (len(df) + max_rows_per_file - 1) // max_rows_per_file
                
                for i in range(num_files):
                    # 获取当前文件的行范围
                    start_row = i * max_rows_per_file
                    end_row = min((i + 1) * max_rows_per_file, len(df))
                    
                    # 切片数据框
                    df_slice = df.iloc[start_row:end_row]
                    
                    # 创建新的文件名
                    new_filename = f"{os.path.splitext(filename)[0]}_{sheet_name}_part{i+1}.xlsx"
                    new_file_path = os.path.join(output_directory, new_filename)
                    
                    # 保存子表到新的 Excel 文件
                    df_slice.to_excel(new_file_path, index=False)
                    print(f"Saved {new_file_path}")

# 使用示例
input_directory = "/Users/mac/Documents/pjlab/评测需求/wanxiang/text_moral_ethics_qa"
output_directory = "/Users/mac/Documents/pjlab/评测需求/wanxiang/sub"
split_excel_sheets(input_directory, output_directory)