import requests
from bs4 import BeautifulSoup

def extract_news_data(url):
    # Send a GET request to the URL
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract headings and paragraphs from specific tags and class
        headings = [heading.text.strip() for heading in soup.find_all('h1')]
        
        # Find the parent 'div' containing both the heading and paragraphs
        parent_div = soup.find('div', class_='story-detail')

        # Extract paragraphs from all 'p' tags under the parent div
        paragraphs = [paragraph.text.strip() for paragraph in parent_div.find_all('p')]

        # Save the extracted data to a text file
        with open('news_data.txt', 'w', encoding='utf-8') as file:
            file.write("Headings:\n")
            for heading in headings:
                file.write(heading + '\n')

            file.write("\nParagraphs:\n")
            for paragraph in paragraphs:
                file.write(paragraph + '\n')

        print("Data has been saved to 'news_data.txt'")
    else:
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")

# Replace 'https://example.com' with the actual URL of the news blog you want to scrape
news_url = 'https://e.thenews.com.pk/detail?id=288049'
extract_news_data(news_url)
