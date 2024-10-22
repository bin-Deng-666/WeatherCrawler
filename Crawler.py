import requests
import csv
from bs4 import BeautifulSoup
import json


def read_csv_to_dict(file_path):
    data = {}
    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            city = row['城市']
            code = row['代码']
            data[city] = code
    return data

# Build the Request and File Path
headers = {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "Referer": "https://tianqi.2345.com/wea_history",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Safari/605.1.15 Edg/130.0.0.0",
    "X-Requested-With": "XMLHttpRequest",
}
url = "https://tianqi.2345.com/Pc/GetHistory"
cityDic_path = 'cityDic.csv'

# Write the Information which You Wanna Crawl
city = "北京"
year = 2024
month = 10

# Read the City Dictionary
cityDic = read_csv_to_dict(cityDic_path)
params = {
    "areaInfo[areaId]": cityDic[city],
    "areaInfo[areaType]": 2,
    "date[year]": year,
    "date[month]": month,
}

# Get the Response from the URL
response = requests.get(url, params=params, headers=headers).text
data = json.loads(response)
html_content = data['data']

# Parse the HTML Content
soup = BeautifulSoup(html_content, 'html.parser')
rows = soup.find('table').find_all('tr')
data = []
for row in rows:
    cols = row.find_all('td')
    cols = [ele.text.strip() for ele in cols]
    data.append([ele for ele in cols if ele])

# Write to the File
file_path = "{city}_{year}_{month}.csv".format(city=city, year=year, month=month)
with open(file_path, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['日期', '最高温度', '最低温度', '天气', '风向', '空气质量'])
    writer.writerows(data)
print(f'数据已成功保存至 {file_path}')