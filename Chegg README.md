# Chegg Q&A Crawler for Mathematics Field (In Progress)
This program is a web scraper that collects Q&A questions from the Chegg website, specifically for the mathematics field. The scraped data includes the question text and any images associated with the question.

## Required Libraries
The following libraries are used in this project:
* pandas
* re
* beautifulsoup
* requests
* time 
* random
## Chegg Class
The Chegg class is defined to crawl the Q&A questions for only the mathematics field. It includes the following methods:

### init(self, url, headers)
This method initializes the class attributes. The url and headers parameters are required to make a request to the Chegg website.

### start_request(self)
This method sends the request to the URL specified in the url parameter sent through the class instance.

### url_parse(self, response)
This method parses the respective tag for subject links.

### request_maths_urls(self)
This method collects the URLs of the mathematics field.

### get_math_archive_link(self)
This method gets the archive URL of all mathematics contents for several years.

### getting_branch_urls(self)
This method gets the branch URLs and returns a list of URLs.

### getting_years(self, branch_urls)
This method gets the year list, whereas there is data for more than ten years.

### getting_month_urls(self, year_list)
This method gets the month URLs for each year.

### getting_day_urls(self, month_urls)
This method gets the day URLs for each month.

### getting_content(self, day_urls)
This method collects the main content URLs and calls the parse_content function to do the parsing and creating the data frame.

### parse_math_content(self, url, answer_status)
This method parses the math question text and downloads the images.

### save(self)
This function exports the dataframe to a CSV file.

### verify_status(self, answer_status)
This function checks whether the question has been answered or not. It takes in a parameter answer_status, which is a string containing '0' if the question is unanswered and '1' if the question is answered.

### download_image(self, url)
This function downloads the image from the provided URL. It takes in a parameter url, which is the URL of the image to be downloaded. The downloaded image is saved in the 'images' folder.

### make_url(self, link, previous_url='')
This function joins the relative URLs to the domain. It takes in two parameters, link and previous_url (optional). The link parameter contains the relative URL to be joined, while the previous_url parameter contains the URL of the previous page.

### start_crawl(self)
This is the main function that initiates the web scraping process. It starts by sending a request and parsing the response to get the subject URLs. It then retrieves the math archive link, branch URLs, year list, month URLs, day URLs, and content URLs.

## Usage
To use this program, you will need to instantiate the Chegg class and pass the URL and headers as arguments. Then, you can call the start_crawl method to scrape the Q&A questions. The data will be saved in a Pandas data frame.

## Note: 
this project isn't completed yet since we have just fetched content urls this has works to do get complete

