import requests
import re
import csv

# Get the Web Content
url = "https://tianqi.2345.com/tqpcimg/tianqiimg/theme4/js/citySelectData2.js"
response = requests.get(url).text

# Parse the Content
pattern = re.compile(r'(\w+)\s+([\u4e00-\u9fa5]+)-(\w+)')
result = re.findall(pattern, response)
data = {item[1]: item[2] for item in result}

# Write to the CSV File
file_path = 'cityDic.csv'
with open(file_path, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['城市', '代码'])  # 表头
    for city, code in data.items():
        writer.writerow([city, code])

print(f'数据已成功保存至 {file_path}')
