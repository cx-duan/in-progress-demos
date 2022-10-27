from enum import unique
from re import S
import requests
import pandas as pd
import numpy as np
from collections import Counter
import json
from pprint import pprint

with open('response.json', 'r') as transcript_json:
    transcript_data = json.load(transcript_json)

entities = transcript_data['entities']
sentiment_analysis_results = transcript_data['sentiment_analysis_results']

sent_to_num = {
    "POSITIVE": 1,
    "NEUTRAL": 0,
    "NEGATIVE": -1
}

def flatten(S):
    if S == []:
        return S
    if isinstance(S[0], list):
        return flatten(S[0]) + flatten(S[1:])
    return S[:1] + flatten(S[1:])

def get_sentiment(start, end, entity):
    sent = []
    ent_arr = []
    for sentiment in sentiment_analysis_results:
        if int(sentiment['start']) >= start and int(sentiment['end'] <= end):
            sent.append(sentiment)
    for s in sent:
        ent_arr.append(sent_to_num[s['sentiment']])
    return entity.lower(), ent_arr

sent_ent = {}
for ent in entities:
    
    sent_list = ''
    start = 0
    end = int(ent['end'] + 2000)
    if int(ent['start'] - 2000 >= 0):
        start = int(ent['start'] - 2000)

    sent = get_sentiment(start, end, ent['text'])
    if sent[0] in sent_ent:
        sent_ent[sent[0]].append(sent[1])
    else:
        sent_ent[sent[0]] = [sent[1]]

real_sent_ent = {}
for i in sent_ent:
    flat = flatten(sent_ent[i])
    s = sum(flat)
    l = len(flat)
    if l > 0:
        avg = s / l
        real_sent_ent[i] = avg

#pprint(real_sent_ent)


sent_and_label = {}
sentences = []
for i in real_sent_ent:
    sentiment = "NEUTRAL"
    if real_sent_ent[i] < 0:
        sentiment = "NEGATIVE"
    elif real_sent_ent[i] > 0:
        sentiment = "POSITIVE"
    
    sent_and_label[i] = {
        "sentiment_value": real_sent_ent[i],
        "sentiment": sentiment
    }
    sentences.append("%s has a %s sentiment value of %s" % (i, sentiment, str(round(real_sent_ent[i],2))))

#pprint(sent_and_label)
pprint(sentences)
