"""
Filename: textmate_app.py
Author: Joshua Longo, Keshav Goel
Course: DS3500
Date: Nov 22 2024
Description: The implementation of the textmate class which involves scraping, translation, and text analysis
functionalities. It processes txt files from various sources, visualizes word relationships
using a Sankey diagram, generates word clouds, and compares sentiment metrics.
"""

# Import statements
from textmate import Textmate
import scraper as sp
import translate as tr
import pprint as pp

def main():

    # Initialize tt class object
    tt = Textmate()

    # Set urls
    tsn_url = ("https://www.tsn.ca/mlb/los-angeles-dodgers-outlast-error-prone-new-york-yankees-in-game-5-to-capture-"
               "world-series-title-1.2198200")
    al_jaz_url = ("https://www.aljazeera.com/sports/2024/10/31/la-dodgers-stunning-comeback-beats-ny-yankees-seals-"
                  "world-series-2024")

    # Scrape non-compatible texts
    sp.scrape_tsn(tsn_url, 'tsn.txt')
    sp.scrape_aljaz(al_jaz_url, 'al_jaz.txt')

    # Load files
    tt.load_text('tsn.txt', label='tsn')
    tt.load_text('al_jaz.txt', label='al_jaz')
    tt.load_text('japannews.txt', label='japannews')
    tt.load_text('bbc.txt', label='bbc')
    tt.load_text('elpais.txt', label='el_pais', parser=tr.openai_translate_parser)
    tt.load_text('latimes.txt', label='latimes')
    tt.load_text('athletic.txt', label='athletic')
    tt.load_text('espn.txt', label='espn')
    tt.load_text('mlb.txt', label='mlb')
    tt.load_text('ap.txt', label='ap')

    # pretty print the data
    pp.pprint(tt.data)

    # Create a sankey visualization
    tt.sankey_from_data(k=5, title='Text-to-Word Sankey Diagram for 2024 World Series Articles', save=True)
    tt.sankey_from_data(themes=['world'], title='Text-to-Word Sankey Diagram for 2024 World Series Articles',
                        filename='world_sankey.png', save=True)
    tt.sankey_from_data(themes=['ohtani'], title='Text-to-Word Sankey Diagram for 2024 World Series Articles',
                        filename='player_sankey.png', save=True)

    # Compare Sentiment polarity and subjectivity
    tt.comp_sentiments_scatter(save=True)

    # Create sublots of wordclouds for each article
    tt.generate_wordclouds(save=True)

if __name__ == '__main__':
    main()