# Importing required libraries

import pandas as pd
import re
import requests as req
from bs4 import BeautifulSoup as bs
from time import sleep
import random


class Amazon():
    
    ''' this class is to scrape the amazon product 
    data like product name , price , title, ...'''
   
    data_list = [] # Class variable to store the scraped data
    sleep_time = random.uniform(1,5)
    
    # Class constructor to initialize instance variables    
    def __init__(self,url,header,query):
        self.url = url
        self.header = header
        self.query = query
        self.df = None
        self.session = req.Session()
     
   #thtis function just returns the html response
    def get_html(self):
        self.session.headers.update(self.header)
        html = self.session.get(self.make_url())
        sleep(self.sleep_time)
        return html 
    
    # this function joins the relative links to domain and returns main as links
    def make_url(self):
        split_query = self.query.split() # spliting each word in the search query
        url_ = self.url+'/s?k='
        for query in split_query: #concatenate the words with domain
            url_ = url_+query+'+'
        url_= url_[:-1]
        print(url_)
        return url_
    
    # Method to scrape the product details of the search results page
    def get_product_data(self,html):
        
        soup = bs(html.text,'lxml')
        products = soup.find_all('div',attrs={
        'data-asin':re.compile(r'\w{10}'),
        'data-index':re.compile(r'\d+')
        }) # to avoid the recommendation products get matched the parsing we are 
        #we are specificlly getting the searched result product alone
        
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
                title = product.h2.text.strip()
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
                out_of_5 = product.find('span',attrs={'aria-label':re.compile('out of 5')}).i.text.strip()
            except: 
                out_of_5 = ''
            try: 
                total_ratings = product.find('span',attrs={'aria-label':re.compile(r'^\d{1,3}(,\d{2,3})*$')}).text.strip()[1:-1]
            except:
                total_ratings = ''
                
            data = {
            'product url':product_url,
            'ASIN':asin_no,
            'title' : title,
            'price' : price,
            'total ratings':total_ratings,
            'out of 5':out_of_5
            }
            
            self.data_list.append(data) # appending data into data_list
        
        
        #pagination
        next_page = soup.find('a',attrs={'class':'s-pagination-item s-pagination-next s-pagination-button s-pagination-separator'})
        if next_page is not None:
            session = req.Session()
            
            html = self.session.get(self.url+next_page['href'])
            sleep(self.sleep_time)
            self.get_product_data(html)
            
            
    # Method to scrape data from all the search results pages        
    def scrape_data(self):
        html = self.get_html()
        self.get_product_data(html)
        
        
    # Method to save the scraped data to a CSV file    
    def save(self):
        df = pd.DataFrame(self.data_list)
        csv = df.to_csv('digital_products.csv',index=False)
        self.df = df
    



if __name__=='__main__':
    URL = 'https://amazon.in/'
    HEADER = {
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
}
    
    queries= ['smart hand band', 'smart watch', 'smart tag', 'wireless earbuds', 'bluetooth headphones',
              'portable speaker', 'streaming device', 'external hard drive', 'gaming laptop', 'gaming mouse', 
              'gaming keyboard', 'smartphone gimbal', 'action camera', 'smart doorbell', 'smart thermostat',
              'smart plug', 'smart light bulbs', 'robot vacuum cleaner', 'air purifier', 'smart water bottle']
    
    for query in queries : 
        amazon = Amazon(URL,HEADER,query) # Amazon class instance 
        amazon.scrape_data() # this method starts crawling
        sleep(amazon.sleep_time)
        
    #this saves the file as csv        
    amazon.save()

    
