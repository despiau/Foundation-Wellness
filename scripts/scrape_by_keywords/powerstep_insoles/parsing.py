import urllib3
from bs4 import BeautifulSoup
import csv

http = urllib3.PoolManager()


def scrape():
    data = open("temp.html", "r", encoding="utf-8")
    soup = BeautifulSoup(data, "html.parser")
    # soup = BeautifulSoup(response.content, "lxml")
    products = soup.find_all("div",{"class":"s-asin"})
    

    for item in products:
        itm = str(item)
        asin = itm[itm.find('asin=')+6:itm.find('asin=')+16]

        # try:
        print("----------------------------------------")
        # print(item.find('span', )
        title = item.select_one(".a-size-base-plus").get_text().strip()
        print(asin)
        print(title)



# def Blog_post(link):
#     try:
#         print(link)
#         blogData = http.request("GET", link)
#         soup = BeautifulSoup(blogData.data, "html.parser")
#         article = ""
#         tags = []
#         heading = soup.find("h1").text
#         for para in soup.find_all("p"):
#             p = para.text
#         p = p.strip("/u")
#         article = article + " " + p
#         for mtags in soup.find_all("a", {"class ": "link u - baseColor — link"}):
#             tags.append(mtags.text)
#             # CreateDataFrame(list())
#             someList = [heading, article, tuple(tags)]
#             # print(someList[0])
#             CreateDataFrame(someList)
#     except:
#         pass


scrape()
