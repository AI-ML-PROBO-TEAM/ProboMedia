# -*- coding: utf-8 -*-
"""
Created on Tue Jun  6 10:34:10 2023

@author: pandy
"""

from flask import Flask, request, jsonify, render_template
from transformers import BartTokenizer, BartForConditionalGeneration ,AutoTokenizer, AutoModelForSeq2SeqLM
from pygooglenews import GoogleNews
from newspaper import Article
from bs4 import BeautifulSoup
import requests
import concurrent.futures
import urllib3
import pandas as pd



app = Flask(__name__)

# Initialize the BART model and tokenizer

model_name = 'facebook/bart-large-cnn'
tokeniz = BartTokenizer.from_pretrained(model_name)
summodel = BartForConditionalGeneration.from_pretrained(model_name)




# Get the list of free proxies
proxies = []

def get_proxies():
    global proxies
    r = requests.get('https://free-proxy-list.net/')
    soup = BeautifulSoup(r.content, 'html.parser')
    table = soup.find('tbody')
    for row in table:
        if row.find_all('td')[4].text == 'elite proxy':
            proxy = ':'.join([row.find_all('td')[0].text, row.find_all('td')[1].text])
            proxies.append(proxy)



# Fetch an article using a proxy
def fetch_article(url):
    try:
        # Rotate through proxies in a round-robin manner
        proxy = proxies.pop(0)
        proxies.append(proxy)
        proxy_dict = {
            'http': proxy,
            'https': proxy
        }

        session = requests.Session()
        adapter = requests.adapters.HTTPAdapter(pool_connections=100, pool_maxsize=100)
        pool = urllib3.HTTPConnectionPool(url, maxsize=100)
        session.mount(url, pool)
        session.proxies = proxy_dict

        article = Article(url, language='en')
        article.session = session
        article.download()
        article.parse()

        return article

    except Exception as e:
        # Handle specific exception if needed
        print(f"An error occurred while fetching the article: {str(e)}")
        return None

# Summarize the content of an article using BART model
def summarize_content(text):
    inputs = tokeniz([text], max_length=1024, truncation=True, return_tensors='pt')
    summary_ids = summodel.generate(inputs['input_ids'], num_beams=4, max_length=150, early_stopping=True)
    summarized_text = tokeniz.decode(summary_ids[0], skip_special_tokens=True)
    return summarized_text


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/news', methods=['POST'])
def get_news():
    try:
        # Get the request JSON data
        keyword = request.form['keyword']

        # Initialize GoogleNews object
        gn = GoogleNews(lang='en', country='in')
        search = gn.search(keyword, when='1h')

        # Extract relevant information from search results
        news_list = []
        article_count = 0  # Counter to track the number of articles processed

        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = []
            for entry in search['entries']:
                if article_count == 2:
                    break  # Exit the loop once 20 articles have been processed

                future = executor.submit(fetch_article, entry.link)
                futures.append(future)
                article_count += 1  # Increment the counter

            for future, entry in zip(futures, search['entries']):
                try:
                    article = future.result()
                    if article:
                        print(article.text)
                        summarized_content = summarize_content(article.text)
                        tex=article.text
                        news = {
                            'title': article.title,
                            'link': entry.link,
                            'summary': summarized_content
                        }
                        news_list.append(news)

                except Exception as e:
                    # Handle specific exception if needed
                    error_message = f"An error occurred while processing an article: {str(e)}"
                    print(error_message)
        
        df = pd.DataFrame(news_list)
        df.to_csv('news_data.csv', index=False)
        # Render the template with news data
        return render_template('news.html', news_list=news_list)
    
    except Exception as e:
        # Handle other exceptions
        error_message = f"An error occurred: {str(e)}"
        print(error_message)
        return jsonify({'error': error_message})


if __name__ == '__main__':
    get_proxies() 
    app.run(host='127.0.0.1',port=8006,debug=False)
