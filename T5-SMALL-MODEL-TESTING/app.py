# -*- coding: utf-8 -*-
"""
Created on Tue Jun  6 10:34:10 2023

@author: pandy
"""

from flask import Flask, request, jsonify, render_template
from transformers import T5Tokenizer, T5ForConditionalGeneration ,AutoTokenizer, AutoModelForSeq2SeqLM
from pygooglenews import GoogleNews
from newspaper import Article
from bs4 import BeautifulSoup
import requests
import concurrent.futures
import urllib3
import openai
from rouge import Rouge
import pandas as pd

app = Flask(__name__)
openai.api_key = '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'

# Initialize the T5 SMALL model and tokenizer

tokeniz = T5Tokenizer.from_pretrained('t5-small')
summodel = T5ForConditionalGeneration.from_pretrained('t5-small')


def generate_summary(text):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=text,
        max_tokens=150,
        temperature=0.3,
        top_p=0.9,
        n=1,
        stop=None,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )
    summary = response.choices[0].text
    return summary

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



def calculate_rouge(reference_summary, generated_summary):
    rouge = Rouge()
    scores = rouge.get_scores(generated_summary, reference_summary)
    return scores[0]['rouge-1']['f'], scores[0]['rouge-2']['f'], scores[0]['rouge-l']['f']

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


# Summarize the content of an article using T5 model
def summarize_content(text):
    preprocess_text = "summarize: " + text
    inputs = tokeniz.encode(preprocess_text, return_tensors='pt', max_length=512, truncation=True)
    summary_ids = summodel.generate(inputs, max_length=200, min_length=40, length_penalty=2.0, num_beams=4, early_stopping=True)
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
                if article_count == 20:
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
                        sud='summmarize it'
                        #questions = generate_question(summarized_content)
                        reference_summary=generate_summary(tex + ' %s'%sud)
                        print('moka :-',reference_summary)
                        rouge_1, rouge_2, rouge_l = calculate_rouge(reference_summary, summarized_content)
                        news = {
                            'title': article.title,
                            'link': entry.link,
                            'summary': summarized_content,
                            #'questions': questions,
                            'rouge_1': rouge_1,
                            'rouge_2': rouge_2,
                            'rouge_l': rouge_l
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
