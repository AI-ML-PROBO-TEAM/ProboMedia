# -*- coding: utf-8 -*-
"""
Created on Tue Jun  6 10:34:10 2023

@author: pandy
"""

from flask import Flask, request, jsonify, render_template
from transformers import PegasusForConditionalGeneration, PegasusTokenizer
from pygooglenews import GoogleNews
from newspaper import Article
from bs4 import BeautifulSoup
import requests
import concurrent.futures
import urllib3


app = Flask(__name__)


# Initialize the pegasus model and tokenizer

model_name = 'google/pegasus-xsum'
tokeniz = PegasusTokenizer.from_pretrained(model_name)
summodel = PegasusForConditionalGeneration.from_pretrained(model_name)

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

def summarize_content(text):
    inputs = tokeniz(text, truncation=True, padding='longest', return_tensors='pt')
    
    # Adjust the parameters for better summarization
    max_length = len(text)/4
    num_beams = 4
    length_penalty = 2.0
    no_repeat_ngram_size = 2
    
    summary = summodel.generate(
        inputs['input_ids'],
        max_length=max_length,
        num_beams=num_beams,
        length_penalty=length_penalty,
        no_repeat_ngram_size=no_repeat_ngram_size,
        early_stopping=True
    )
    
    summarized_text = tokeniz.decode(summary[0], skip_special_tokens=True)
    summarized_text = summarized_text.strip()
    
    return summarized_text
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
                if article_count == 5:
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
                        print('moka :-',summarized_content)
                        
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
        # Render the template with news data
        return render_template('news.html', news_list=news_list)
    
    except Exception as e:
        # Handle other exceptions
        error_message = f"An error occurred: {str(e)}"
        print(error_message)
        return jsonify({'error': error_message})


if __name__ == '__main__':
    get_proxies() 
    app.run(host='127.0.0.1',port=8008,debug=False)
