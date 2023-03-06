# Amazon Product Scraper
This script scrapes the search results page of Amazon.in for digital products using the provided search queries and saves the scraped data to a CSV file.## Prerequisites
Before running the script, make sure to install the following libraries:
* pandas 
* beautifulSoup4
* re
* time
* requests
You also need to have the Chrome web browser installed on your machine.

## USage 
To use the scraper, create an instance of the Amazon class with the following parameters:
* 'url': The base URL of Amazon's website for your region (e.g. 'https://amazon.com' for the US site).
* 'header': A dictionary of headers to send with the requests (e.g. user agent).
* 'driver': The Selenium webdriver instance to use for scraping.
* 'query': A list of search queries to scrape data for.
## export 
to save the data in to csv use method amazon.save()

# Disclaimer
This script is for educational purposes only. Scraping Amazon's website may violate their terms of service. Use at your own risk.




