from requests import get
from bs4 import BeautifulSoup
from time import sleep
from random import randint

import numpy as np
import pandas as pd

response = get('https://detroit.craigslist.org/d/cars-trucks/search/cta')
html_soup = BeautifulSoup(response.text, 'html.parser')

all_posts = html_soup.find('div', class_='search-legend')
total = int(all_posts.find('span', class_='totalcount').text)
print(total)

pages = np.arange(0, total+1, 120)

iterations = 0

post_timing = []
post_hoods = []
post_titles = []
post_links = []
post_prices = []

for page in pages:
    response = get('https://detroit.craigslist.org/d/cars-trucks/search/cta' + 's=' + str(page))

    sleep(randint(1, 5))

    if response.status_code != 200:
        print('Status Code {}'.format(response.status_code))

    page_html = BeautifulSoup(response.text, 'html.parser')

    posts = html_soup.find_all('li', class_='result-row')

    for post in posts:

        post_datetime = post.find('time', class_='result-date')['datetime']
        post_timing.append(post_datetime)

        if post.find('span', class_='result-hood') is not None:
            post_hood = post.find('span', class_='result-hood').text
            post_hoods.append(post_hood)
        else:
            post_hoods.append('')

        post_title = post.find('a', class_='result-title hdrlnk')
        post_titles.append(post_title.text)

        post_link = post_title['href']
        post_links.append(post_link)

        post_price = post.a.text.strip().replace('$', '')

        post_prices.append(post_price)

        iterations += 1
        print("Page " + str(iterations) + " scraped successfully!")

    print("\n")

    print("Scrape complete!")

print(len(post_timing))
print(len(post_hoods))
print(len(post_titles))
print(len(post_prices))
print(len(post_links))

cars = pd.DataFrame({'posted': post_timing, 'location': post_hoods,
                    'titles': post_titles, 'price': post_prices, 'link': post_links})

print(cars.head(10))
