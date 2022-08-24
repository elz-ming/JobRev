#IMPORT_ANTS#
import praw
from praw.models import MoreComments

import pandas as pd

import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

import string

import os.path

from datetime import date

#INITIATING REDDIT
reddit = praw.Reddit(
    client_id="bfx8ExsQXjGUptX6jLA5Rg",
    client_secret="fwnSOPiCXFTv4JtKSX9iqLd3r40YcA",
    user_agent="Scraper1",
)

#GETTING HOT POST
hot_posts = reddit.subreddit('Jobs').hot()

post_list = []

for post in hot_posts:
    post_list.append([post.id, post.score, post.num_comments, post.title, post.selftext])


post_df = pd.DataFrame(post_list, columns=['id','score','comm_num','title','body'])

post_df = post_df.sort_values('score',ascending=False).reset_index()
post_df.drop(['index'], axis=1, inplace=True)

top_subm_id = post_df['id'][0]
submission = reddit.submission(id=top_subm_id)

word_list = []
sent_list = []

submission.comments.replace_more(limit=0)
for comm in submission.comments:
    
    #1 - Lower-casing
    comment = comm.body.lower()
    
    #2 - Tokenize and removing punctuations
    tokenizer = nltk.RegexpTokenizer(r'\w+')
    clean_word = tokenizer.tokenize(comment)
    
    #3 - Removing singular characters and returning sentence
    words_wout_alphabets = []
    for w in clean_word:
        if w not in list(string.ascii_lowercase):
            words_wout_alphabets.append(w)
    clean_sent = ' '.join(words_wout_alphabets)
    sent_list.append(clean_sent)
    
    #4 - Removing stopwords
    stopword = stopwords.words('english')
    words_wout_stopwords = []
    for w in words_wout_alphabets:
        if w not in stopword:
            words_wout_stopwords.append(w)
    
    #5 - Lemmatization
    lemmatizer = WordNetLemmatizer()
    for w in words_wout_stopwords:
        word_list.append(lemmatizer.lemmatize(w))

Subm_Today = {
    "date" : str(date.today()),
    "id" : post_df['id'][0],
    "score" : int(post_df['score'][0]),
    "title" : post_df['title'][0],
    "body" : post_df['body'][0],
    "sent_num" : len(sent_list),
    "sent_str" : str(sent_list),
    "word_num" : len(word_list),
    "u_word_num" : len(set(word_list)),
    "word_str" : str(word_list),
}

to_save = pd.DataFrame(Subm_Today,index=[0])

if  os.path.isfile('DataFile/Reddit_Top_Submission.csv'):
    df = pd.read_csv('DataFile/Reddit_Top_Submission.csv')
    df_updated = pd.concat([df,to_save])
else:
    df_updated = to_save
df_updated.to_csv('DataFile/Reddit_Top_Submission.csv',index=False)


import tkinter as tk 

root= tk.Tk() 
 
canvas1 = tk.Canvas(root, width = 300, height = 300)
canvas1.pack()

label1 = tk.Label(root, text='There is a new scrape!')
canvas1.create_window(150, 150, window=label1)

root.mainloop()