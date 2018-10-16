import mysql.connector
from bs4 import BeautifulSoup
import requests
from functools import reduce

# 爬取链家的租房数据
conn = mysql.connector.connect(host='', user='', password='', database='')
my_url = "https://hz.lianjia.com/zufang/"


def insert(name, price, area, house_type, house_height, direction, community, place1, place2, remark, payment_method):
    cursor = conn.cursor()
    name = "" + name
    price = "".join(price)
    area = "".join(area)
    house_type = "".join(house_type)
    house_height = "".join(house_height)
    direction = "".join(direction)
    community = "".join(community)
    place1 = "".join(place1)
    place2 = "".join(place2)
    remark = "".join(remark)
    payment_method = "".join(payment_method)
    cursor.execute(
        "insert into lianjia_house(name,price,area,house_type,house_height,direction,community,place1,place2,remark,payment_method) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
        [name, price, area, house_type, house_height, direction, community, place1, place2, remark, payment_method])
    cursor.close()
    conn.commit()


def get_page(url):
    page = requests.get(url, "lxml")
    soup = BeautifulSoup(page.text)
    name = soup.find('h1', attrs={"class": "main"}).string
    print(name)
    price = soup.find('span', attrs={"class": "total"}).string
    lf_list = soup.find_all('p', attrs={"class", "lf"})
    area = lf_list[0].text.split("：")[1]
    house_type = lf_list[1].text.split("：")[1]
    house_height = lf_list[2].text.split("：")[1]
    direction = lf_list[3].text.split("：")[1]
    a_list = soup.find('div', attrs={"class": "zf-room"}).find_all('a')
    community = a_list[0].string
    place1 = a_list[2].string
    place2 = a_list[3].string
    payment_method_list = soup.select("div.content > ul > li")
    payment_method = payment_method_list[1].text.split("：")[1].replace(" ", "")
    remarks = soup.select("ul.se > li.tags")
    remark = ""
    if len(remarks) > 0:
        remark = reduce(lambda x, y: x + ", " + y, map(lambda e: e.text.replace(" ", "").replace("\n", ""), remarks))
    insert(name, price, area, house_type, house_height, direction, community, place1, place2, remark, payment_method)


def get_one_page(page_url):
    url = requests.get(page_url, "lxml")
    soup = BeautifulSoup(url.text)
    house_list = soup.find_all('div', attrs={"class": "pic-panel"})
    for house in house_list:
        page_url = house.find('a').attrs["href"]
        get_page(page_url)


if __name__ == '__main__':
    for i in range(1, 101):
        print("第 %d 页" % i)
        url = my_url + "pg/%d" % i
        get_one_page(url)
