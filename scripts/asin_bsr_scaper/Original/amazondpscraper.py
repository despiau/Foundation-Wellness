from selectorlib import Extractor
import gspread
import datetime
import requests
import json
import re

# Date 
now = datetime.datetime.now()
print(now.strftime("%y-%m-%d"))

# Create an Extractor by reading from the YAML file 
e = Extractor.from_yaml_file('selectors.yml') 
def scrape(url): 
    headers = { 'authority': 'www.amazon.com',
                'pragma': 'no-cache',
                'cache-control': 'no-cache',  
                'dnt': '1',  
                'upgrade-insecure-requests': '1',  
                'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',  
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp, image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9', 
                'sec-fetch-site': 'none',
                'sec-fetch-mode': 'navigate',
                'sec-fetch-dest': 'document',  
                'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
              }
 
    # Download the page using requests  
    #print("Downloading %s"%url) 
    r = requests.get(url, headers=headers) 
    # Simple check to check if page was blocked (Usually 503)  
    if r.status_code > 500: 
        if "To discuss automated access to Amazon data please contact" in r.text: 
            print("Page %s was blocked by Amazon. Please try using better proxies\n"%url) 
        else: 
            print("Page %s must have been blocked by Amazon as the status code was %d"% 
                   (url,r.status_code)) 
        return None  
    # Pass the HTML of the page and create  
    return e.extract(r.text) 

# JSON
with open("urls.txt",'r') as urllist, open('output.json','w') as outfile:
    for url in urllist.readlines():
        data = scrape(url)
        # print(data)
        if data:
            print(data)
            json.dump(data,outfile)
            outfile.write("\n")

# Google Sheets Connection
gc = gspread.service_account(filename='cred.json')
sh = gc.open('Original-BSR').sheet1

# Data Insert
date = str(now.strftime("%y-%m-%d"))
title = data["title"]
price = data["price"]
reviews = data["reviews"].split("ratings")[0]
rating = data["rating"].split("out")[0]
bsr = data["bsr"]
bsr = re.findall("\d+", bsr)[0]

sh.append_row([date, title, price, reviews, rating, bsr])