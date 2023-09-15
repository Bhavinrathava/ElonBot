
from praw.models import MoreComments
import logging
import bson
import praw
# Prefect imports
from prefect import task, flow


def searchPhrasefunc( comment:str, searchPhrase:str):
    if(searchPhrase in comment):
        return True
    return False


def findInSubreddit(redditInstance, subName:str,  searchPhrase: str):
    matchingComments = []
    subreddit = redditInstance.subreddit(subName)
    submissions = subreddit.hot()
    for submission in submissions:
        for comment in submission.comments:
            if isinstance(comment, MoreComments):
                continue
            if(comment.saved == False ):
                comment.saved = True
                if (searchPhrasefunc(comment.body, searchPhrase)):
                    matchingComments.append(comment)

    return matchingComments

@task
def replyToComments(redditInstance, processedComments):
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


def sentimentBasedReplies(comments, redditInstance):
    POSITIVE_MESSAGE = "I Sense some respect in your comment! But, you're FIRED anyway. Adios!"
    NEGATIVE_MESSAGE = "I Do not like the look of this comment. You are FIRED! "
    returnComments = []
    logging.info("Number of Comments queued for replies : {}", len(comments))
    for comment in comments:
        logging.info("current Comment : {}" ,comment["commentID"])
        commentID = comment["commentID"]
        replyText = POSITIVE_MESSAGE if (comment['sentiment'] == 'POSITIVE') else NEGATIVE_MESSAGE
        try:
            replyID = redditInstance.comment(commentID).reply(replyText) 
            logging.info("Submitted a Reply! CommentID : {} :: ReplyID : {} ", commentID, replyID)
            comment['replied'] = True
            comment['replyID'] = replyID
            returnComments.append(comment)   
        
        except Exception:
            logging.exception("Encountered an Error while Replying to Comments")
        
        finally:
            pass
        

    
    return returnComments


        
