import json

class Review:
    def __init__(self,text,asin):  
        self.text =text
        self.asin =asin
        
file_name='Cell_Phones_and_Accessories_5.json'
reviews=[]
with open(file_name) as f:
    for line in f:
        review=json.loads(line)
        reviews.append(Review(review['reviewText'].lower(),review['asin']))
        
from collections import Counter
import numpy as np
counts = Counter()
for i in range(len(reviews)):
    for word in reviews[i].text.split(" "):
        counts[word] += 1
        
import spacy
import pandas as pd
import os
DATA_DIR="C:/Users/Nishil07/Desktop/amazon label"

"""Create a list of common words to remove"""
stop_words=["i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours", "yourself", 
            "yourselves", "he", "him", "his", "himself", "she", "her", "hers", "herself", "it", "its", "itself", 
            "they", "them", "their", "theirs", "themselves", "what", "which", "who", "whom", "this", "that", "these", 
            "those", "am", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had", "having", "do", 
            "does", "did", "doing", "a", "an", "the", "and", "but", "if", "or", "because", "as", "until", "while", 
            "of", "at", "by", "for", "with", "about", "against", "between", "into", "through", "during", "before", 
            "after", "above", "below", "to", "from", "up", "down", "in", "out", "on", "off", "over", "under", "again", 
            "further", "then", "once", "here", "there", "when", "where", "why", "how", "all", "any", "both", "each", 
            "few", "more", "most", "other", "some", "such", "no", "nor", "not", "only", "own", "same", "so", "than",
            "too", "very", "s", "t", "can", "will", "just", "don", "should", "now","%","people","sister","aaa","lot",
            "owls","love","wife","mom","son","friend","thanks","nails","daughter","name","friends"]


"""Load the pre-trained NLP model in spacy"""
import en_core_web_lg

nlp=spacy.load("en_core_web_lg") 
nlp.max_length=141690237

"""Define a function to extract keywords"""
def get_aspects(x):
    doc=nlp(x) ## Tokenize and extract grammatical components
    doc=[i.text for i in doc if i.text not in stop_words and i.pos_=="NOUN"] ## Remove common words and retain only nouns
    doc=list(map(lambda i: i.lower(),doc)) ## Normalize text to lower case
    doc=pd.Series(doc)
    doc=doc.value_counts().index.tolist()[:15] ## Get 15 most frequent nouns
    return doc

"""data=""
for i in range(7):
    data = data+" "+reviews[i].text"""


data={}
for i in range(len(reviews)):
    x = reviews[i].asin
    y = reviews[i].text
    if(x in data.keys()):
        data[x] = data[x]+" "+y
    else:
        data[x]=y

#Apply the function to get aspects from reviews
tags={}
for k in data.keys():
    tags[k]=get_aspects(data[k])

"""just for checking
from difflib import get_close_matches
l = []
a = tags['120401325X']
for i in range(15):
    word = a[i]
    if word not in l:  
        x = get_close_matches(word, list(set(a)-set([word])), cutoff=0.75, n=1)
        if(len(x)>0):
            l.append(x[0])
a = list(set(a)-set(l))"""


# for all the tags
for j in tags.keys():
    l = []
    a = tags[j]
    for i in range(len(a)):
        word = a[i]
        if word not in l:  
            x = get_close_matches(word, list(set(a)-set([word])), cutoff=0.75, n=1)
            if(len(x)>0):
                l.append(x[0])
    a = list(set(a)-set(l))
    updated_tags[j] = a
    
