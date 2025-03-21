import pandas as pd
from typing import Type, Dict
from pandas import DataFrame

import json
from datetime import datetime
from io import BytesIO
from urllib.parse import quote

import pandas as pd
from typing import Type, Dict
from pandas import DataFrame

from loguru import logger

def auto_table(excel_df: Dict[str, DataFrame]) -> DataFrame:

    # Initialize dictionaries to store results
    sheet_results = {}
    overall_results = {'总题数': 0, 1: 0, 2: 0, 3: 0, 4: 0}

    # Process each sheet
    for sheet_name in excel_df.keys():
        df = excel_df[sheet_name]
        # Assuming the column with audit results is named '审核结果'
        if '审核结果' in df.columns:
            results = df['审核结果'].value_counts()
            total = results.sum()
            qualified = results.get(3, 0) + results.get(4, 0)
            qualified_rate = str(round((qualified / total)*100,2))+'%' if total else 0

            # Store results for each sheet
            sheet_results[sheet_name] = {
                '合格率': qualified_rate,
                1: results.get(1, 0),#results.get(1, 0)/total,
                2: results.get(2, 0),#results.get(2, 0)/total,
                3: results.get(3, 0),#results.get(3, 0)/total,
                4: results.get(4, 0),#results.get(4, 0)/total
                '总题数': total,
            }

            # Update overall results
            overall_results['总题数'] += total
            for i in range(1, 5):
                overall_results[i] += results.get(i, 0)
  
    # Calculate overall qualifi
    # ed rate
    overall_qualified = overall_results[3] + overall_results[4]
    overall_results['合格率'] = str(round((overall_qualified / overall_results['总题数'])*100,2))+'%' if overall_results['总题数'] else 0
    # 设置输出为百分比
    # for i in range(1, 5):
    #     overall_results[i] /= overall_results['总题数']
        
    # Creating a DataFrame to store all the results in a single sheet
    results_df = pd.DataFrame()


    # Adding each sheet's results
    for sheet_name, result in sheet_results.items():
        temp_df = pd.DataFrame([result])
        temp_df.index = [sheet_name]
        results_df = pd.concat((results_df,temp_df))

    # Adding overall results to the DataFrame
    overall_df = pd.DataFrame([overall_results])
    overall_df.index = ['整体结果']
    results_df = pd.concat((results_df,overall_df))
    # Reordering columns for better readability
    # results_df = results_df[['总题数', 1, 2, 3, 4, '合格率']]
    # 设置输出为百分比
    # results_df = results_df.rename(columns={i: f"{i}（%）" for i in range(1, 5)})
    # for col in ['1（%）', '2（%）', '3（%）', '4（%）', '合格率']:
    #     results_df[col] = results_df[col] * 100
    # results_df['合格率'] = results_df['合格率'] * 100
    

    return results_df


filename = "./file/2月1违反社会主义核心价值观+puyu102B+问答记录.xlsx"
with open(filename, 'rb') as file:
    pd_file = file.read()
csv_data = pd.read_excel(BytesIO(pd_file), na_values="null", sheet_name=None)
result_df = auto_table(csv_data)
with pd.ExcelWriter("./file/res/table_result.xlsx") as writer:
    result_df.to_excel(writer)