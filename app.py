from flask import Flask, request, jsonify
from pygooglenews import GoogleNews

app = Flask(__name__)

@app.route('/news', methods=['POST'])
def get_news():
    # Get the request JSON data
    request_data = request.get_json()
    country = request_data.get('country')
    keyword = request_data.get('keyword')

    # Initialize GoogleNews object
    gn = GoogleNews(lang='en', country=country)

    search = gn.search(keyword, when='1h')

    # Extract relevant information from search results
    news_list = []
    for entry in search['entries']:
        news = {
            'title': entry.title,
            'link': entry.link,
        }
        news_list.append(news)

    # Create a dictionary with the extracted news information
    response_dict = {'news': news_list}

    # Return the response as JSON
    return jsonify(response_dict)

if __name__ == '__main__':
    app.run(debug=False)
