import requests
from bs4 import BeautifulSoup
import csv

def extract_blog_content(url):
    # Send an HTTP request to the provided URL
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content of the page using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract the news content from class="jeg_post_title" (h1 tag)
        title_tag = soup.find('h1', class_='jeg_post_title')
        title_content = title_tag.text if title_tag else "Title not found"

        # Extract the news content from class="content-inner" (all p tags)
        content_div = soup.find('div', class_='content-inner')
        p_tags = content_div.find_all('p') if content_div else []

        # Extract the text content from all p tags
        paragraph_content = "\n".join([p.text for p in p_tags])

        return {
            'title': title_content,
            'content': paragraph_content
        }
    else:
        print(f"Failed to retrieve the page. Status Code: {response.status_code}")
        return None

def save_to_csv(file_name, data):
    with open(file_name, 'a', encoding='utf-8', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow([data['title'], data['content']])

# Example usage for the first URL:
url1 = 'https://www.nation.com.pk/E-Paper/islamabad/2024-03-09/page-1/detail-3'
result1 = extract_blog_content(url1)

if result1:
    # Save to CSV file
    file_name = 'page-1.csv'
    save_to_csv(file_name, result1)
    print(f"\nContent from {url1} saved to {file_name}")

# Example usage for the second URL:
url2 = 'https://www.nation.com.pk/E-Paper/islamabad/2024-03-09/page-1/detail-5'
result2 = extract_blog_content(url2)

if result2:
    # Save to CSV file (append to existing file)
    save_to_csv(file_name, result2)
    print(f"\nContent from {url2} saved to {file_name}")
