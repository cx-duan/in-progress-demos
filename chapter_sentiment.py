from enum import unique
from re import S
import numpy as np
from collections import Counter
import json
from pprint import pprint

with open('response.json', 'r') as transcript_json:
    transcript_data = json.load(transcript_json)

chapters = transcript_data['chapters']
sentiments = transcript_data['sentiment_analysis_results']

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


def get_sentiment(start, end, chapter):
    sent = []
    chap_arr = []
    for sentiment in sentiments:
        if int(sentiment['start']) >= start and int(sentiment['end'] <= end):
            sent.append(sentiment)
    for s in sent:
        chap_arr.append(sent_to_num[s['sentiment']])
    return chapter, chap_arr

sent_chap = {}
for chap in chapters:
    start = 0
    end = int(chap['end'] + 2000)
    if int(chap['start'] - 2000 >= 0):
        start = int(chap['start'] - 2000)
    sent = get_sentiment(start, end, chap['gist'])
    if sent[0] in sent_chap:
        sent_chap[sent[0]].append(sent[1])
    else:
        sent_chap[sent[0]] = [sent[1]]

real_sent_chap = {}
for i in sent_chap:
    flat = flatten(sent_chap[i])
    s = sum(flat)
    l = len(flat)
    if l > 0:
        avg = s / l
        real_sent_chap[i] = avg

# Add the sentiment value to the dictionary based on if the average sentiment value is >0, <0, =0
sent_and_label = {}
sentences = []
for i in real_sent_chap:
    sentiment = "neutral"

    if real_sent_chap[i] < 0:
        sentiment = "negative"
        if real_sent_chap[i] < -0.5:
            sentiment = "very negative"
    elif real_sent_chap[i] > 0:
        sentiment = "positive"
        if real_sent_chap[i] < 0.5:
            sentiment = "very positive"
    
    sent_and_label[i] = {
        "sentiment_value": real_sent_chap[i],
        "sentiment": sentiment
    }
    sentences.append("Chapter: %s - has a %s sentiment" % (i, sentiment))
print(sentences)