# Amazon Product Scraper
This Python script scrapes data from Amazon's search results page for a given list of search queries and stores it in a Pandas DataFrame.
## Prerequisites
Before running the script, make sure to install the following libraries:
* pandas 
* beautifulSoup4
* regex
* selenium
You also need to have the Chrome web browser installed on your machine.

## USage 
To use the scraper, create an instance of the Amazon class with the following parameters:
* 'url': The base URL of Amazon's website for your region (e.g. 'https://amazon.com' for the US site).
* 'header': A dictionary of headers to send with the requests (e.g. user agent).
* 'driver': The Selenium webdriver instance to use for scraping.
* 'query': A list of search queries to scrape data for.
