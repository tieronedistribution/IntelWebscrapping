# Import the necessary libraries
from bs4 import BeautifulSoup
import time
from selenium import webdriver
import csv


# Set up the Selenium WebDriver
path = 'executable path to the driver'
driver = webdriver.Chrome()

# Open the target webpage
driver.get('https://www.amazon.com/stores/page/F5F593B6-3E70-4D1D-9716-9CF687366CAA?ingress=3&visitId=96e37960-519e-4dca-811b-a7a9245670ae')  # Replace with your target URL

# Wait for JavaScript to load
time.sleep(5)  # Adjust timing as necessary depending on the website and your internet speed

html_content = driver.page_source

# Parse the HTML to find product items
soup = BeautifulSoup(html_content, 'lxml')
driver.quit()
items = []

lis = soup.find('div', attrs={'data-testid' : 'product-grid-container'})
products = lis.find_all('li', attrs={'data-testid' : 'product-grid-item'})

# Extract details for each product
for product in products:
    title = product.find('a', attrs = {'data-testid' : 'product-grid-title'}).text
    price = product.find('div', attrs={'data-testid' : 'grid-item-buy-price'}).span['aria-label']
    score = product.find('i', attrs = {'data-testid' : 'icon-star'}).span.text
    people = product.find('span', attrs = {'data-testid' : 'grid-item-review-count'}).text
    review = f"{score} among {people} reviews"
    item = {'title' : title, 'price' : price, 'review' : review}
    items.append(item)

# Save the data extracted into a CSV file
with open('intel.csv', 'w', newline='', encoding = 'utf-8') as file:
    fieldnames = ['Title', 'Price', 'Review']
    writer = csv.DictWriter(file, fieldnames = fieldnames)
    writer.writeheader()
    for i in items:
        writer.writerow(i)