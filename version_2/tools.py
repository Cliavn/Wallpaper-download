import requests
from lxml import etree


#   获取html 源码
def source(url):
    re = requests.get(url, timeout=10)
    if re.status_code in (443, 410):
        return False
    return re.text


#   xpath解析
def analysis(url, xpath):
    html = source(url)
    if html is False:
        return url
    tree = etree.HTML(html)
    elements = tree.xpath(xpath)
    return elements
