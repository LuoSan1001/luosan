import requests
import re
from lxml import etree
from bs4 import BeautifulSoup
import numpy as np
import os

# 相同文件重命名
def rename_duplicate(list, print_result=False):
    new_list=[v + str(list[:i].count(v) + 1) if list.count(v) > 1 else v for i, v in enumerate(list)]
    if print_result:
	    print("Renamed list:",new_list)
    return new_list

# 1 拿到所有的新闻网址
page = 1
page_content = ""
url_list2 = []
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36'
}
while page < 6:
    if page == 1:
        url = "https://sise.uestc.edu.cn/xwtz/tzgg/yb.htm"
    else:
        code = 6-page
        url = f"https://sise.uestc.edu.cn/xwtz/tzgg/yb/{code}.htm"
    resp = requests.get(url)
    resp.encoding = "UTF-8"
    # session = requests.Session()
    # resp = session.get(url=url, headers=headers).text.encode('latin1')
    page_content += resp.text
    # print(resp.text)

    obj1 = re.compile(r'/system/resource/js/ajax.js">(?P<news>.*?)<link rel="stylesheet" Content-type="text/css" ', re.S)
    result1 = obj1.finditer(page_content)
    # print(result1)
    for it in result1:
        news = it.group('news')
        # print(ul)
        if page == 1:
            obj2 = re.compile(r'<a href="../../(?P<url>.*?)">', re.S)
        else:
            obj2 = re.compile(r'<a href="../../../(?P<url>.*?)">', re.S)
        result2 = obj2.finditer(news)
        # print(result2)
        for itt in result2:
            url ='https://sise.uestc.edu.cn/' + itt.group('url')
            # print(url)
            url_list2.append(url)

    page += 1
    # 去重
    url_list = []
    for i in url_list2:
        if not i in url_list:
            url_list.append(i)

# 2 拿到标题，创建每个新闻对应的文件夹
titles = []
for r in url_list:
    # print(r)
    resp = requests.get(r)
    resp.encoding = "UTF-8"
    child_page_content = resp.text
    # print(child_page_content)
    obj3 = re.compile(r'<title>(?P<titles>.*?)-', re.S)
    result3 = obj3.finditer(child_page_content)

    for title in result3:
        title = title.group('titles')
        # print(title)
        titles.append(title)

renamed_titles = rename_duplicate(titles, False)

for tt in renamed_titles:
    # print(tt)
    os.mkdir(f'C:/Users/nllkj/Desktop/休对故人思故国/焦糖工作室招新/#5-赖子秋/任务一/{tt}')


# 3 爬取标题 文本 时间放入文件夹

code = 0
for r in url_list:
    # print(r)
    txt_path = f'C:/Users/nllkj/Desktop/休对故人思故国/焦糖工作室招新/#5-赖子秋/任务一/{renamed_titles[code]}/标题，时间，文本.txt'
    code += 1
    f = open(txt_path, 'a', encoding='utf-8')

    resp = requests.get(r)
    resp.encoding = "UTF-8"
    child_page_content = resp.text
    obj3 = re.compile(r'<title>(?P<titles>.*?)-', re.S)
    result3 = obj3.finditer(child_page_content)

    for title in result3:
        title = title.group('titles')
        # print(title)
        f.write(title+'   ')
    obj4 = re.compile(r'<p class="content-tip"> (?P<times>.*?) 作者', re.S)
    result4 = obj4.finditer(child_page_content)
    for time in result4:
        time = time.group('times')
        # print(time)
        f.write(time+'\n')
    session = requests.Session()
    resp = session.get(url=r, headers=headers).text.encode('latin1')
    tree = etree.HTML(resp)
    links = tree.xpath(
        '/html/body/div[@class="news-list-content"]/div[2]/div[2]/div[1]/div/p|//*[@id="vsb_content"]/div/table|/html/body/div[2]/div[2]/div[2]/div[1]/div/form'
         )
    if not links:
        f.write('无正文')
        break
    for li in links:
        page_list_li = li.xpath('.//text()')
        f.writelines(page_list_li)

f.close()
print('TXT OVER!')

# 4 爬取图片放入相应文件夹
code = 0

for r in url_list:

    resp = requests.get(r)
    resp.encoding = "UTF-8"
    child_page_content = BeautifulSoup(resp.text, "html.parser")
    img_list = child_page_content.find("div", class_="v_news_content").find_all("img")
    # print(img_list)

    # 处理重复文件名
    img_list = rename_duplicate(str(img_list), False)

    for li in img_list:
        obj5 = re.compile(r'<img src="(?P<src>.*?)"/>',re.S)
        result5 = obj5.search(li)
        if not result5:
            break
        src = result5.group('src')

        img_url = "https://sise.uestc.edu.cn" + src
        img = requests.get(img_url)
        # print(img)
        img_name = src.split("/")[-1]
        img_name = img_name.split('?')[0]
        # print(img_name)

        img_path = f'C:/Users/nllkj/Desktop/休对故人思故国/焦糖工作室招新/#5-赖子秋/任务一/{renamed_titles[code]}/{renamed_titles[code]}' + img_name
        code += 1
        with open(img_path, mode="wb") as img_f:
            img_f.write(img.content)

print('IMG OVER!')


# 5 爬取附件放入相应文件夹
code = 0

for r in url_list:
    resp = requests.get(r)
    resp.encoding = "UTF-8"
    child_page_content = BeautifulSoup(resp.text, "html.parser")
    href_list = child_page_content.find("div", class_="v_news_content").find_all("a")

    for lii in href_list:
        href = lii.get('href')
        # print(href)

        # 判断是否为空
        if not href:
            break
        
        # 区别不同网址
        # try:
        text1 = href.split(".")[0]
        # except AttributeError:
            # print(href)
            # break
        if text1 == 'https://www':
            href_url = href
        else:
            href_url = "https://sise.uestc.edu.cn" + href

        # 去除杂质
        text2 = href + '@'
        text2 = text2.split("@")[1]
        if text2 == 'uestc.edu.cn':
            break
        text3 = href.split(".")[0]
        if text3 == 'http://uestc' or text3 == 'http://sose':
            break

        href_name = href.split("/")[-1]
        href_name = href_name.split('?')[0]
        # print(href_name)
        fail_name = "ERROR " + href_name
        href_path = f'C:/Users/nllkj/Desktop/休对故人思故国/焦糖工作室招新/#5-赖子秋/任务一/{renamed_titles[code]}/' + href_name
        fail_path = f'C:/Users/nllkj/Desktop/休对故人思故国/焦糖工作室招新/#5-赖子秋/任务一/{renamed_titles[code]}/' + fail_name + '.txt'
        code += 1

        try:
            href_content = requests.get(href_url).content
        except requests.exceptions.ConnectionError:
            with open(fail_path, mode="w") as h_f:
                h_f.write('附件失效')
        else:
            with open(href_path, mode="wb") as h_f:
                h_f.write(href_content)

print('HREF OVER!')

print('ALL OVER!!!!')







