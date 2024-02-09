import os
import csv
import requests
import re
import time
from bs4 import BeautifulSoup

def scrape(source_url, soup):
    books = soup.find_all("article", class_= "product_pod")

    for book in books:
        info_url = source_url+"/"+book.h3.find("a")["href"]
        cover_url = source_url+"/catalogue"+ \
            book.a.img["src"].replace("..", "")
        title = book.h3.find("a")["title"]
        rating = book.find("p", class_= "star-rating")["class"][1]
        price = book.find("p", class_="price_color").text.strip().encode(
            "ascii", "ignore").decode("ascii")
        availability = book.find(
            "p", class_="instock availability").text.strip()
        
        write_to_csv([title, rating, price, availability])

def browse_and_scrape(seed_url, page_number=1):
    # Fetch the URL - We will be using this to append to images and info routes
    url_pat = re.compile(r"(http://.*\.com)")
    source_url = url_pat.search(seed_url).group(0)

   # Page_number from the argument gets formatted in the URL & Fetched
    formatted_url = seed_url.format(str(page_number))

    try:
        if page_number <= 5:
            html_text = requests.get(formatted_url).text
            # Prepare the soup
            soup = BeautifulSoup(html_text, "html.parser")
            print(f"Now Scraping - {formatted_url}")

            # This if clause stops the script when it hits an empty page
            if soup.find("li", class_="next") != None:
                scrape(source_url, soup)     # Invoke the scrape function
                # Be a responsible citizen by waiting before you hit again
                time.sleep(3)
                page_number += 1
                # Recursively invoke the same function with the increment
                browse_and_scrape(seed_url, page_number)
            else:
                scrape(source_url, soup)     # The script exits here
                return True
            return True
    except Exception as e:
        return e


def write_to_csv(input_list):
    try:
        with open(os.path.join(file_path, "ExampleBookScraper.csv"), "a", newline="") as f:
            csv_writer = csv.writer(f, delimiter= ";", lineterminator= "\n")
            csv_writer.writerow(input_list)
    except:
        return False


if __name__ == "__main__":
    file_path = os.path.dirname(__file__)
    col_list = ["Name", "Rating", "Price", "Is in stock?"]
    write_to_csv(col_list)
    seed_url = "http://books.toscrape.com/catalogue/page-{}.html"
    print("Web Scraping has begun")
    result = browse_and_scrape(seed_url)
    if result == True:
        print("Web scraping is now complete!")
    else:
        print(f"Oops, That doesn't seem right!!! - {result}")