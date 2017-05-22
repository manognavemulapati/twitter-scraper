""" This class creates an object that given a string word or phrase, will scrape Twitter messages for the idea contained in the word or phrase. This is done by first parsing the phrase and extracting synonyms of important nouns, then performing searches using the Twitter API for both the original phrase and variations of the phrase with the synonyms substituted.
    ***UNIMPLEMENTED***: This code also implements a matrix-vector recursive neural network that performs sentiment analysis on a database of messages for the intention of "going for a run." The composition function assigns the product of each word vector and its context matrix a feature on a scale from 1 to 5 of how relevant to this idea the phrase is. The final feature value outputed after the root node of the parse tree has been computed determines whether or not the sentence overall has the intent of going for a run.
"""

import random
import nltk
from nltk.corpus import wordnet as wn
import twitter
import pymongo
from pymongo import MongoClient
import json
import collections
import re
import twilio_text

class TwitterScraper :

    api = twitter.Api (consumer_key = 'I87Eq5ApXLc32Pj10EfCrOLeE',
                    consumer_secret = 'tNiEzFAsm1OYAMDHZDGcKmESTc0e7TU7ntshMImMJ4C2JX0QYS',
                    access_token_key = '865616999942107136-qDE0v22XVo36pybmwylm7dGGolgjRaB',
                    access_token_secret = '9cZaEjZUUJO3AAO1q4WvvtF0whrnNhVot1KBdHCaRafKz')

    client = MongoClient()
    db = client.database


    def __init__ (self, phrase) :
        self.phrase = phrase
        '''initializes object with a string that contains a word or phrase to be searched for'''

    def parse_phrase (self) :
        tokens = nltk.word_tokenize(self.phrase)
        pos = nltk.pos_tag(tokens)
        '''trained by default with Penn Treebank Training Set'''
        synonyms = dict()
        pattern = re.compile("NN.*")
        for i in pos :
            (word, p) = i
            if (re.match(pattern, p)) :
                syns = []
                for synset in wn.synsets(word,pos=wn.NOUN) :
                    for lemma in synset.lemmas() :
                        syns.append(str(lemma.name()))
                synonyms[word]=syns
        return synonyms
        '''returns a dictionary containing each noun in the original phrase, mapped to its corresponding synonyms'''

        
    def search_query(self) :
        results = list()
        results.append(self.api.GetSearch(raw_query="q=%22go%20for%20a%20run%22&src=typd"))
        ''' search results with the exact phrase "go for a run" '''
        results.append(self.api.GetSearch(raw_query="q=go%20for%20a%20run%20OR%20jog&src=typd"))
        ''' search results with either run or jog '''
        results.append(self.api.GetSearch(raw_query="q=%23run&src=typd"))
        ''' search results with the hashtag #run '''
        return results
    

    def decode_json(self,results) :
        docs = list()
        for r in results :
                message = {}
                raw = json.loads(json.dumps(r._json))
                text = (raw[u'text'])
                date = (raw[u'created_at'])
                user = ""
                if (raw[u'entities'][u'user_mentions'] != []) : #if user is anonymous, this parameter would be empty
                    user = str(raw[u'entities'][u'user_mentions'][0][u'screen_name'])
                message = {'text':text, 'date':date, 'username':user}
                ''' converts JSON format of tweet into a dictionary containing the text of the tweet, the author, and the date/time it was posted '''
                docs.append(message)
        return docs
        ''' returns a list of messages '''
                

    def add_to_database(self,docs) :
        for d in docs :
            self.db.collection.insert_one(d)
            ''' adds all collected messages in dictionary format to a collection in local mongoDB instance '''
                

    def test_text (self) :
            '''***For testing purposes only: Create an instance of this class and run test_text() to receive a text of a randomly chosen tweet from the database.***'''
        results = self.search_query()
        msgs = list()
        for r in results :
            for i in r :
                if (type(i) == list) :
                    msgs.append(i)
        self.add_to_database(self.decode_json(msgs))
        message = self.db.collection.find(limit=1)[random.randint(0,self.db.collection.count({}))]

        M ="Tweet: " + (str(message['text'])) + "\nUser: " + (str(message['username'])) + "\nDate/Time: " + (str(message['date']))
        sms = twilio_text.SMS(M,"+19786186820","+16692227982")
        sms.send_sms()

