from bs4 import BeautifulSoup


class HtmlParser(object):
    def __init__(self, html_cont):
        self.html_cont = html_cont

    def get_soup(self):
        soup = BeautifulSoup(self.html_cont, 'lxml', from_encoding='utf-8')
        return soup
