# from django.shortcuts import render

# ========== JOBSTREET SCRAPER ========== #

def jsscraper1():
    # ========== IMPORT-ANTS ========== #
    from selenium import webdriver
    from webdriver_manager.chrome import ChromeDriverManager
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.common.by import By

    from bs4 import BeautifulSoup
    
    import pandas as pd

    import time

    url = 'https://www.jobstreet.com.my/en/companies/browse-reviews'
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get(url) 

    counter = 0
    while counter < 100:
        try:
            driver.find_element(By.CLASS_NAME, 'Gk2xjdpX_s0S3hsfi__X').click()
            counter += 1
            try:
                time.sleep(2)
                driver.find_element(By.CLASS_NAME, 'gwCwc3YZYufjgIcBtu0l').click()
            except:
                continue
        except:
            break

    soup = BeautifulSoup(driver.page_source, 'html.parser')

    all_company_info = soup.find_all(name="div", class_="_WfdmOZ2wLBd0x_TFyKO")

    company_list = []
    company_url_list = []
    company_rating = []

    for i in range(len(all_company_info)):
        company_list.append(all_company_info[i].find(name="a", class_="_9d6_WXgVpZWn7HaXEgs").getText())

    ## Get company jobstreet main url
    endpoint = "https://www.jobstreet.com.my"
    for i in range(len(all_company_info)):
        company_url_list.append(endpoint + all_company_info[i].find(name="a", class_="_9d6_WXgVpZWn7HaXEgs")["href"])


    for i in range(len(all_company_info)):
        company_rating.append(float(all_company_info[i].find_all(name="span", class_="j6BF91AmxWn9vS_m399j")[1].getText().split("out")[0]))

    data = {
        "company_name" : company_list,
        "company_js_url" : company_url_list,
        "company_rating" : company_rating
    }

    df = pd.DataFrame(data=data)
    
    return df

def jsscraper2(Dataframe):
    # ========== IMPORT-ANTS ========== #    
    from bs4 import BeautifulSoup
    import pandas as pd
    import requests

    df = Dataframe

    five_star_list = []
    four_star_list = []
    three_star_list = []
    two_star_list = []
    one_star_list = []
    salary_rate_list = []
    recommendation_rate_list = []

    for url in df['company_js_url']:
        response = requests.get(url)
        data = response.text
        soup = BeautifulSoup(data, "html.parser")

        try:
            salary_rate = soup.find_all(name="div", class_="RL2EfHhuwPsO8xlgwG_S")[0].getText()
            salary_rate_list.append(salary_rate)
        except:
            salary_rate_list.append("No Info")

        try:
            recommendation_rate = soup.find_all(name="div", class_="RL2EfHhuwPsO8xlgwG_S")[1].getText()
            recommendation_rate_list.append(recommendation_rate)
        except:
            recommendation_rate_list.append("No Info")

        try:
            five_star = soup.find_all(name="span", class_="DCaw56gNq5O1IBoC5xcz")[0].getText()
            five_star_list.append(five_star)
        except:
            five_star_list.append("0")

        try:
            four_star = soup.find_all(name="span", class_="DCaw56gNq5O1IBoC5xcz")[1].getText()
            four_star_list.append(four_star)
        except:
            four_star_list.append("0")

        try:
            three_star = soup.find_all(name="span", class_="DCaw56gNq5O1IBoC5xcz")[2].getText()
            three_star_list.append(three_star)
        except:
            three_star_list.append("0")

        try:
            two_star = soup.find_all(name="span", class_="DCaw56gNq5O1IBoC5xcz")[3].getText()
            two_star_list.append(two_star)
        except:
            two_star_list.append("0")

        try:
            one_star =  soup.find_all(name="span", class_="DCaw56gNq5O1IBoC5xcz")[4].getText()
            one_star_list.append(one_star)
        except:
            one_star_list.append("0")

    df["five_star_rating"] = five_star_list
    df["four_star_rating"] = four_star_list
    df["three_star_rating"] = three_star_list
    df["two_star_rating"] = two_star_list
    df["one_star_rating"] = one_star_list
    df["salary_rate"] = salary_rate_list
    df["recommendation_rate"] = recommendation_rate_list
    
    return df


