import requests
from bs4 import BeautifulSoup

def get_product_name(soup):
    try:
        name = soup.find("span", attrs={"class": "a-size-medium a-color-base a-text-normal"}).text.strip()
    except AttributeError:
        name = ""
    return name

def get_product_price(soup):
    try:
        price = soup.find("span", attrs={"class": "a-offscreen"}).text.strip()
    except AttributeError:
        price = ""
    return price

def get_product_rating(soup):
    try:
        rating = soup.find("span", attrs={"class": "a-icon-alt"}).text.strip()
    except AttributeError:
        rating = ""
    return rating

def get_number_of_raters(soup):
    try:
        raters = soup.find("span", attrs={"class": "a-size-base"}).text.strip()
    except AttributeError:
        raters = ""
    return raters

def get_availability(soup):
    try:
        availability = soup.find("span", attrs={"class": "a-size-medium a-color-success"}).text.strip()
    except AttributeError:
        availability = "Not Available"
    return availability

if __name__ == '__main__':

    HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/114.0', 'Accept-Language': 'en-US, en;q=0.5'}

    URL = "https://www.amazon.com/s?k=laptop&s=exact-aware-popularity-rank&qid=1688399269&ref=sr_st_exact-aware-popularity-rank&ds=v1%3ACi97C3YM1IuUrOkVaNbdCecAUUc7gn0xMLw0v1%2BPFNk"

    webpage = requests.get(URL, headers=HEADERS)

    soup = BeautifulSoup(webpage.content, "html.parser")

    name = get_product_name(soup)
    price = get_product_price(soup)
    rating = get_product_rating(soup)
    raters = get_number_of_raters(soup)
    availability = get_availability(soup)

    print("Product Name:", name)
    print("Price:", price)
    print("Rating:", rating)
    print("Number of Raters:", raters)
    print("Availability:", availability)
