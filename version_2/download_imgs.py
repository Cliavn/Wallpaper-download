import json
import os.path
from datetime import datetime

import requests
from tqdm import tqdm

from version_2.tools import extract_domain


def read_json(path, kay):
    result = []
    with open(path, 'r') as file:
        wallhaven_json = json.load(file)
    for page, imgs in dict(wallhaven_json).items():
        if 'http' in page:
            page_list = []
            for img, value in dict(imgs).items():
                if value == kay:
                    page_list.append(img)
            page_dist = {page: page_list}
            result.append(page_dist)
    return result


# 更新JSON数据
def renewal_json(page, img_url):
    path = 'wallhaven.cc.json'
    # 读取 JSON 文件并解析为 Python 对象
    with open(path, 'r') as file:
        data = json.load(file)

    # 更新 Python 对象中的数据
    data[str(page)][img_url] = "1"
    pass
    # 将更新后的 Python 对象转换为 JSON 格式
    updated_json = json.dumps(data, indent=4)

    # 将更新后的 JSON 数据写入到 JSON 文件中
    with open(path, 'w') as file:
        file.write(updated_json)


def down_img(img_urls):
    key1 = list(img_urls[0].keys())[0]
    path = extract_domain(key1)
    if not os.path.isdir(path):
        os.mkdir(path)
    for page in img_urls:
        for key, value in page.items():
            t = tqdm(value)
            for img_url in t:
                file_name = str(img_url).rsplit("/", 1)[-1]
                response = requests.get(img_url)
                with open(f"{path}/{file_name}", "wb") as file:
                    file.write(response.content)
                now_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                t.set_description(f"{now_time, key, img_url, response.status_code}")
                renewal_json(key, img_url)


if __name__ == '__main__':
    # 获取imgs 列表
    imgs_list = read_json('wallhaven.cc.json', '0')
    # print(imgs_list)

    # 下载列表中的img
    down_img(imgs_list)
