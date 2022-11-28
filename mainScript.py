from SentimentAnalysis import Analyser
import praw
from subredditScraper import SrScrapper
import logging
if __name__ == "__main__":

    reddit = praw.Reddit("elonbot", user_agent="ElonBot v1.0 developed by u/zeroDev_")

    scrapper = SrScrapper()
    analyser = Analyser()

    matchingComment = scrapper.findInSubreddit(reddit, "test", "Elon")

    # {commentID : ["text", Positive / Negative, replyID]}
    ds = {}
    for i in matchingComment:
        ds[i.id] = [i.body]
    logging.info("Found {} comments mentioning Elon-san ! ", len(ds))

    processedComments = analyser.classify(ds)

    scrapper.replyToComments(reddit,processedComments)

