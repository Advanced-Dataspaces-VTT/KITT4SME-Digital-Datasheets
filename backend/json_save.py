import os
import json
import requests
import pandas as pd

def download_json_files(base_url, filenames, save_directory):
    for filename in filenames:
        url = f"{base_url}/{filename}"
        response = requests.get(url)

        if response.status_code == 200:
            save_path = os.path.join(save_directory, filename)
            with open(save_path, 'wb') as file:
                file.write(response.content)
            print(f"File '{filename}' downloaded and saved successfully.")
        else:
            print(f"Failed to download file '{filename}'. Status code: {response.status_code}")

def read_json_files_to_dataframe(filenames, save_directory):
    rows = []
    for filename in filenames:
        json_path = os.path.join(save_directory, filename)
        with open(json_path, 'r') as json_file:
            data = json.load(json_file)
        rows.append(pd.json_normalize(data))  # Use json.load() to parse JSON data safely

    df = pd.concat(rows, ignore_index=True)
    return df

if __name__ == "__main__":
    base_url = "https://kitt4sme.collab-cloud.eu/datasheets-backend-rest/download-backup"
    filenames = [
        "datasheet_75.json",
        "datasheet_13.json",
        "datasheet_99.json",
        "datasheet_50.json",
        "datasheet_30.json",
        "datasheet_25.json",
        "datasheet_48.json",
        "datasheet_7.json",
        "datasheet_3.json",
        "datasheet_62.json",
        "datasheet_31.json",
        "datasheet_22.json",
        "datasheet_89.json",
        "datasheet_100.json",
        "datasheet_57.json",
    ]
    save_directory = "json_files"  # Replace with your desired save directory

    if not os.path.exists(save_directory):
        os.makedirs(save_directory)

    download_json_files(base_url, filenames, save_directory)

    df = read_json_files_to_dataframe(filenames, save_directory)

    excel_file_path = "json_data.xlsx"  # Replace with the desired Excel file path
    df.to_excel(excel_file_path, index=False)
    print("Data has been imported into Excel successfully.")
