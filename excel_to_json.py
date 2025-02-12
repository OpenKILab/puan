import pandas as pd
import json
import os
import glob

# Define the category map
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

def excel_to_json(excel_path, output_json_path):
    # Read the Excel file
    df = pd.read_excel(excel_path)

    # Extract the label from the file name
    file_name = os.path.basename(excel_path)
    label_number = file_name.split('、')[0]  # Assuming the label is the first number in the file name
    label = int(label_number) if label_number.isdigit() else 0
    model_cate = category_map.get(label_number, 'unknown')

    # Convert the DataFrame to a list of dictionaries
    records = df.to_dict(orient='records')

    # Create the JSON structure
    json_data = []
    for record in records:
        json_record = {
            "question": record.get("question", ""),
            "answer": record.get("answer", ""),
            "label": label,
            "model_cate": model_cate
        }
        json_data.append(json_record)

    # Write the JSON data to a file
    with open(output_json_path, 'w', encoding='utf-8') as json_file:
        for entry in json_data:
            json.dump(entry, json_file, ensure_ascii=False)
            json_file.write('\n')

    print(f"JSON file created at: {output_json_path}")

def process_folder(folder_path, output_folder):
    # Ensure the output folder exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Get all Excel files in the folder
    excel_files = glob.glob(os.path.join(folder_path, '*.xlsx'))

    for excel_file in excel_files:
        # Determine the output JSON file path
        base_name = os.path.basename(excel_file)
        json_file_name = os.path.splitext(base_name)[0] + '.json'
        output_json_path = os.path.join(output_folder, json_file_name)

        # Convert the Excel file to JSON
        excel_to_json(excel_file, output_json_path)

# Example usage
folder_path = '/Users/mac/Documents/pjlab/评测需求/wanxiang/text_moral_ethics_qa'
output_folder = '/Users/mac/Documents/pjlab/评测需求/wanxiang/json'
process_folder(folder_path, output_folder)