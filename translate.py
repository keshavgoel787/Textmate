"""
Filename: translate.py
Author: Joshua Longo, Keshav Goel
Course: DS3500
Date: Nov 22 2024
Description: A customer parser that utilizes OpenAI's API to translate a txt file
"""

# Import statements
import openai
import dotenv
import os
from textblob import TextBlob
from collections import Counter
from textmate import Textmate

def openai_translate_parser(filename):
    """
    Custom parser that uses OpenAI's API to translate the content of a file into English.

    Args:
        filename (str): Path to the input text file.

    Returns:
        (dict) : Analysis of the translated text, including word count, total words,
        sentiment polarity, sentiment subjectivity, and processed content.
    """
    # load environment variables from env file and initialize openai client using api key from env variable
    dotenv.load_dotenv()
    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    # Read the file contents
    with open(filename, 'r', encoding='utf-8') as f:
        text = f.read()

    # Use OpenAI API to translate the content into English
    response = client.chat.completions.create(
        model="chatgpt-4o-latest",  # Use the desired model
        messages=[
            {"role": "user",
             "content": f"Translate the following text into English:\n{text}"
             }
        ]
    )

    # Extract the translated text
    translated_text = response.choices[0].message.content

    # Preprocess the translated text using the textmate preprocess method
    text_new = Textmate().preprocess_text(translated_text)

    # Analyze the translated text for sentiment and word count
    text_blob = TextBlob(translated_text)
    wordcount = Counter(text_new.split())
    numwords = len(translated_text.split())
    return {
        'wordcount': wordcount,
        'numwords': numwords,
        'sentiment_polarity': text_blob.sentiment.polarity,
        'sentiment_subjectivity': text_blob.sentiment.subjectivity,
        'content': text_new
    }

def main():

    # test the translation of the openai parser
    parsed_translation = openai_translate_parser("elpais.txt")
    print(parsed_translation)

if __name__ == '__main__':
    main()