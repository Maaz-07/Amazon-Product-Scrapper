from bs4 import BeautifulSoup
import requests

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/114.0',
    'Accept-Language': 'en-US, en;q=0.5'
}

URL = "https://www.amazon.com/s?k=laptop&s=exact-aware-popularity-rank&qid=1688399269&ref=sr_st_exact-aware-popularity-rank&ds=v1%3ACi97C3YM1IuUrOkVaNbdCecAUUc7gn0xMLw0v1%2BPFNk"

webpage = requests.get(URL, headers=HEADERS)
soup = BeautifulSoup(webpage.content, "html.parser")

links = soup.find_all("a", attrs={'class': 'a-link-normal s-no-outline'})
links_list = []
for link in links:
    href = link.get('href')
    if href.startswith('/'):
        product_page = requests.get('https://www.amazon.com' + href, headers=HEADERS)
        product_soup = BeautifulSoup(product_page.content, "html.parser")
        sponsored_element = product_soup.find("span", attrs={'class': 'a-color-base'}, string='Sponsored')
        if not sponsored_element:
            links_list.append('https://www.amazon.com' + href)

for link in links_list:
    product_page = requests.get(link, headers=HEADERS)
    product_soup = BeautifulSoup(product_page.content, "html.parser")

    # Extract the name
    name = product_soup.find("span", attrs={'id': 'productTitle'}).text.strip()

    # Extract the price
    price = product_soup.find("span", attrs={'class': 'a-offscreen'}).text.strip()

    # Extract the rating
    rating = product_soup.find("span", attrs={'class': 'a-icon-alt'}).text.strip()

    # Extract the number of raters
    num_raters = product_soup.find("span", attrs={'id': 'acrCustomerReviewText'}).text.strip()

    # Extract the availability
    availability_element = product_soup.find("span", attrs={'class': 'a-size-medium a-color-success'})
    availability = availability_element.text.strip() if availability_element else 'Not available'

    # Extract the specific description
    description_table = product_soup.find("table", attrs={'class': 'a-normal a-spacing-micro'})
    rows = description_table.find_all("tr")
    description_data = {}
    for row in rows:
        cells = row.find_all("td")
        if len(cells) == 2:
            attribute = cells[0].find("span").text.strip()
            value = cells[1].find("span").text.strip()
            description_data[attribute] = value

    print("Name:", name)
    print("Price:", price)
    print("Rating:", rating)
    print("Number of raters:", num_raters)
    print("Availability:", availability)
    print("Description:", description_data)
    print("------")
