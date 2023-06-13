# News Summarization Flask App

This Flask application is designed to scrape news articles, summarize their content using the BART model, and calculate Rouge scores for evaluation. The application uses the Google News API, the transformers library for BART model usage, and other supporting libraries such as pygooglenews, newspaper, BeautifulSoup, requests, concurrent.futures, urllib3, openai, pandas, and rouge.

## BART (Bidirectional and Auto-Regressive Transformers)

BART (Bidirectional and Auto-Regressive Transformers) is a transformer-based model architecture that is commonly used for text generation tasks, including text summarization. It is pretrained on large amounts of data and can be fine-tuned for specific downstream tasks.

The BART model consists of an encoder-decoder architecture, where the encoder processes the input text and extracts its contextual representations, and the decoder generates the target text based on these representations. BART utilizes a combination of masked language modeling (MLM) and denoising autoencoding (DAE) objectives during pretraining, enabling it to handle both conditional and unconditional generation tasks.

In this Flask application, the BART model is used for text summarization. Given a news article, BART is used to generate a concise summary of the article's content. The model is initialized and loaded using the facebook/bart-large-cnn pre-trained weights, and the transformers library is used for tokenization and decoding of the generated summaries.

You can customize the BART model by changing the model_name, tokeniz, and summodel variables in the code to experiment with different pretrained models or fine-tuned variants based on your requirements.

## Rouge (Recall-Oriented Understudy for Gisting Evaluation)

Rouge (Recall-Oriented Understudy for Gisting Evaluation) is a set of evaluation metrics commonly used in natural language processing and text summarization tasks. Rouge measures the quality of a summary by comparing it to one or more reference summaries and calculating the overlap or similarity between them.

The Rouge metrics include Rouge-1, Rouge-2, and Rouge-L, which evaluate the unigram, bigram, and longest common subsequence (LCS) overlap between the generated summary and the reference summary. These metrics provide a measure of the precision, recall, and F1 score of the generated summary compared to the reference summaries.

In this Flask application, Rouge scores are calculated to evaluate the quality of the generated summaries. The rouge library is used to compute the Rouge-1, Rouge-2, and Rouge-L scores based on the generated summary and the reference summary. The scores are then displayed alongside the summaries to provide an objective measure of their quality.

You can further explore the Rouge metrics and adjust the evaluation criteria according to your specific needs by modifying the calculate_rouge() function in the code.


## Features

- Scrapes news articles based on user-defined keywords using the Google News API.
- Summarizes the content of each article using the BART model.
- Calculates Rouge scores (Rouge-1, Rouge-2, Rouge-L) to evaluate the quality of the summaries.
- Renders the summarized news articles along with their summaries and Rouge scores on a web page.

- pip install -r requirements.txt

## Usage

1. Clone the repository or download the code files.
2. Download Anaconda for Windows from the official Anaconda website (https://www.anaconda.com/products/individual#windows) and follow the installation instructions.
3. Once the download is finished, open Anaconda Prompt or Anaconda PowerShell from the Start menu.
4. In the Anaconda Prompt or Anaconda PowerShell, create a new environment using the following command: 
`conda create --name myenv python=3.8`
5. Activate the newly created environment using the command: 
`conda activate myenv`
6. navigate to the project directory.
7. Install the required libraries by following the command
`pip install -r requirements.txt`
8. Run the Flask application using the following command: `python app.py`
9. Open a web browser and go to `http://localhost:8006` to access the application.
10. Enter a keyword in the search field and click the "Search" button.
11. The application will scrape news articles related to the keyword, summarize their content, and display them on the web page.
12. The summaries will be evaluated using Rouge scores, and the scores will be displayed alongside the summaries.
13. You can modify the code to customize the summarization model, API usage, or any other aspect according to your requirements.

## Additional Notes

- The application uses the BART model for summarization. You can change the model by modifying the `model_name`, `tokeniz`, and `summodel` variables in the code.
- The code includes functionality to fetch and rotate through free proxies for web scraping. You can disable or modify this feature as per your needs.
- Error handling is implemented to handle exceptions that may occur during web scraping or summarization. You can customize the error handling as per your requirements.

