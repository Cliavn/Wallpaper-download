from datetime import datetime

from tqdm import tqdm

from version_2.tools import *


class Run:
    # 数据初始化
    def __init__(self, xpath1, xpath2, xpath3):
        self.main_url = not None
        self.old_main_url = ''
        self.page_url = []
        self.img_url = []
        self.Lose_page_url = []
        self.Lose_img_url = []
        self.file_name = ''
        self.pages_xpath = xpath1  # 列表中壁纸详细页url定位 Xpath
        self.img_xpath = xpath2  # 壁纸详细页中图片url定位 Xpath
        self.next_xpath = xpath3  # 下一页按钮的url定位 Xpath

    # 启动
    def run(self, run_url):
        if self.old_main_url == '':
            self.old_main_url = run_url
        self.main_url = run_url

        # 判断文件保存位置的文件夹是否存在  返回文件名
        self.file_name = create_folder_if_not_exists(f"{extract_domain(main_url)}")

        # 读取当前JSON文件  用于检测当前解析url  是否已经被解析完成
        with open(self.file_name, "r") as file:
            existing_data = json.load(file)

        # 判断是否已经被解析完成
        if str(run_url) in existing_data:
            print(run_url, "-----已经解析完成，跳过当前url")
        else:
            # 解析一页中的page href
            page_url = analysis(self.main_url, self.pages_xpath)
            if not page_url:
                self.Lose_page_url.append(page_url)
            else:
                self.page_url = page_url

            # 解析page中的img href
            t = tqdm(self.page_url)
            for page in t:
                page = link_splicing(self.old_main_url, page)
                img = str(analysis(page, self.img_xpath))
                img = img.replace("['", "").replace("']", "")
                if 'png' in img:
                    self.img_url.append(img)
                elif 'jpg' in img:
                    self.img_url.append(img)
                else:
                    self.Lose_img_url.append(page)
                rsplit = img.rsplit(" / ", 1)[-1]
                time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                t.set_description(f"{time}, {self.main_url}, {rsplit}")
            # filtered_list = list(filter(None, self.img_url))
            # self.img_url = filtered_list

            # 将img下载地址 生成json文件 保存在当前文件夹 名为 “{当前网址的域名}.json”
            get_json(self.old_main_url, self.main_url, self.img_url, self.file_name)

            # 重置 self.img_url 列表
            self.img_url = []

        # 统计数据
        # print('失败的page', self.Lose_page_url)
        get_json(self.old_main_url, "fail_page", self.Lose_page_url, self.file_name)
        # print('失败的img', self.Lose_img_url)
        get_json(self.old_main_url, "fail_img", self.Lose_img_url, self.file_name)

        # 检测下一页按钮 存在则继续下载  不存在则结束程序
        next_main_url = analysis(self.main_url, self.next_xpath)
        next_main_url = link_splicing(self.old_main_url, next_main_url)
        if next_main_url:
            self.run(next_main_url)


if __name__ == '__main__':
    main_url = "https://wallhaven.cc/latest"  # 网址
    pages_xpath = '//figure//@href'  # 列表中壁纸详细页url定位 Xpath
    img_xpath = '//img[@id="wallpaper"]//@src'  # 壁纸详细页中图片url Xpath
    next_xpath = '//a[@class="next"]/@href'  # 下一页 url Xpath
    Run(pages_xpath, img_xpath, next_xpath).run(main_url)
