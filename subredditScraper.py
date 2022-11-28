import praw
from praw.models import MoreComments
import logging

class SrScrapper:
    def __init__(self) -> None:
        pass

    def searchPhrase(self, comment:str, searchPhrase:str):
        if(searchPhrase in comment):
            return True
        return False
    

    def findInSubreddit(self, redditInstance, subName:str,  searchPhrase: str):
        matchingComments = []
        subreddit = redditInstance.subreddit(subName)
        submissions = subreddit.hot()
        for submission in submissions:
            for comment in submission.comments:
                if isinstance(comment, MoreComments):
                    continue
                if(self.searchPhrase(comment.body, searchPhrase)):
                    matchingComments.append(comment)

        return matchingComments
    
    def replyToComments(self, redditInstance, processedComments):
        POSITIVE_MESSAGE = "I Sense some respect in your comment! But, you're FIRED anyway. Adios!"
        NEGATIVE_MESSAGE = "I Do not like the look of this comment. You are FIRED! "
        commentIDs = list(processedComments.keys())
        #{CID:[text, sentiment]}
        
        for commentid in commentIDs:
            arr = processedComments[commentid]
            if(arr[-1] == 'POSITIVE'):
                repID = redditInstance.comment(commentid).reply(POSITIVE_MESSAGE)
                logging.info("Found a Positive Sent. comment : Comment ID -> {} and replyID -> {}", commentid,repID)
            else:
                repID = redditInstance.comment(commentid).reply(NEGATIVE_MESSAGE)
                logging.info("Found a Positive Sent. comment : Comment ID -> {} and replyID -> {}", commentid,repID)

            

            
