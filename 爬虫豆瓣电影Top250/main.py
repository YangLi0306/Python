# -*- coding = utf-8 -*-
# @Time: 2022/5/9 9:10
# @File: main.py
# @Software: PyCharm

from bs4 import BeautifulSoup      #网页解析，获取数据
import re       #正则表达式，进行文字匹配
import urllib.request, urllib.error  #制定URL，获取网页数据
import xlwt     #Excel操作

def Network_Crawler():
    baseurl = "https://movie.douban.com/top250?start=" 
    #1. 爬取网页
    datalist = getData(baseurl)
    savepath = ".\\Douban_Movie_Top_250.xls"
    # 保存数据
    saveData(datalist, savepath)

# 相关信息过滤
findTitle = re.compile(r'<span class="title">(.*)</span>')
findRating = re.compile(r'<span class="rating_num" property="v:average">(.*)</span>')
findJudge = re.compile(r'<span>(\d*)人评价</span>')
findSummary = re.compile(r'<span class="inq">(.*)</span>')

def getData(baseurl):
    datalist = []
    for i in range(0, 10):
        url = baseurl + str(i*25)
        html = askURL(url)

        # 解析数据
        soup = BeautifulSoup(html,"html.parser")
        for item in soup.find_all('div', class_="item"): #查找符合要求的字符串
            data = []
            item = str(item)
            Title = re.findall(findTitle, item)
            data.append(Title[0])
            Rating = re.findall(findRating, item)[0]
            data.append(Rating)
            Judge = re.findall(findJudge, item)[0]
            data.append(Judge)
            Summary = re.findall(findSummary, item)
            if len(Summary)!= 0:
                data.append(Summary[0])
            else:
                data.append('-')
            datalist.append(data)
    return datalist

def askURL(url):
    # 模拟头部信息，向服务器发送信息
    head = {
        "User-Agent" : "Mozilla / 5.0(Windows NT 10.0; Win64; x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 101.0.4951.54 Safari / 537.36"
    }
    request = urllib.request.Request(url, headers = head)
    html = ""
    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode("utf-8")
    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)
    return html

def saveData(datalist, savepath):
    book = xlwt.Workbook(encoding='utf-8', style_compression=0)
    sheet = book.add_sheet('豆瓣电影Top250', cell_overwrite_ok=True)
    col = ["电影名字" , "评分", "评价人数", "一句话简介"]
    for i in range(0, 4):
        sheet.write(0, i, col[i])
    for i in range(0, 250):
        print("保存第 %d 条数据" % (i + 1))
        data = datalist[i]
        for j in range(0, 4):
            sheet.write(i + 1, j, data[j])
    book.save(savepath)


if __name__ == '__main__':
    Network_Crawler()
