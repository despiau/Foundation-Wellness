import csv
import time
import datetime
from bs4 import BeautifulSoup
from selenium import webdriver
import chromedriver_autoinstaller

chromedriver_autoinstaller.install()

csv_file = "powerstep_insoles.csv"
main_page = "https://www.amazon.com/s?k=powerstep+insoles"
page2 = "&page=2"
pages = [main_page, main_page + page2]
SCROLL_PAUSE_TIME = 3
now = datetime.datetime.now()

dt = now.strftime("%Y-%m-%d %H:%M:%S")


def main():
    options = webdriver.ChromeOptions()
    #options.add_argument("headless")
    options.add_argument("--log-level=1")
    driver = webdriver.Chrome(options=options)
    results = []
    good = True
    y = 0
    for i in pages:
        print("Scraping page: " + i)
        driver.get(i)
        # Get scroll height
        last_height = driver.execute_script("return document.body.scrollHeight")

        while True:
            # Scroll down to bottom
            driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight-2500);"
            )

            # Wait to load page
            time.sleep(SCROLL_PAUSE_TIME)

            # Calculate new scroll height and compare with last scroll height
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        data = open("temp.html", "w", encoding="utf-8")
        data.write(driver.page_source)
        data.close()
        print("Page " + str(i) + " done")
        data = open("temp.html", "r", encoding="utf-8")
        soup = BeautifulSoup(data, "html.parser")
        # soup = BeautifulSoup(response.content, "lxml")
        products = soup.find_all("div",{"class":"s-asin"})
        
        for item in products:
            try:
                itm = str(item)
                asin = itm[itm.find('asin=')+6:itm.find('asin=')+16]

                # try:
                print("----------------------------------------")
                # print(item.find('span', )
                title = item.select_one(".a-size-base-plus").get_text().strip()
                print(asin)
                print(title)
                results.append([dt,str(y+1),asin,title])
            except:
                print("There is an error with this product")
            y += 1
        print("----------------------------------------")
        if y == 60 or y==120:
            pass
        else:
            print("The complete data was not scraped. Might be an internet issue.")
            print("Please run again.")
            print("If the issue persists, increase the value of SCROLL_PAUSE_TIME.")
            good = False
            break
    driver.close()
    if good:
        with open(csv_file, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerows(results)

        print("Data scraping complete")


if __name__ == "__main__":
    main()
