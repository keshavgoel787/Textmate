"""
Filename: textmate.py
Author: Joshua Longo, Keshav Goel
Course: DS3500
Date: Nov 22 2024
Description: A reusable library for text analysis and comparison. The framework supports any collection of
text of interest with the implementation of a custom parser.
"""

# Import statements
from collections import defaultdict, Counter
import pandas as pd
import matplotlib.pyplot as plt
from textblob import TextBlob
import textmate_sankey as sk
import re
import requests
from wordcloud import WordCloud
import plotly.express as px
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords

# Import custom exceptions
from exceptions import *

# Download wordnet resource from nltk downloader and ensure NLTK stop words are downloaded
nltk.download('wordnet')
nltk.download('stopwords')

class Textmate:

    def __init__(self):
        """ Constructor that initializes the object with data storage, stop words, and a lemmatizer. """
        self.data = defaultdict(dict)
        self.stop_words = self.load_stop_words()
        self.lemmatizer = WordNetLemmatizer()

    def load_stop_words(self):
        """
        Load stop words from an external file and add custom words to the list.

        Args:
            stopfile (str): URL or path to the file containing stop words.

        Returns:
            stopwords (set): A set of stop words including custom additions.
        """
        try:
            # Load the NLTK stop words for English
            stopwords_set = set(stopwords.words('english'))

            # Add custom words to the stop words set
            stopwords_set.update(['dodger', 'dodgers', 'yankees', 'yankee', 'game', 'series', 'angeles', 'los', 'said'])
            return stopwords_set
        except Exception as e:
            raise StopWordsLoadError() from e

    def preprocess_text(self, text):
        """
        Preprocess text by normalizing, removing punctuation and stop words, and lemmatizing.

        Args:
            text (str): Input text to preprocess.

        Returns:
            (str): The cleaned and lemmatized text.
        """
        try:
            text_lower = text.lower()
            text_new = re.sub(r"[^\w\s&]", "", text_lower)
            words = text_new.split()
            filtered_text = [w for w in words if w not in self.stop_words]
            lemmatized_words = [self.lemmatizer.lemmatize(w) for w in filtered_text]
            return ' '.join(lemmatized_words)
        except Exception as e:
            raise ParsingError(message="An error occurred during text preprocessing.") from e

    def default_parser(self, filename):
        """
        Parse a standard text file and produce extracted data results.

        Args:
            filename (str): Path to the text file to be parsed.

        Returns:
            (dict): Extracted data including word count, number of words, sentiment polarity, and subjectivity.
        """
        try:
            with open(filename, 'r') as f:
                text = f.read()
        except FileNotFoundError:
            raise FileNotFoundError(filename)
        except Exception as e:
            raise ParsingError(filename) from e

        try:
            text_new = self.preprocess_text(text)
            wordcount = Counter(text_new.split())
            numwords = len(text_new.split())
            analysis = TextBlob(text)
            return {
                'wordcount': wordcount,
                'numwords': numwords,
                'sentiment_polarity': analysis.sentiment.polarity,
                'sentiment_subjectivity': analysis.sentiment.subjectivity,
                'content': text_new,
            }
        except Exception as e:
            raise ParsingError(filename) from e

    def load_text(self, filename, label=None, parser=None):
        """
        Register a document with the framework.

         Args:
            filename (str): Path to the text file.
            label (str, optional): Custom label for the document. Defaults to filename.
            parser (callable, optional): Custom parsing function. Defaults to default_parser.

        Returns:
            None: Adds text data to nested dictionary.
        """
        try:
            if parser is None:
                results = self.default_parser(filename)
            else:
                results = parser(filename)

            if label is None:
                label = filename

            for k, v in results.items():
                self.data[k][label] = v
        except FileNotFoundError as e:
            raise e
        except ParsingError as e:
            raise e
        except Exception as e:
            raise TextasticError("An error occurred while loading the text.") from e

    def sankey_from_data(self, themes=None, k=5, title=None, filename='ttw_sankey.png', save=False):
        """
        Creates a Sankey diagram based on the article data.

        Args:
            themes (list, optional): Specific themes (words) to include. Defaults to None.
            k (int): Number of most common words to include if no themes are specified. Defaults to 5.
            title (str, optional): Title for the Sankey diagram. Defaults to None.
            filename (str, optional): Filename to save the diagram. Defaults to None.
            save (bool): Whether to save the diagram to a file. Defaults to False.

        Returns:
            fig (plotly graph): The sankey diagram created by the imported make_sankey function.
        """
        try:
            #if the user input choice words check they are the right format
            if themes:
                invalid_words = [word for word in themes if not word.islower()]
                if invalid_words:
                    raise SankeyDataError(invalid_words)

            # Gather all top k words across all articles
            global_top_words = set()
            for wc in self.data['wordcount'].values():
                if themes:
                    # Use the provided themes as the set of global top words
                    global_top_words.update(themes)
                else:
                    # Add the top k words for this article to the global set
                    global_top_words.update(dict(Counter(wc).most_common(k)).keys())

            # Generate Sankey data including all articles and the global top words
            sankey_data = []
            for label, wc in self.data['wordcount'].items():
                # Filter the word counts to include only global top words
                selected_words = {word: count for word, count in wc.items() if word in global_top_words}
                for word, count in selected_words.items():
                    sankey_data.append({'src': label, 'targ': word, 'count': count})

            #Create a datagrame from that data and use the make_sankey function to make the sankey
            df = pd.DataFrame(sankey_data)
            if not df.empty:
                fig = sk.make_sankey(df, src='src', targ='targ', vals='count', title=title,
                               filename=filename)
                
                # save the sankey if the user requested to
                if save:
                    fig.write_image(filename)
                    print(f"Sankey diagram saved as {filename}")

                fig.show()
            else:
                raise SankeyDataError(message="No data available for the given themes or k-most common words.")
        except SankeyDataError as e:
            raise e
        except Exception as e:
            raise VisualizationError("An error occurred while generating the Sankey diagram.") from e

    def generate_wordclouds(self, max_words=100, figsize=(5, 10), filename='wordcloud.png', save=False):
        """
        Generate word clouds for each document.

        Args:
            max_words (int): Maximum number of words in the word cloud. Defaults to 100.
            figsize (tuple): Size of the word cloud figure. Defaults to (25, 10).
            filename (str): File name for saving the word cloud. Defaults to 'wordcloud.png'.
            save (bool): Whether to save the word cloud to a file. Defaults to False.

        Returns:
        """
        try:
            #Gets all the file names, wordcounts, and sets the rows and column amount
            labels = list(self.data['wordcount'].keys())
            wordcounts = list(self.data['wordcount'].values())
            num_docs = len(labels)
            cols = int(len(labels) * 0.2)
            rows = (num_docs // cols) + (num_docs % cols > 0)
            
            #create subplots and flatten to make iteration easier
            fig, axes = plt.subplots(rows, cols, figsize=figsize)
            axes = axes.flatten()

            #iterate through each label and subplot, and plot the wordcloud 
            for i, (label, wc) in enumerate(zip(labels, wordcounts)):
                wordcloud = WordCloud(max_words=max_words, background_color='white',
                                      colormap= 'twilight').generate_from_frequencies(wc)
                axes[i].imshow(wordcloud, interpolation='bilinear')
                axes[i].axis('off')
                axes[i].set_title(label, fontsize=10)

            #remove any unused subplots
            for ax in axes.flatten():
                if not ax.has_data():
                    fig.delaxes(ax)

            plt.tight_layout()
            
            #If the user chooses, save the wordcloud 
            if save:
                plt.savefig(filename)
                print(f"Word Cloud saved as {filename}")

            plt.show()         

        except Exception as e:
            raise VisualizationError("An error occurred while generating word clouds.") from e

    def comp_sentiments_scatter(self, filename='sentscatter.png', save=False):
        """
        Compare sentiment polarity and subjectivity using a scatter bubble plot.

        Args:
            filename (str): Filename to save the plot. Defaults to sentscatter.png.
            save (bool): Whether to save the scatter plot to a file. Defaults to False.

        Returns:
            fig (plotly graph): The sentiment bubble scatter plot.
        """
        try:
            # Prepare the data
            polarities = {label: self.data['sentiment_polarity'][label] for label in self.data['sentiment_polarity']}
            subjectivities = {label: self.data['sentiment_subjectivity'][label] for label in
                            self.data['sentiment_subjectivity']}
            wordcounts = {label: sum(self.data['wordcount'][label].values()) for label in self.data['wordcount']}

            # Create a DataFrame for Plotly
            data = {
                "Article": list(polarities.keys()),
                "Polarity": list(polarities.values()),
                "Subjectivity": list(subjectivities.values()),
                "Word Count": list(wordcounts.values())
            }
            df = pd.DataFrame(data)

            # Create the scatter bubble plot
            fig = px.scatter(
                df,
                x="Polarity",
                y="Subjectivity",
                size="Word Count",
                color="Article",
                hover_name="Article",
                title="Sentiment Analysis of 2024 World Series Articles",
                labels={"Polarity": "Sentiment Polarity", "Subjectivity": "Sentiment Subjectivity"}
            )

            # Customize the layout
            fig.update_layout(
                xaxis=dict(title="Polarity"),
                yaxis=dict(title="Subjectivity"),
                legend_title="Articles",
                )

            # If user chooses to save the plot
            if save:
                fig.write_image(filename)
                print(f'Figure saved as {filename}')

            fig.show()
        except SentimentAnalysisError as e:
            raise e

