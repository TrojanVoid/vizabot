# vizabot
!!! This bot is not complete, only the scraping part of the bot currently operates, the uploader will be added within one week after repository creation. !!!
A bot made with Python libraries that automatically scrapes content from Reddit's subreddits and periodically uploads to configured Instagram pages.

Vizabot consists of two bots, one for scraping subreddits and the other for uploading to the designated Instagram pages. From now on, these bots will be referred as scraper and uploader respectively.

SCRAPER:
Scraper indirectly uses Reddit's API for scraping since it uses the PRAW (Python Reddit API Wrapper) wrapper library to request data. 
The data can be gathered  from a singular or multiple subreddits, specified in either the configurations file or in the terminal start command with the terminal option having higher priority. The default subreddit is 'all', which contains all the posts in all subbreddits available.

The requested content number can be limited but at this point, only the 'top' parameter tag of the subreddits can be used. The limitation number is again specified in either the configurations or in the terminal start command with the terminal option having higher priority. The default limitation is set to 10.

After the URLs and content information such as author, title and upvote count are successfuly gathered, scraper screenshots the content's viewport from the URL, and saves to the pre-designated folder. To center the viewport, rectangular cropping values can be specified. The target folder and the crop-box can be designated in the same way before. 
The screenshotting and image cropping is done with the Selenium and Pillow libraries respectively.
