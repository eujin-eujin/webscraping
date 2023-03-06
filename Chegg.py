# importing required libraries here
from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
import re
import random
from time import sleep
import os


class Chegg():
    '''this chegg class is to crawl the Q&A questions for only mathematcis field'''

    # we are initializing the class attributes here
    def __init__(self, url, headers):
        self.url = url
        self.headers = headers
        self.session = requests.Session()
        self.url_dic = {}
        self.math_archive = None
        self.sleep_time = random.uniform(1, 5)  # to generate the randome number for random sleep
        self.data_list = []
        self.day_urls = []
        self.df = None

    # this function gives the request to url sent through the class instance
    def start_request(self):
        self.session.headers.update(self.headers)
        response = self.session.get(self.url)
        sleep(self.sleep_time)
        return response

    # this is url_parser function which parses the respected tag for subject_links
    def url_parse(self, response):
        soup = bs(response.text, 'lxml')
        subjects_container = soup.find_all(
            'a', class_='sc-1ecizwc-5 gjLkPS')  # we are selecting the all_subjects tag over here

        for subject in subjects_container:
            subject_name = subject.text.strip().lower()
            subject_url = subject['href']
            self.url_dic[subject_name] = self.make_url(
                subject_url)  # to join domain and relative link we the make_url func

    def request_maths_urls(self):
        # even we collected the all the field brances link we are gonna scrape questions from mathematics alone

        math_url = self.url_dic['math']
        response = self.session.get(math_url)
        sleep(self.sleep_time)
        return response

    # this will get the archive_url of the all math contents for several years
    def get_math_archive_link(self):
            response = self.request_maths_urls()
            soup = bs(response.text, 'lxml')
            more_q_a = soup.find('a', class_='more-qna-link')['href']
            self.math_archive = self.make_url(more_q_a)

            # this function pares the math question text and downloads the images by calling download_image_fucntion

    '''to reach the content url it has some process like
    getting branch,month,day urls and fetching them to reach the 
    contents posted for single day '''

    #this function gets the branch urls and returns list of urls
    def getting_branch_urls(self):
        response = self.session.get(self.math_archive)
        soup = bs(response.text, 'lxml')
        subject_list = soup.find('ul', class_='subject-list').find_all('li')
        branch_urls = [self.make_url(subject.a['href']) for subject in subject_list]  # getting math branches url
        print(branch_urls[2:3])
        return branch_urls

    #this function gets the year list whereas there is data for more than 10 years
    def getting_years(self, branch_urls):
        year_list = []
        for branch_url in branch_urls[2:3]:
            response = self.session.get(branch_url)
            sleep(self.sleep_time)
            soup = bs(response.text, 'lxml')
            year_list_ = soup.find(
                'ul', class_='year-list').find_all(
                'li', class_='year mod-box', recursive=False)  # geting all the years url
            for year in year_list_:
                year_list.append((year, branch_url))
        return year_list

    # this function gets month urls for each year
    def getting_month_urls(self, year_list):
        month_urls = []
        for branch_year in year_list[:1]:
            year = branch_year[0]
            branch_url = branch_year[1]
            month_list = year.find('ul', class_='month-list').find_all('li')

            for month_url in month_list:  # getting each month_links of the year
                month_urls.append(self.make_url(month_url.a['href'], branch_url))
        return month_urls

    # this function gets the days urls for each month
    def getting_day_urls(self, month_urls):
        day_urls = []
        for month_url in month_urls[:1]:
            response = self.session.get(month_url)
            sleep(self.sleep_time)
            soup = bs(response.text, 'lxml')
            day_urls_ = soup.find(
                'table', class_='calendar').find_all('a')
            for day_url in day_urls_[:1]:
                day_urls.append(self.make_url(day_url['href'], month_url))  # getting each day urls of the
                print(self.make_url(day_url['href'], month_url))
        return day_urls

    # in this function we are collecting the main content urls and calling parse_content function
    # to do the parsing and creating dataframe
    def getting_content(self, day_urls):
        for day_url in day_urls:
            print(day_url)
            response = self.session.get(day_url)
            print(response)
            sleep(self.sleep_time)
            soup = bs(response.text, 'html.parser')
            try:
                questions = soup.find('ul', class_='questions-list').find_all('li')
                for question in questions:
                    try:
                        answer_status = self.verify_status(question.find('div', class_='more').text.strip())
                    except:
                        answer_status = ''
                    try:
                        content_url = self.make_url(question.a['href'])
