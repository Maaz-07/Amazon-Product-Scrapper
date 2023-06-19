import requests
from bs4 import BeautifulSoup

url = "https://www.amazon.com/s?k=laptop+computer&crid=140WOO6C5KR9B&sprefix=la%2Caps%2C305&ref=nb_sb_ss_ts-doa-p_1_2"

# Send a GET request to the URL
response = requests.get(url)

# Create a BeautifulSoup object with the HTML content
soup = BeautifulSoup(response.content, "html.parser")

# Find all the laptop products on the page
products = soup.find_all("div", class_="sg-col-inner")

# Loop through each product and extract the desired information
for product in products:
    # Extract product name
    name_element = product.find("span", class_="a-size-medium")
    if name_element:
        name = name_element.text.strip()
    else:
        continue

    # Extract product price
    price_element = product.find("span", class_="a-offscreen")
    if price_element:
        price = price_element.text.strip()
    else:
        continue

    # Extract product rating
    rating_element = product.find("span", class_="a-icon-alt")
    if rating_element:
        rating = rating_element.text.strip().split()[0]
    else:
        continue

    # Extract number of raters
    raters_element = product.find("span", class_="a-size-base")
    if raters_element:
        raters = raters_element.text.strip().replace(",", "")
    else:
        continue

    # Print the extracted information
    print("Name:", name)
    print("Price:", price)
    print("Rating:", rating)
    print("Number of Raters:", raters)
    print()

