PROJECT 

- Elon Parody Bot for Reddit 

WHAT LIBS / FRAMEWORKS DOES IT USE 
- Prefect
- Praw
- Huggingface Transformers
- Pymongo 

WHAT IT DOES 
- Scrapes a selected subreddit for comments that mention Elon 
- Assembles a list of comments 
- Connects to a remote MongoDB cloud Cluster and saves the comments to the Collection 
- Access Cluster for unprocessed comments and determine their sentiment classification using Huggingface pipeline
- Save the sentiment analysis results to DB for next step  
- Reply to comments based on sentiment detected 
- Monitor the progress and logs via Prefect Flows 

![Alt text]('/ReadmeSS/DBSS-1.png')
![Alt text]('/ReadmeSS/DBSS-2.png')
![Alt text]('/ReadmeSS/PrefectShot.png') 