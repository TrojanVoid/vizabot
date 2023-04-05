import os
import praw
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

from image_cropper import ImageCropper

class Scraper():
    def __init__(self, subreddit:str='all', limit:int=10, folder:str='images'):
        self.num_skipped_content = 0 # TODO : RESET this value to 0 whenever a subreddit's scraping is done
        self.limit = limit
        self.setup_reddit_instance()
        self.subreddit = self.reddit.subreddit(subreddit)
        self.submissions = {}
        self.get_submissions()
        self.driver = webdriver.Firefox()
        self.driver.set_window_size(1920,1080)
        self.screenshots = []
        self.folder = folder
        self.image_cropper = ImageCropper()
        
    def scrape(self):
        self.screenshot_urls()
        self.move_screenshots_to_folders()
        self.crop_screenshots()
        
    def set_folder(self, folder:str):
        self.folder = folder
        
    def setup_reddit_instance(self):
        self.reddit = praw.Reddit(
        client_id = 'BwSrUSHNluLc58OTVGMP4A',
        client_secret = 'H-gK5uixqXY62w44af8Z5wybH2wzzw',
        user_agent = 'ContentScraper/0.1 by Trojaneo',
        )
        
    def get_submissions(self):
        for submission in self.subreddit.top(time_filter='week', limit=self.limit):
            is_original = False
            if not submission.is_self:
                if submission.is_original_content:
                    is_original = True
                self.submissions.update({submission : {
                    "is_original" : is_original,
                    "real_url" : "https://www.reddit.com" + submission.permalink
                }})
                
    def print_submissions(self)->None:
        if self.submissions != {}:
            for submission, props in zip(self.submissions, self.submissions.values()):
                print(  
                f"[ TITLE ] {submission.title} \n",
                f"[ SCORE ] {submission.score} \n",
                f"[ ID ] {submission.id} \n",
                f"[ URL ] {props['real_url']} \n\n"),
                f"[ CONTENT URL ] {submission.url}"
        else:
            print("No submissions have been requested yet.")
            
    def screenshot_urls(self):
        for submission, props in zip(self.submissions, self.submissions.values()):
            filename = submission.title + '.png' if not props["is_original"] else submission.title + '#' + submission.author.fullname + '.png'
            filename = self.sanitize_filename(filename)
            url = props["real_url"]
            print(f"[ URL ] {url}\n[ FILENAME ] {filename}")
            self.driver.get(url)
            try: element = self.driver.find_element(By.TAG_NAME, 'shreddit-post')
            except: 
                try: element = self.driver.find_element(By.CLASS_NAME, 'Post')
                except: 
                    print("Failed to find element")
                    continue
            time.sleep(3)
            print("Post screenshot is saved.")
            element.screenshot(filename)
            self.screenshots.append(filename)
        
        if self.num_skipped_content > 0:
            print(f"{self.num_skipped_content} posts have been skipped since they did not contain an image.")
            
    def crop_screenshots(self):
        for screenshot in self.screenshots:
            self.image_cropper.set_image(f'{self.folder}/{screenshot}')
            self.image_cropper.crop([55, 0, 0, 50])
            print("Post image has been cropped.")
            
    def move_screenshots_to_folders(self):
        if len(self.screenshots) > 0:
            for screenshot in self.screenshots:
                if not os.path.isfile(f'{self.folder}/{screenshot}'):
                    os.renames(screenshot, f'{self.folder}/{screenshot}')
                
    def sanitize_filename(self, filename:str):
        sanitized = ""
        for c in filename:
            if c == ' ': sanitized += sanitized.join("_")
            elif c == '.' or c.isalnum(): sanitized += sanitized.join(c)
        return sanitized
    
    
    