from browsermobproxy import Server
from selenium import webdriver
from query_parser import parse_results
from datetime import date
from urllib.parse import urlparse
import csv


class ApiCrawler(object):
    def __init__(self, target, supported_methods=('GET', 'POST')):

        self.target = list(target)
        self.supported_methods = supported_methods
        self.browser_mob = 'C:/browsermob-proxy-2.1.4/bin/browsermob-proxy' #Path to browsermob
        self.server = None
        self.current_har = None

    def __start_server(self):
        self.server = Server(self.browser_mob)
        self.server.start()
        self.proxy = self.server.create_proxy()

    def __start_driver(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--proxy-server={}".format(self.proxy.proxy))
        self.driver = webdriver.Chrome(chrome_options=chrome_options)

    def __start_all(self):
        self.__start_server()
        self.__start_driver()

    def __create_har_no_interaction(self, title, url):
        self.proxy.new_har(title)
        self.driver.get(url)
        self.current_har = self.proxy.har
        return self.proxy.har

    def __parse_har(self):
        response = []
        temp = self.current_har['log']['entries']
        for i in temp:
            if i['request']['method'] in self.supported_methods:
                if any(target in i['request']['url'] for target in self.target):
                    url = i['request']['url']
                    method = i['request']['method']
                    params = parse_results(url)
                    status = i['response']['status']
                    redirect_url = i['response']['redirectURL']
                    if params:
                        result_row = [url, method, status, redirect_url] + params
                        response.append(result_row)
        return response

    def __write_to_csv(self, url, results):

        parsed = urlparse(url)

        with open('{}-{}.csv'.format(parsed.netloc, date.today()), 'a') as file:
            writer = csv.writer(file, dialect='excel')

            for item in results:
                item = [parsed.netloc] + item
                writer.writerow(item)

    def __stop_all(self):
        self.server.stop()
        self.driver.quit()

    def single_page(self, url):
        self.__start_all()
        self.__create_har_no_interaction('N/A', url)
        results = self.__parse_har()
        self.__write_to_csv(url, results)
        self.__stop_all()

    def list_of_pages(self, url_list):
        self.__start_all()
        for url in url_list:
            try:
                self.__create_har_no_interaction('N/A', url)
                results = self.__parse_har()
                self.__write_to_csv(url, results)
            except:
                continue
        self.__stop_all()

if __name__ == '__main__':
    a = ApiCrawler(['api','v1'])
    a.single_page('http://edmundmartin.com')
