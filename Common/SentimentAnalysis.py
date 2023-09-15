from transformers import pipeline

# Prefect imports
from prefect import task, flow


def classify(data):
    pl = pipeline("sentiment-analysis")

    for comment in data :
        comment['sentiment'] = pl(comment['body'])[0]['label']
        comment['replied'] = False

    return data

@task
def classifyOne(data:str)->list:

    results = pipeline("sentiment-analysis")([data])
    answers = results[0]['label']
    return answers


if __name__ == "__main__":
    data = {1:["text1"], 2:['text2'], 3:['text3']}
    print(classify(data))