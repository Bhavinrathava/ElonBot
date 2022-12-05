
from prefect import flow
from SaveCommentsTODB import SaveCommentstoDB
from ParseSavedComments import parseCommentsFromDB
from replyToSavedComments import ReplyToComments

@flow
def ElonBotFlow():
    SaveCommentstoDB()
    parseCommentsFromDB()
    ReplyToComments()


if __name__ == "__main__":
    ElonBotFlow()