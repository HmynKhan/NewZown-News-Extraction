import requests
from bs4 import BeautifulSoup
import csv
import os
import re
import datetime

def extract_news_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        headings = [heading.text.strip() for heading in soup.find_all('h1')]
        parent_div = soup.find('div', class_='story-detail')
        if parent_div:
            paragraphs = [paragraph.text.strip() for paragraph in parent_div.find_all('p')]
            date = '01/20/2024 5:00' # mm/dd/yyyy
            first_paragraph = paragraphs[0] if paragraphs else ''
            city_match = re.search(r'([A-Za-z\s]+(?:\s*[./]\s*[A-Za-z\s]+)?)[.:]', first_paragraph)
            city = city_match.group(1).strip() if city_match else None
            return paragraphs, headings, date, city
        else:
            return None, None, None, None
    else:
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
        return None, None, None, None

def save_to_csv(file_name, paragraphs, headings, city, date):
    mode = 'w' if not os.path.exists(file_name) else 'a'
    with open(file_name, mode, newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        if mode == 'w':
            writer.writerow(['Paragraph', 'Heading', 'City', 'Date'])
        for heading, paragraph in zip(headings, paragraphs):
            writer.writerow([heading, paragraph, city, date])
    print(f"Data of {date} has been saved to {file_name}")

csv_file_name = 'TheNews_1_MarchNews.csv'

for page_number in range(1, 17):
    if page_number not in [4, 6, 7, 8, 9, 10, 11]:
        url = f"https://e.thenews.com.pk/lahore/20-01-2024/page{page_number}"
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            links = soup.find_all('area', href=True)
            for link in links:
                if "?id=" in link['href']:
                    headings, paragraphs, date, city = extract_news_data(link['href'])
                    if headings is not None and paragraphs is not None:
                        save_to_csv(csv_file_name, paragraphs, headings, city, date)
        else:
            print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
