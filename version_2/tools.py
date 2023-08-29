import json
import os
from time import sleep
from urllib.parse import urlparse, urljoin

import requests
from lxml import etree


# 链接拼接
def link_splicing(base_url, relative_url):
    complete_url = relative_url
    if not 'http' in str(relative_url):
        complete_url = urljoin(base_url, relative_url)
    if '' == str(relative_url):
        complete_url = ''
    return complete_url


#   获取html 源码
def source(url):
    re = requests.get(url, timeout=10)
    # print(re.status_code)
    if not re.status_code == 200:
        print("\n", url, "链接获取源码失败,检测到反爬，等待10秒", re.status_code)
        sleep(10)
        source(url)
    return re.text


#   xpath解析
def analysis(url, xpath):
    url = str(url).replace("['", "").replace("']", "")
    try:
        html = source(url)
    except:
        print("\n", url, "html源码获取失败,检测到反爬，等待10秒")
        sleep(10)
        html = source(url)
    if html is False:
        return url
    tree = etree.HTML(html)
    elements = tree.xpath(xpath)
    return elements


# 判断 文件夹\文件 是否存在  不存在就立刻生成
def create_folder_if_not_exists(folder_path):
    data_json = f'{folder_path}.json'
    if not os.path.exists(data_json):
        with open(data_json, 'w') as file:
            json.dump({}, file)
    return data_json


# 提取域名
def extract_domain(url1):
    parsed_url = urlparse(url1)
    domain = parsed_url.netloc
    return domain


#   生成json文件
def get_json(old_main_url, main_url, img_url, file_name):
    main_url = str(main_url).replace("['", "").replace("']", "")
    # 生成JSON数据
    new_img_json = {}
    for img in img_url:
        img = link_splicing(old_main_url, img)
        if not '[]' in str(img):
            new_img_json[img] = '0'
    # print(new_img_json.keys())
    print(len(new_img_json))
    new = {str(main_url): new_img_json}

    # 判断文件是否存在
    if os.path.exists(file_name):
        # 如果文件存在，追加数据到已有的 JSON 文件
        with open(file_name, "r") as file:
            existing_data = json.load(file)
        existing_data.update(new)
    else:
        # 如果文件不存在，创建新的 JSON 文件
        existing_data = new

    # 合并json文件
    existing_data.update(new)
    #   写出JSON数据 为JSON文件
    with open(file_name, "w", encoding='utf-8') as outfile:
        json.dump(existing_data, outfile, indent=4, sort_keys=True)


if __name__ == '__main__':
    print(analysis(url='https://pic.netbian.com/index_16.html',
                   xpath='//div[@class="slist"]//@src'))