# ========== REDDIT SCRAPER ========== #
def rscraper1():
    # ========== IMPORT-ANTS ========== #
    import praw

    import pandas as pd

    reddit = praw.Reddit(
        client_id="bfx8ExsQXjGUptX6jLA5Rg",
        client_secret="fwnSOPiCXFTv4JtKSX9iqLd3r40YcA",
        user_agent="Scraper1",
    )

    hot_posts = reddit.subreddit('Jobs').hot()

    post_list = []

    for post in hot_posts:
        post_list.append([post.id, post.score, post.num_comments, post.title, post.selftext])


    post_df = pd.DataFrame(post_list, columns=['id','score','comm_num','title','body'])

    post_df = post_df.sort_values('score',ascending=False).reset_index()
    post_df.drop(['index'], axis=1, inplace=True)
    
    top_subm_info = post_df.iloc[0].to_dict()

    return top_subm_info

def rscraper2(TopSubmInfoDict):
    # ========== IMPORT-ANTS ========== #
    import praw
    from praw.models import MoreComments

    import nltk
    from nltk.corpus import stopwords
    from nltk.stem import WordNetLemmatizer


    import string

    import pandas as pd
    import re

    reddit = praw.Reddit(
            client_id="bfx8ExsQXjGUptX6jLA5Rg",
            client_secret="fwnSOPiCXFTv4JtKSX9iqLd3r40YcA",
            user_agent="Scraper1",
            )

    top_id = TopSubmInfoDict['id']
    submission = reddit.submission(id=top_id)

    comment_list = []

    submission.comments.replace_more(limit=0)
    for comm in submission.comments:

        #1 - Lower-casing
        comment = comm.body.lower()

        #2 - Tokenize and removing punctuations
        tokenizer = nltk.RegexpTokenizer(r'\w+')
        clean = tokenizer.tokenize(comment)

        #3 - Removing stopwords and singular characters
        stopword = stopwords.words('english')
        stopword = stopword + list(string.ascii_lowercase)
        word_list = []
        for word in clean:
            if word not in stopword:
                word_list.append(word)

        #4 - Lemmatization
        lemmatizer = WordNetLemmatizer()
        for w in word_list:
            comment_list.append(lemmatizer.lemmatize(w))

    return comment_list

def rplot1(comment_list):
    from nltk.probability import FreqDist
    import matplotlib as pl
    %matplotlib inline
    import matplotlib.pyplot as plt

    fdist=FreqDist(comment_list)
    fdist.plot(20,cumulative=False)

def rplot2(comment_list):
    from wordcloud import WordCloud, ImageColorGenerator

    import matplotlib as pl
    %matplotlib inline
    import matplotlib.pyplot as plt
    
    import numpy as np
    
    from PIL import Image
    
    # Because WordCloud takes in string but not list
    comment_string = ' '.join(comment_list)
    
    # Mask with a RM50 bill
    mask = np.array(Image.open('./RM100.jpg')) 
    color= ImageColorGenerator(mask)
    
    # WordCloud settings
    wordcloud=WordCloud(
        background_color='white', 
        max_font_size=200,
        max_words=1000,
        mask=mask,
        random_state=42,
        repeat=True,
        )
    
    # WordCloud generator
    wordcloud.generate(comment_string)
    
    # WordCloud plotter
    plt.figure(figsize=(10,10))
    plt.axis('off')
    plt.imshow(wordcloud.recolor(color_func=color), interpolation="bilinear")
    plt.show()

# ========== MAIN() ========== #

def jsmain():
    jsscraper2(jsscraper1())
    return None

def rmain():
    comment_list = rscraper2(rscraper1())
    rplot1(comment_list)
    rplot2(comment_list)



    