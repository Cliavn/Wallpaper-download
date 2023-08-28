from tqdm import tqdm

from version_2.tools import analysis


class Run:
    # 数据初始化
    def __init__(self, url):
        self.main_url = url
        self.page_url = []
        self.img_url = []
        self.Lose_page_url = []
        self.Lose_img_url = []

    # 启动
    def run(self, xpath1, xpath2):
        # 解析一页中的page href
        page_url = analysis(self.main_url, xpath1)
        if page_url == self.main_url:
            self.Lose_page_url.append(page_url)
        else:
            self.page_url = page_url
        # print("=========页面中的page========\n", self.page_url)

        # 解析page中的img href
        print(f"---------------{self.main_url}中的img href解析中---------------")
        t = tqdm(self.page_url)
        for page in t:
            img = analysis(page, xpath2)
            if img == page:
                self.Lose_img_url.append(img)
            else:
                self.img_url.append(img)
            t.set_description(page.rsplit("/", 1)[-1], page)
        filtered_list = list(filter(None, self.img_url))
        self.img_url = filtered_list
        print(f"---------------{self.main_url}中的img href解析完成---------------")

        print("=========page中的img========\n", self.img_url)


if __name__ == '__main__':
    main_url = "https://wallhaven.cc/latest?page=30"
    pages_xpath = '//figure//@href'
    img_xpath = '//img[@id="wallpaper"]/@src'
    Run(main_url).run(pages_xpath, img_xpath)
