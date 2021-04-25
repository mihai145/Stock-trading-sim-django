# Trading - general description
This Django application tries to imitate an online broker. Non-authenticated users can search for and analize certain stocks, and authenticated users can put money into their investment account, buy and sell shares and track their transaction history.

## Distinctiveness and Complexity
This project is based on Finnhub’s API. It contains data about 65000 companies. The backend makes requests to this API in order to provide realistic data for the application.\
This project is fully mobile-responsive (as shown in the recorded screencast). For this, the frontend uses Bootstrap 4’s grid layout functionalities.\
This project uses Django and it has 3 models (one representing user data, one representing stock ownership and the third representing transaction data). JavaScript is used on the frontend in order to enable users to put money into their investment account, buy and sell shares without refreshing the page.

## Project Structure
This Django project consists of a single application called Stocks. Inside the Stocks directory, one may find the following:
* models.py that contains the three models used by the application (User, Stocks and Transaction)
* urls.py that contains the url patterns for the application
* views.py that contains the logic for handling the requests
* a templates folder that contains the layout.html file (this file provides a general structure for the interface of the entire application, including a collapsing Bootstrap Navbar that has a search field for stock tickers) and other html files representing different views (such as index.html or profile.html)
* a static folder that contains the styles.css file and four other javascript files (adjustPrices.js - calculates the price per share after commission, invest.js - enables the user to add funds to the investment account without refreshing the page, buy.js and sell.js - enables the user to buy or sell shares without refreshing the page)

## How to run this application
Download the code, then run the following commands:\
python manage.py makemigrations\
python manage.py migrate

Then, go to https://finnhub.io/ and register for a free API key. Open the file stocks/views.py and replace YOUR_API_KEY from lines 33 and 134 with your own API key from Finnhub.

Then, you can start the application with:\
python manage.py runserver
