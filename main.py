import requests
from bs4 import BeautifulSoup

def scrape_amazon(search_query):
    base_url = "https://www.amazon.com"
    search_url = base_url + "/s?k=" + search_query.replace(" ", "+")

    # Send a GET request to the search URL
    response = requests.get(search_url)

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, "html.parser")

    # Find all the product containers on the page
    product_containers = soup.find_all("div", {"data-component-type": "s-search-result"})

    # Extract desired information from each product container
    for container in product_containers:
        # Extract the product title
        title_element = container.find("span", class_="a-size-medium")
        if title_element:
            title = title_element.text.strip()
        else:
            title = "N/A"

        # Extract the product price
        price_element = container.find("span", class_="a-offscreen")
        if price_element:
            price = price_element.text.strip()
        else:
            price = "N/A"

        # Extract the product rating
        rating_element = container.find("span", class_="a-icon-alt")
        if rating_element:
            rating = rating_element.text.strip()
        else:
            rating = "N/A"

        # Print the extracted information
        print("Title:", title)
        print("Price:", price)
        print("Rating:", rating)
        print("-----------------------")

# Example usage
search_query = "laptop"
scrape_amazon(search_query)
