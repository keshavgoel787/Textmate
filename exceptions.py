"""
Filename: exceptions.py
Author: Joshua Longo, Keshav Goel
Course: DS3500
Date: Nov 22 2024
Description: Creates custom exceptions to be thrown in the textmate class.
"""

class TextasticError(Exception):
    """Base class for all exceptions in the Textastic library."""
    pass

class FileNotFoundError(TextasticError):
    """Raised when a specified file is not found."""
    def __init__(self, filename, message="File not found. Please check the file path."):
        self.filename = filename
        self.message = f"{message} Filename: {filename}"
        super().__init__(self.message)

class StopWordsLoadError(TextasticError):
    """Raised when stop words fail to load."""
    def __init__(self, url, message="Failed to load stop words from the provided URL."):
        self.url = url
        self.message = f"{message} URL: {url}"
        super().__init__(self.message)

class ParsingError(TextasticError):
    """Raised when there is an error during text parsing."""
    def __init__(self, filename=None, message="An error occurred during parsing."):
        self.filename = filename
        file_info = f" Filename: {filename}" if filename else ""
        self.message = message + file_info
        super().__init__(self.message)

class SankeyDataError(TextasticError):
    """
    Raised when there is an issue with generating Sankey diagram data.
    
    Specifically handles cases where input words are not lowercase or processed correctly.
    """
    def __init__(self, invalid_words=None, message="Invalid or improperly formatted words provided for Sankey diagram."):
        self.invalid_words = invalid_words
        word_list = f" Invalid words: {', '.join(invalid_words)}" if invalid_words else ""
        self.message = message + word_list
        super().__init__(self.message)

class VisualizationError(TextasticError):
    """Raised when there is an issue with data visualization."""
    def __init__(self, message="An error occurred during visualization."):
        self.message = message
        super().__init__(self.message)

class SentimentAnalysisError(TextasticError):
    """Raised when there is an issue during sentiment analysis."""
    def __init__(self, message="An error occurred during sentiment analysis."):
        self.message = message
        super().__init__(self.message)
