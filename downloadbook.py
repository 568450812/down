"""
coding:utf-8
"""
import re
import requests
from multiprocessing import Process

book_name = ""
author = ""
describ = ""


def get_one_page(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64)"
                                 " AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.108 Safari/537.36"}
        print(url)
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            response.encoding = "utf-8"
            return response.text
        return None
    except Exception as e:
        print(e)
        return None


def get_url(html, url):
    global book_name, author
    book_name = re.findall("<h1>(.*)</h1>", html)[0]
    author = re.findall("<dl>作&nbsp;&nbsp;者：(.*)</dl>", html)[0]
    url01 = re.findall(r'<li><a href="(\d.{6,12})"', html, re.S)
    list_url = []
    for value in url01:
        value = url + value
        if value in list_url:
            list_url.remove(value)
            list_url.append(value)
        else:
            list_url.append(value)
    return list_url


def get_content(html):
    try:
        title = re.findall("<h1> (.*)</h1>", html)
        print(title)
    except TypeError:
        return
    content = re.findall("&nbsp;&nbsp;&nbsp;&nbsp;(.*?)\r<br />\r<br />", html, re.S)
    f = open("%s.txt" % book_name, "a")
    f.write(title[0] + "\n\n")
    for i in content:
        f.write(i + "\n\n")
    f.close()


def main(bookid):
    url = "https://www.qisuu.la/Shtml%s.html" % bookid
    html = get_one_page(url)
    c1 = re.findall("""<a class="downButton" href='(.*?)'""", html, re.S)
    global describ
    describ = re.findall("<p>(.*)</p>", html, re.S)[0]
    url = "https://www.qisuu.la/" + c1[0]
    html = get_one_page(url)
    list01 = get_url(html, url)
    f = open("%s.txt" % book_name, "a")
    f.write("书名:" + book_name + "\n\n")
    f.write("作者:" + author + "\n\n")
    f.write("简介:" + describ + "\n\n")
    f.close()
    for i in list01:
        html = get_one_page(i)
        get_content(html)


def process():
    p = Process(target=main, args=("9118",))
    p.daemon = True
    p.start()


if __name__ == '__main__':
    process()
    book_id = "15862"
    main(book_id)
