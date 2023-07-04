from bs4 import BeautifulSoup
import requests
import openpyxl

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

data = []
attribute_names = set()

for link in links_list:
    product_page = requests.get(link, headers=HEADERS)
    product_soup = BeautifulSoup(product_page.content, "html.parser")

    name = product_soup.find("span", attrs={'id': 'productTitle'}).text.strip()
    price = product_soup.find("span", attrs={'class': 'a-offscreen'}).text.strip()
    rating = product_soup.find("span", attrs={'class': 'a-icon-alt'}).text.strip()
    num_raters = product_soup.find("span", attrs={'id': 'acrCustomerReviewText'}).text.strip()
    availability_element = product_soup.find("span", attrs={'class': 'a-size-medium a-color-success'})
    availability = availability_element.text.strip() if availability_element else 'Not available'

    description_table = product_soup.find("table", attrs={'class': 'a-normal a-spacing-micro'})
    if description_table:
        rows = description_table.find_all("tr")
        description_data = {}
        for row in rows:
            cells = row.find_all("td")
            if len(cells) == 2:
                attribute = cells[0].find("span").text.strip()
                value = cells[1].find("span").text.strip()
                description_data[attribute] = value
                attribute_names.add(attribute)
    else:
        description_data = {}

    item_data = [name, price, rating, num_raters, availability]
    for attribute in attribute_names:
        item_data.append(description_data.get(attribute, ""))

    data.append(item_data)

# Create an Excel workbook and worksheet
workbook = openpyxl.Workbook()
worksheet = workbook.active

# Write headers to the worksheet
headers = ['Name', 'Price', 'Rating', 'Number of Raters', 'Availability']
headers.extend(attribute_names)
worksheet.append(headers)

# Write data to the worksheet
for item in data:
    worksheet.append(item)

# Save the workbook
workbook.save("laptop_data.xlsx")
