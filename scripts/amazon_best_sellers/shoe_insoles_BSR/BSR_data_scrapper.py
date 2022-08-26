import csv
import time
import datetime
from bs4 import BeautifulSoup
from selenium import webdriver
import chromedriver_autoinstaller

chromedriver_autoinstaller.install()

csv_file = "bsr_shoe_insoles.csv"
main_page = "https://www.amazon.com/gp/bestsellers/hpc/3780121"
page2 = "/ref=zg_bs_pg_2?_encoding=UTF8&pg=2"
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
    for i in pages:
        print("Scraping page: " + i)
        driver.get(i)
        # Get scroll height
        last_height = driver.execute_script("return document.body.scrollHeight")

        while True:
            # Scroll down to bottom
            driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight-2000);"
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
        for item in soup.select("#gridItemRoot"):
            try:
                print("----------------------------------------")
                rank = item.select_one(".zg-bdg-text").get_text().strip()
                ratings = item.select_one(".a-size-small").get_text().strip()
                itm = str(item)
                asid = itm[itm.find("/dp/") + 4 : itm.find("/dp/") + 14]
                print(asid)
                itm = item.text
                r = itm[-10:]
                price = r[r.find("$") + 1 :]
                print(price)
                print(rank)
                print(ratings)
                results.append([dt, asid, rank, ratings, price])
            except:
                print("There is an error with this product")
        print("----------------------------------------")
        if rank == "#50" or rank == "#100":
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