# Flask News API Endpoint

This is a Flask web application that provides a news API endpoint for retrieving recent news articles based on a specific country and keyword. It utilizes the pygooglenews library to perform the news search.

The application exposes a single route /news, which accepts POST requests. The request payload should be a JSON object containing the country and keyword fields. The country field specifies the country for which the news articles should be retrieved, and the keyword field specifies the search keyword.

The application initializes a GoogleNews object with the specified country and language parameters. It then performs a search using the provided keyword, restricting the results to articles published within the last hour.

The relevant information from the search results, such as the title and link of each article, is extracted and stored in a list of dictionaries. Finally, the extracted news information is packaged into a response dictionary and returned as JSON.

To run the application, you can execute the script containing this code. By default, the Flask application runs on http://localhost:5000. You can modify the debug parameter in app.run() to control the debugging mode.

# Testing the Flask Code using Postman

To check if the provided Flask code is working using Postman, follow these steps:

* Make sure you have Postman installed on your system. If not, you can download and install it from the official Postman website: https://www.postman.com/downloads/.

* Once the Flask application is running, open Postman.

* Create a new request by clicking on the "New" button in Postman's interface.

* Set the request type to "POST".

* Enter the URL for the Flask API endpoint in the address bar. For example, if the Flask application is running locally, use http://localhost:5000/news as the URL.

* In the request body, select the "raw" option and set the body format to JSON.

* Provide the required parameters in JSON format. You can choose only two countries for now for US it is "us" and for india it is "in" For example:
{
  "country": "us",
  "keyword": "technology"
}
* Click on the "Send" button to send the POST request to the Flask API endpoint.

* Postman will display the response received from the Flask application. If everything is working correctly, you should see a JSON response containing a list of news articles.
* The server is running on `http://165.343.188.124:8000/news`. you can check on postman just replace  http://localhost:5000/news with http://165.343.188.124:8000/news







