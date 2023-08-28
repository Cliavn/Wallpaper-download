import os
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm


def extract_domain(url1):
    parsed_url = urlparse(url1)
    domain = parsed_url.netloc
    return domain


class RunMain:
    def __init__(self, root_url):
        self.urls_list = []
        self.root_url = root_url
        self.turning = None
        self.get_img_timeout = []

    def get_img(self, img_url):
        global re
        try:
            re = requests.get(img_url, timeout=10)
        except:
            print("获取img连接超时")
            self.get_img_timeout.append(img_url)
        soup = BeautifulSoup(re.text, "html.parser")
        find = soup.find(id="wallpaper")
        result = find['src']
        soup.clear()
        re.close()
        return result

    @staticmethod
    def auto_page_turning(soup):
        if soup.find(class_="next"):
            return soup.find(class_="next")['href']
        else:
            return False

    def get_pages(self, page_url):
        global re
        try:
            re = requests.get(page_url, timeout=10)
        except:
            print("访问网站连接超时")
        print(page_url, "====", re.status_code)
        html = re.text

        soup = BeautifulSoup(html, "html.parser")
        self.turning = self.auto_page_turning(soup)
        previews = soup.find_all(class_="preview")
        for preview in previews:
            self.urls_list.append(preview['href'])
        soup.clear()
        re.close()

    @staticmethod
    def new_folder(folder_path):
        if not os.path.exists(folder_path):
            os.mkdir(folder_path)
            print(f"文件夹 {folder_path} 创建成功！")
        else:
            # print(f"文件夹 {folder_path} 已经存在。")
            pass

    def run(self):
        self.get_pages(self.root_url)
        while self.turning:
            next_url = self.turning
            self.get_pages(next_url)
            domain_name = extract_domain(self.root_url)
            self.new_folder(rf'F:\爬虫\爬取动漫图片\动漫图片\{domain_name}')
            t = tqdm(self.urls_list)
            for i in t:
                img_url = self.get_img(i)
                filename = img_url.rsplit("/", 1)[-1]
                jpg = rf'F:\爬虫\爬取动漫图片\动漫图片\{domain_name}\{filename}'
                if os.path.isfile(jpg):
                    # print(jpg.rsplit("/", 1)[-1], "已存在")
                    continue

                response = requests.get(url)
                response.raise_for_status()
                with open(jpg, "wb") as file:
                    file.write(response.content)
                t.set_description(f"{img_url, filename}")

            self.urls_list = []
        print(f"获取img连接超时,{self.get_img_timeout}")


if __name__ == '__main__':
    url = input("请输入你要下载的网站:")
    RunMain(url).run()
