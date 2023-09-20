# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import requests
import pandas as pd

website = 'https://glaciertoyota.ca/pre-owned/?condition=used&listing_order=body-style&listing_orderby=ASC'
HEADERS = {'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148'}
response = requests.get(website, headers=HEADERS)
soup = BeautifulSoup(response.content, 'html.parser')
results = soup.find_all('div', {'class':'col-lg-12'})
all_tables = soup.find_all('table', {'class':'options-secondary'})

urls = [website]

#Color
color = []
for url in urls:
    response = requests.get(url)  # Send a GET request to the URL to obtain the HTML content

    if response.status_code == 200:
        tables = pd.read_html(response.text, attrs={'class': 'options-secondary'})

        for table in tables:
            if not table.empty:
                ex_color = table.iloc[0, 1]  # Pulling data from array location [0][1]
                color.append(ex_color)
    else:
        # Handle HTTP request error (e.g., page not found)
        color.append('None') #if data out of range, then just appending 'None' - so no data

#Name
name = []
for url in urls:
    response = requests.get(url)  # Send a GET request to the URL to obtain the HTML content

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all elements with class 'title'
        titles = soup.find_all('div', {'class': 'title'})

        for title in titles:
            name.append(title.get_text().strip())
    else:
        # Handle HTTP request error (e.g., page not found)
        name.append(None)  #if data out of range, then just appending 'None' - so no data

#Milage
mileage = []
for url in urls:
    response = requests.get(url)  # Send a GET request to the URL to obtain the HTML content

    if response.status_code == 200:
        tables = pd.read_html(response.text, attrs={'class': 'options-primary'})

        for table in tables:
            if not table.empty:
                odo = table.iloc[0, 1]  # Pulling data from array location [0][1]
                mileage.append(odo)
    else:
        # Handle HTTP request error (e.g., page not found)
        mileage.append('None') #if data out of range, then just appending 'None' - so no data

#Price
price = []
for url in urls:
    response = requests.get(url)  # Send a GET request to the URL to obtain the HTML content

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all elements with class 'figure'
        figures = soup.find_all('div', {'class': 'figure'})

        for figure in figures:
            price.append(figure.get_text().strip())
    else:
        # Handle HTTP request error (e.g., page not found)
        price.append(None)  #if data out of range, then just appending 'None' - so no data

"""##Pandas Data Frame"""

Dealer_name = pd.DataFrame({'Name':name,
                            'Mileage':mileage,
                            'Price':price,
                            'Color':color})

"""##Export"""

Dealer_name.to_csv('Dealer Cars.csv', index=False)
