import requests
from scraper import Scraper


def __main__():
    if __name__ == '__main__':
        scraper = Scraper(subreddit='travelphotos',limit=50, folder='travel')
        scraper.scrape()
        
__main__()