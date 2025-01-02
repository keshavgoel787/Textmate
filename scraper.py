"""
Filename: scraper.py
Author: Joshua Longo, Keshav Goel
Course: DS3500
Date: Nov 22 2024
Description: A scraper library that scrapes two particular articles reporting on the 2024 World Series.
The library is utilized within the implementation of the textmate class for nlp.
"""

# Import statements
from bs4 import BeautifulSoup
import requests
from urllib.parse import urlparse

# Function to scrape tsn article and save it
def scrape_tsn(url, filename=None):
    """
    Scrape an article from TSN and save its content to a text file.

    Args:
        url (str): URL of the TSN article to scrape.
        filename (str, optional): Name of the file to save the article. Defaults to None, where filename is
        derived from the website domain.

    Returns:
        None: Saves the scraped article content, including the title and text, to a text file.
    """
    # Send a GET request to fetch the raw HTML content
    response = requests.get(url).text

    # Use beautiful soup to clean html output
    soup = BeautifulSoup(response, 'html.parser')

    # Extract the article title and text
    title = soup.find('h1').get_text()

    # Find div class with paragraph text
    txt_div = soup.find('div', class_='c-text')

    # Extract the paragraphs and join them
    paragraphs = [p.get_text() for p in txt_div.find_all('p')]
    article_text = "\n".join(paragraphs)

    # Determine the website name for the filename if a filename isn't given
    if not filename:
        # Extract the main domain
        domain = urlparse(url).netloc.split('.')[1]
        filename = f"{domain}.txt"

    # Save the article to a text file
    with open(filename, 'w', encoding='utf-8') as file:
         file.write(title + '\n' + article_text)
    print(f"Article saved to {filename}")

# Function to scrape al jazeera article and save it
def scrape_aljaz(url, filename=None):
    """
    Scrape an article from Al Jazeera and save its content to a text file.

    Args:
        url (str): URL of the Al Jazeera article to scrape.
        filename (str, optional): Name of the file to save the article. Defaults to None, where filename is
        derived from the website domain.

    Returns:
        None: Saves the scraped article content, including the title, headers, and paragraphs, to a text file.
    """
    # Send a GET request to fetch the raw HTML content
    response = requests.get(url).text

    # Use beautiful soup to clean html output
    soup = BeautifulSoup(response, 'html.parser')

    # Extract the article title
    title = soup.find('h1').get_text()

    # Initialize an empty list to store content
    content = []

    # Find all the h2 and p elements in their chronological order
    elements = soup.find_all(['h2', 'p'])

    # Loop through elements to build the content list
    current_header = ""
    for element in elements:
        if element.name == 'h2':
            # Update the current header
            current_header = element.get_text()
            # Add the header
            content.append(current_header)
        # If a paragraph add that to content
        elif element.name == 'p':
            paragraph = element.get_text()
            content.append(paragraph)

    # Combine the content into a single string
    article_text = "\n".join(content)

    # Determine the website name for the filename if a filename isn't given
    if not filename:
        # Extract the main domain
        domain = urlparse(url).netloc.split('.')[1]
        filename = f"{domain}.txt"

    # Save the article to a text file
    with open(filename, 'w', encoding='utf-8') as file:
         file.write(title + '\n' + article_text)
    print(f"Article saved to {filename}")

def main():

    # Assign urls to variables
    tsn_url = ("https://www.tsn.ca/mlb/los-angeles-dodgers-outlast-error-prone-new-york-yankees-in-game-5-to-capture-"
               "world-series-title-1.2198200")
    al_jaz_url = ("https://www.aljazeera.com/sports/2024/10/31/la-dodgers-stunning-comeback-beats-ny-yankees-seals-"
                  "world-series-2024")

    # test scraper out
    scrape_tsn(tsn_url)
    scrape_aljaz(al_jaz_url)

if __name__ == '__main__':
    main()