#                         self.parse_math_content(content_url, answer_status)
                    except:
                        content_url = ''

            except:
                questions = ''
            next_pg = soup.find('div',class_='questions-pagination').find('a',attrs={'class':'questions-pagination-link'},text='Next')
            print(next_pg)
            next_page = soup.find('a',attrs={'class':'page-link next','aria-label':'Page Next'})
            if next_page is not None:
                index = day_urls.index(day_url)
                day_urls.insert(index+1,self.make_url(next_page))



    # this function parses required data  stroing it in dataframe
    def parse_math_content(self, content_url, answer_status):
        response = self.session.get(content_url)
        sleep(self.sleep_time)
        soup = bs(response.text, 'lxml')
        try:
            image_url = soup.find('div', class_='styled__QuestionBody-sc-1f9k7g9-2 cYjKgc').img['src']
        #             image_path = self.download_image(image_url)
        except:
            image_url = ''
            image_path = ''
        try:
            question_text = soup.find('h1', class_='styled__PageHeading-sc-1f9k7g9-0 NJrfD').text
        except:
            question_text = ''

        data = {
            'content_url': content_url,
            'image url': image_url,
            'question text': question_text,
            'answer status': answer_status,
            'content path': image_path
        }
        self.data_list.append(data)
        df = pd.DataFrame(self.data_list)
        self.df = df

    '''
    while collecting the urls to join relative links and while 
    getting the data for downloading image and then exporting data
    we are using the below functions'''
    
    #----- helping functions ------

    # exports dataframe into csv file
    def save(self):
        #         csv = self.to_csv('math_questions.csv',index=False)
        pass

    # this function verifies whether the question is answered or not
    def verify_status(self, answer_status):
        if '0' in answer_status:
            return 'unanswered'
        else:
            return 'answered'

    # this function helps us to download the images on images folder
    def download_image(self, url):
        if not os.path.exists('images'):
            os.mkdir('images')
        try:
            file_name = re.search(r'\w{8}-\w{4}-\w{4}-\w{4}-\w{12}', url).group()
            file_name_ = os.path.join('images', file_name[0] + '.JPEG')
            response = self.session.get(url)
            if not os.path.exists(file_name_):
                if response.status_code == 200:
                    with open(file_name_, 'wb') as f:
                        f.write(response.content, '\w{8}-\w{4}-\w{4}-\w{4}-\w{12}')
                        print(f'{file_name[0]} downloaded successfully')
                else:
                    print('image url is not working')
        except:
            file_name_ = ''
        return file_name_

    # this is helping function which joins the relatvie urls to domain .. and we call this function in url_parse
    def make_url(self, link, previous_url=''):
        if '/' in link:
            url = self.url.replace('/study/qa', '') + link
        else:
            url = '/'.join(previous_url.split('/')[:-1]) + '/' + link
        return url

    #---main--- function which starts the crawling ...
    # func to start the request and parse functions...
    def start_crawl(self):
        response = self.start_request()  # we get respone here
        self.url_parse(response)  # we get the subject urls here
        self.get_math_archive_link()  # this will give url in which page we can find the maths questions archive
        branch_urls = self.getting_branch_urls()
        year_list = self.getting_years(branch_urls)
        month_urls = self.getting_month_urls(year_list)
        day_urls = self.getting_day_urls(month_urls)
        content_urls = self.getting_content(day_urls)


if __name__ == '__main__':
    URL = 'https://www.chegg.com/study/qa'
    HEADERS = {
        #         ':authority': 'www.chegg.com',
        #          ':method': 'GET',
        #          ':path': '/study/qa',
        #          ':scheme': 'https',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9,ta;q=0.8,hi;q=0.7',
        'cache-control': 'no-cache',
        'cookie': '_schn=_txz2iv; CVID=2e5c78e6-08f3-4987-87b0-118c5cf49c26; V=c794aa821b8e192fea04a0f2e78064b16402db1d6b6ab8.11525317; CSessionID=84e7ab9d-fc0a-47ce-9417-0d8e8805f656; userData=%7B%22authStatus%22%3A%22Logged%20Out%22%2C%22attributes%22%3A%7B%22uvn%22%3A%22c794aa821b8e192fea04a0f2e78064b16402db1d6b6ab8.11525317%22%7D%7D; CSID=1677908765541; pxcts=dbd38866-ba4f-11ed-b21e-4c656b506a6c; _pxvid=dbd37c27-ba4f-11ed-b21e-4c656b506a6c; schoolapi=null; usprivacy=1---; _pxff_tm=1; OptanonConsent=isGpcEnabled=0&datestamp=Sat+Mar+04+2023+11%3A16%3A59+GMT%2B0530+(India+Standard+Time)&version=6.39.0&isIABGlobal=false&hosts=&consentId=b51b2919-baae-4ff3-a570-4eaabcb33de0&interactionCount=1&landingPath=NotLandingPage&groups=fnc%3A0%2Csnc%3A1%2Ctrg%3A0%2Cprf%3A0&AwaitingReconsent=false; _scid=a0c9d5d9-5fc2-4b1a-b746-752a8e633ed0; ln_or=eyI4ODQyMzUiOiJkIn0%3D; _sctr=1|1677868200000; _px3=7c8e5e690a23b26f5a997ff8d0722a246b717aff5d41569be5fd6bc65b978c7',
        'dnt': '1',
        'pragma': 'no-cache',
        'referer': 'http',
        'sec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", "Google Chrome";v="110"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
    }

    chegg = Chegg(URL, HEADERS)
    chegg.start_crawl()
