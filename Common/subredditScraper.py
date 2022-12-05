
from praw.models import MoreComments
import logging
import bson

# Prefect imports
from prefect import task, flow

class SrScrapper:
    def __init__(self) -> None:
        pass

    @task
    def searchPhrase(self, comment:str, searchPhrase:str):
        if(searchPhrase in comment):
            return True
        return False
    
    @task
    def findInSubreddit(self, redditInstance, subName:str,  searchPhrase: str):
        matchingComments = []
        subreddit = redditInstance.subreddit(subName)
        submissions = subreddit.hot()
        for submission in submissions:
            for comment in submission.comments:
                if isinstance(comment, MoreComments):
                    continue
                if(comment.saved == False ):
                    comment.saved = True
                    if (self.searchPhrase(comment.body, searchPhrase)):
                        matchingComments.append(comment)

        return matchingComments
    
    @task
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

    @task
    def sentimentBasedReplies(self, comments, redditInstance):
        POSITIVE_MESSAGE = "I Sense some respect in your comment! But, you're FIRED anyway. Adios!"
        NEGATIVE_MESSAGE = "I Do not like the look of this comment. You are FIRED! "
        returnComments = []
        for comment in comments:
            replyText = ""
            comment = bson.decode(comment.raw)
            if(comment['sentiment'] == 'POSITIVE'):
                replyText = POSITIVE_MESSAGE
            else:
                replyText = NEGATIVE_MESSAGE
            
            replyID = redditInstance.comment(comment["id"]).reply(replyText)

            comment['saved'] = True
            comment['replyID'] = replyID

            returnComments.append(comment)
        
        return returnComments


            
