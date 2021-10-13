import re
import urllib.request
import time
from lxml import etree
import requests
import os
import pymysql


# time.sleep(2)

# 连接数据库并创建表
db = pymysql.connect(host='localhost', user='root', password='172229', port=3306)
cursor = db.cursor()
cursor.execute('SELECT VERSION()')
data = cursor.fetchone()
print('Database version:', data)
cursor.execute("CREATE DATABASE IF NOT EXISTS 爬虫任务二 DEFAULT CHARACTER SET utf8")

db = pymysql.connect(host='localhost', user='root', password='172229', port=3306, db='爬虫任务二')
cursor = db.cursor()
sql1 = 'DROP TABLE IF EXISTS 评论详情;'
sql2 = 'CREATE TABLE 评论详情 (' \
       '评论内容 TEXT,' \
       '链接 VARCHAR(255),' \
       '作者 VARCHAR(255),' \
       '发布时间 VARCHAR(255),' \
       '点赞数 VARCHAR(255),' \
       '空间链接 VARCHAR(255),' \
       '头像图片 LongBlob)' \

cursor.execute(sql1)
cursor.execute(sql2)

# 为每条评论创建文件夹
for code in range(1, 121):
    path = f'C:/Users/LuoSa/Desktop/休对故人思故国/2021焦糖招新-赖子秋/#5-赖子秋/任务二/评论{code}'
    isExists = os.path.exists(path)
    if not isExists:
        os.mkdir(path)

code = 1

for i in range(1, 7):
    # print(i)
    r = 'https://t.bilibili.com/560233713032161611?tab=2'
    url = 'https://api.bilibili.com/x/v2/reply?jsonp=jsonp&pn=' +str(i)+ '&type=17&oid=560233713032161611&sort=2'
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36' } #代理用户进行浏览器伪装
    html = urllib.request.Request(url=url, headers=headers)
    data = urllib.request.urlopen(html).read().decode('utf-8')

    obj = re.compile(r'"code":0,"message":"0",(?P<page0>.*)然然可以去b站关注嘉然今天吃什么@嘉然今天吃什么 ，这个小姐姐可以给所有人带来甜甜的快乐', re.S)
    result = obj.finditer(data)
    for ii in result:
        page0 = ii.group('page0')
        # print(page0)
        obj1 = re.compile(r'"parent":0(?P<page>.*?)"max_line":6', re.S)
        result1 = obj1.finditer(page0)

        for it in result1:
            page = it.group('page')
            # print(page)

            path = f'C:/Users/LuoSa/Desktop/休对故人思故国/2021焦糖招新-赖子秋/#5-赖子秋/任务二/评论{code}/评论{code}内容.txt'
            # f = open(path, 'a', encoding='utf-8')

            # 爬取评论内容
            obj2 = re.compile(r'"message":"(?P<commend>.*?)","plat"', re.S)
            result2 = obj2.finditer(page)
            for itt in result2:
                commend = itt.group('commend')
                commend = commend.replace('\\n', '\n')
                commend = commend.replace('\\u0026#34;', ' ')
                # commends.append(commend)
                # print(page)
                # f.write('评论内容：'+commend+'\n')
                # print('评论内容：', commend)

            # 爬取作者
            obj3 = re.compile(r'"uname":"(?P<name>.*?)","sex', re.S)
            result3 = obj3.finditer(page)
            for it3 in result3:
                name = it3.group('name')
                # print("作者：", name)
                # f.write("作者："+name+'\n')
                # names.append(name)
                break

            # 爬取时间
            obj4 = re.compile(r'"ctime":(?P<time>.*?),"rpid', re.S)
            result4 = obj4.finditer(page)
            for it4 in result4:
                ctime = it4.group('time')
                # time = int(time)
                timeArray = time.localtime(int(ctime))
                otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
                # print("时间：", otherStyleTime)
                # f.write('时间：'+otherStyleTime+'\n')
                # times.append(time)

            # 爬取点赞数
            obj5 = re.compile(r'"like":(?P<like>.*?),"action"', re.S)
            result5 = obj5.finditer(page)
            for it5 in result5:
                like = it5.group('like')
                # print("点赞数：", like)
                # f.write('点赞数：'+like+'\n')
                # likes.append(like)
                break

            # 爬取链接
            obj6 = re.compile(r'"rpid_str":"(?P<link>.*?)","', re.S)
            result6 = obj6.finditer(page)
            for it6 in result6:
                link = it6.group('link')
                link = 'https://t.bilibili.com/560233713032161611/#reply' + link
                # print("链接：", link)
                # f.write('链接:'+link+'\n')
                # links.append(link)
                break

            # f.close()

            # 爬取作者头像
            obj7 = re.compile(r'"avatar":"(?P<img>.*?)","', re.S)
            result7 = obj7.finditer(page)
            for it7 in result7:
                img = it7.group('img')
                img = requests.get(img)
                img_path = f'C:/Users/LuoSa/Desktop/休对故人思故国/2021焦糖招新-赖子秋/#5-赖子秋/任务二/评论{code}/头像.jpg'
                with open(img_path, mode="rb") as img_f:
                    img = img_f.read()
                    # img_f.write(img.content)
                break

            # 爬取作者空间链接
            obj8 = re.compile(r'"mid":"(?P<link2>.*?)","uname"', re.S)
            result8 = obj8.finditer(page)
            for it8 in result8:
                link2 = it8.group('link2')
                link2 = 'https://space.bilibili.com/' + link2 + '?spm_id_from=444.42.0.0'
                # print("作者空间链接：", link2)
                li_path = f'C:/Users/LuoSa/Desktop/休对故人思故国/2021焦糖招新-赖子秋/#5-赖子秋/任务二/评论{code}/作者空间链接.txt'
                # with open(li_path, mode="w") as li_f:
                    # li_f.write(link2)
                break

            for a in range(1, 4):
                try:
                    sql3 = 'INSERT INTO 评论详情(评论内容, 链接, 作者, 发布时间, 点赞数, 空间链接, 头像图片) VALUES(%s, %s, %s, %s, %s, %s, %s)'
                    data = (commend, link, name, otherStyleTime, like, link2, img)
                    cursor.execute(sql3, data)
                    db.commit()
                    print('OK,', code)
                    break
                except:
                    print("fail,", code)

            code += 1
            print()
            print()

db.close()


