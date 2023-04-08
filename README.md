# Flask Stock Dashboard
### This is a Flask web application that provides a stock dashboard for a given stock symbol. It includes historical stock data visualization, prediction of stock prices, evaluation of the model's prediction, and a news feed for the stock.

[![Check it out live][run_img]][run_link]

[run_img]: https://storage.googleapis.com/cloudrun/button.svg
[run_link]: https://movie-recommender-pssahwnxxa-pd.a.run.app

## Getting Started

````
pip install -r requirements.txt
````

Next, you will need to start the Flask server by running the following command:

````
python main.py
````
This will start the server on `http://localhost:5000/`, where you can access the movie recommendation system.
## To deploy this app on Google Cloud
````
gcloud run deploy
````
## Usage

Enter a stock symbol in the search bar and click on the search button to view the dashboard.

## Features

The homepage redirects to the Market page, which displays the dashboard for the default stock symbol along with predictions.

The Market page shows a dashboard that includes a historical stock price chart, a prediction of future prices, and a news feed for the stock.

The Evaluation page shows the evaluation of the model's prediction for the stock symbol for the past 20 days along with actual movement

The News page displays the latest news articles related to the stock symbol.

The user can search for a different stock symbol using the search bar on the top of the Market, Evaluation, and News pages.

## Acknowledgements
This application was created by Yash Sawnat as a project for Capstone 2 in Durham College's Artifical Intelligence Design and Analysis Program. It uses data from YFinance for stock information.