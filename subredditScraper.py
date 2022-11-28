import praw
from praw.models import MoreComments
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
            
