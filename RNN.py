""" This code implements a recursive neural network that performs sentiment analysis on a database of messages for the intention of "going for a run." Positive points are awarded for phrases that reinforce this intention, and negative points are added for words or phrases that imply the opposite intention. (Irrelevant or indifferent messages are given 0 points). In the end, all positive valued messages are aggregated.
"""

import math
import nltk
from nltk import wordnet as wn
import twitter
import pymongo
from pymongo import MongoClient
import json
import collections
import re

class TwitterScraper :

    api = twitter.Api (consumer_key = 'I87Eq5ApXLc32Pj10EfCrOLeE',
                    consumer_secret = 'tNiEzFAsm1OYAMDHZDGcKmESTc0e7TU7ntshMImMJ4C2JX0QYS',
                    access_token_key = '865616999942107136-qDE0v22XVo36pybmwylm7dGGolgjRaB',
                    access_token_secret = '9cZaEjZUUJO3AAO1q4WvvtF0whrnNhVot1KBdHCaRafKz')

    client = MongoClient()
    db = client.database


    def __init__ (self, phrase) :
        self.phrase = phrase

    def parse_phrase (self) :
        tokens = nltk.word_tokenize(self.phrase)
        pos = nltk.pos_tag(self.phrase)
        '''trained by default with Penn Treebank Training Set'''
        synonyms = dict()
        pattern = (r'NN(.*)') | (r'VB(.*)') | (r'JJ(.*)') | (r'RB(.*)')
        for i in tokens :
            (word, p) = pos[i]
            if (re.match(pattern, p)) :
                syn[tokens[i]] = wn.synsets(tokens[i])
        return synonyms

        
    def search_query(self) :
        results = self.api.GetSearch(raw_query="q=run%20&result_type=recent&since=2014-07-19&count=100")
        #"q=go%20for%20a%20run%20OR%20jog&src=typd"
        #"q=%22go%20for%20a%20%22run&src=typd"
        return results

   # def add_to_database(self,docs) :
    #    print (self.db)
     #   print (self.db.collection)
      #  for d in docs :
       #     print(d)
        #    self.db.collection.insert_one(d)

    def decode_json(self,results) :
       # x = 
        docs = list()
        for r in results :
                message = {}
                raw = json.loads(json.dumps(r._json))
                text = (raw[u'text'])
                date = (raw[u'created_at'])
                user = ""
                if (raw[u'entities'][u'user_mentions'] != []) :
                    user = str(raw[u'entities'][u'user_mentions'][0][u'screen_name'])
                message = {'text':text, 'date':date, 'username':user}
                docs.append(message)
        return docs

    def filter (self,messages) :
        tweets = list()
        for msg in messages :
            if ("run" in msg) :
                tweets.append(msg)
        return tweets

    def parse_tree (sent) :
        return

    def tester (self) :
        x = self.search_query()
        docs = self.decode_json(x)
        return docs
