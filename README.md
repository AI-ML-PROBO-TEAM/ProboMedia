# Media
The  Media project is a comprehensive initiative aimed at exploring and harnessing the power of digital technologies in the realm of media. It encompasses various aspects of  media production, distribution, and consumption, with a focus on leveraging innovative tools and platforms to create, share, and engage with content in the digital landscape.
The primary objectives of the media project are:

# Content Creation and Production
The project aims to enable the creation of high-quality media content across various formats such as videos, images, audio, and interactive experiences. It encompasses techniques like digital storytelling, graphic design, video editing, sound production, and animation to produce engaging and visually appealing content.

**Digital Distribution and Publishing:**
The project focuses on exploring digital channels and platforms for the distribution and publishing of media content. This includes leveraging social media platforms, websites, streaming services, and mobile applications to reach and engage with a wide audience. The project also involves strategies for search engine optimization (SEO), content promotion, and audience targeting to maximize the reach and impact of the media assets.

**Audience Engagement and Interaction:** 
The project places significant emphasis on fostering active audience participation and interaction with media content. This involves incorporating interactive elements, user-generated content, social sharing features, and community building aspects to enhance user engagement and encourage dialogue between content creators and consumers.

**Analytics and Insights:** 
The media project incorporates data analytics and measurement tools to gather insights and track the performance of media assets. It utilizes metrics such as views, likes, shares, comments, and user behavior to assess the effectiveness of content strategies, identify trends, and make data-driven decisions to optimize content creation and distribution.

**Emerging Technologies and Trends:** 
The project remains attuned to the rapidly evolving media landscape and explores emerging technologies and trends. It investigates cutting-edge technologies like virtual reality (VR), augmented reality (AR), artificial intelligence (AI), and machine learning (ML) to explore their potential applications in enhancing the media experience.

Overall, the media project aims to empower content creators, publishers, and consumers in the digital era by providing tools, strategies, and insights to navigate the evolving media landscape. By embracing digital technologies and leveraging innovative approaches, the project seeks to redefine how media content is created, distributed, and experienced in the digital realm.

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







