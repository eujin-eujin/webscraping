 # Importing required libraries

import pandas as pd
import re
import requests as req
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import random


class Amazon():
    
    data_list = [] # Class variable to store the scraped data
    sleep_time = random.uniform(1,5)
    # Class constructor to initialize instance variables    
    def __init__(self,url,header,driver,query):
        self.url = url
        self.header = header
        self.driver = driver
        self.query = query
        self.df = None
    
    # Method to get HTML content of the Amazon search results page
    def get_html(self):
        page = self.driver.get(self.url)
        sleep(3)
        search_bar = self.driver.find_element(By.XPATH,'//*[@id="twotabsearchtextbox"]')
        search_bar.send_keys(self.query[0])
        search_bar.send_keys(Keys.RETURN)
        html = self.driver.page_source
        sleep(self.sleep_time)
        self.driver.close()
        return html 
    
    # Method to scrape data from the HTML content of a search results page
    def get_product_data(self,html):
        soup = bs(html,'lxml')
        products = soup.find_all('div',attrs={'data-asin':re.compile(r'[A-Z0-9]{10}')})
        
        for product in products:
            try:
                pattern = re.compile(r'data-asin="(\w{10})')
                asin_no = re.search(pattern,str(product)).group(1)
            except:
                asin_no = ''
            try:
                product_url = self.url+product.find('a',class_='a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal')['href']
            except : 
                product_url = ''
            try:
                title = product.find('span',class_='a-size-medium a-color-base a-text-normal').text.strip()
            except: 
                title = ''
            try :    
                symbol = product.find('span',class_='a-price-symbol').text.strip()
            except:
                symbol = ''
            try:
                price = symbol+product.find('span',class_='a-price-whole').text.strip()
            except:
                price = ''
                
            try: 
                out_of_5 = product.find('span',class_='a-icon-alt').text.strip()
            except: 
                out_of_5 = ''
            try: 
                total_ratings = product.find('span',class_='a-size-base s-underline-text').text.strip()[1:-1]
            except:
                total_ratings = ''
            data = {
            'product url':product_url,
            'asin':asin_no,
            'title' : title,
            'price' : price,
            'total ratings':total_ratings,
            'out of 5':out_of_5
            }
            
            self.data_list.append(data) # appending data into data_list
        
        
        #pagination
        next_page = soup.find('a',attrs={'class':'s-pagination-item s-pagination-next s-pagination-button s-pagination-separator'})
        if next_page is not None:
            html_ = req.get(self.url+next_page['href'],headers=self.header)
            sleep(self.sleep_time)
            self.get_product_data(html_.text)
            
    # Method to scrape data from all the search results pages        
    def scrape_data(self):
        html = self.get_html()
        self.get_product_data(html)
        
    # Method to save the scraped data to a CSV file    
    def save(self):
        df = pd.DataFrame(self.data_list)
        #csv = df.to_csv('digital_products.csv',index=False)
        print(df)
        self.df = df
    



if __name__=='__main__':
    URL = 'https://amazon.in/'
    HEADER = {
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
}

    # Create a ChromeOptions object
    chrome_options = Options()

    # set up Chrome options

    chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36')
    chrome_options.add_argument('--headless') 

    # set up Chrome service and driver
    chrome_service = Service(executable_path='ex:user/name/downloads/chromedriver') # use your chrome driver path here
    chrome_service.start()
    DRIVER = webdriver.Chrome(service=chrome_service, options=chrome_options)
    
    
    query = ['camera']
    amazon = Amazon(URL,HEADER,DRIVER,query)
    amazon.scrape_data()
    amazon.save()
    
