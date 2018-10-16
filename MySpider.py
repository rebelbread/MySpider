from bs4 import BeautifulSoup
import requests

url = requests.get("https://movie.douban.com/top250", "lxml")
soup = BeautifulSoup(url.text)
page_set = {"https://movie.douban.com/top250"}
movie_titles = []
for link in soup.find("div", attrs={"class": "paginator"}).find_all("a"):
    page_set.add("https://movie.douban.com/top250" + link.get("href"))
for page in page_set:
    url = requests.get(page, "lxml")
    soup = BeautifulSoup(url.text)
    for movie in soup.select("ol > li"):
        # 标题
        movie_title = movie.find_all('span', attrs={"class": "title"})[0].string
        movie_titles.append(movie_title)
        print(movie.find_all('span', attrs={"class": "title"})[0].string)
print(len(movie_titles))
