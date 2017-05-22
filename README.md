# twitter-scraper
Scrape Twitter for messages related to any word or phrase. This package uses the python-twitter wrapper for the Twitter API to scrape for messages, MongoDB to store messages, and Python's Natural Language Toolkit (nltk) to parse the messages.

A TwitterScraper object has the following attributes:
- constructor with string word or phrase
- parse_phrase() - tokenizes words in the object's phrase and returns synonyms of keywords
- search_query() - returns list of results from Twitter searches in JSON format
- decode_json(JSON object list) - returns list of dictionaries representing each JSON tweet
- add_to_database(dict list) - adds dictionaries to mongoDB instance
- test_text() - runs all search functions and randomly chooses one of the resulting tweets to text to a phone number, using Twilio's API
