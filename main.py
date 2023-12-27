from bs4 import BeautifulSoup
import requests
import csv

# Scraping professional certificate course data in coursera

professional_course = [['Course Name', 'Level', 'Duration', 'Rating', 'Course Link']]

def get_data(url):

    response = requests.get(url)
    response.raise_for_status()
    data = response.text
    soup = BeautifulSoup(data, 'html.parser')

    list_items = soup.select(selector='li.cds-76')
    for item in list_items:
        try:
            title = item.select_one(selector='a h3').text
            rating = item.select_one(selector='.product-reviews p').text
            details = item.select_one(selector='.cds-CommonCard-metadata p').text.split('Â')
            level = details[0]
            duration = details[-1][2:]
            link = 'https://www.coursera.org' + item.select_one(selector='.cds-ProductCard-header a').get('href')
        except AttributeError:
            continue  # not all items have a full set of information
        new_data = [title, level, duration, rating, link]
        professional_course.append(new_data)


for i in range(1, 13):
    print('page', i)
    url = f'https://www.coursera.org/search?query=professional%20certificate&productTypeDescription=Professional%20Certificates&page={i}&=null'
    get_data(url)

with open('professional_course_on_coursera.csv', mode='w', newline='',  encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerows(professional_course)