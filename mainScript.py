from SentimentAnalysis import Analyser
import praw
from subredditScraper import SrScrapper
if __name__ == "__main__":

    reddit = praw.Reddit("elonbot", user_agent="ElonBot v1.0 developed by u/zeroDev_")

    scrapper = SrScrapper()
    matchingComment = scrapper.findInSubreddit(reddit, "xqcow", "lil bro")

    
    map(function)
    for comment in matchingComment:
        text = comment.body 

        result = Analyser.classifyOne(text)
        if(result == 'POSITIVE'):


