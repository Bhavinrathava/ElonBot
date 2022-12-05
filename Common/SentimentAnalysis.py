from transformers import pipeline

# Prefect imports
from prefect import task, flow

class Analyser:
    def __init__(self, pipelineName:str = "sentiment-analysis"):
        self.pipeline = pipeline(pipelineName)

    @task
    def classify(self,data):
        # data = {id-> [text]}
        textList = [i[0] for i in data.values()]
        results = self.pipeline(textList)

        keys = list(data.keys())
        for i in range(len(keys)):
            data[keys[i]].append(results[i]['label'])
            
        return data 
    @task
    def classifyOne(self,data:str)->list:

        results = self.pipeline([data])
        answers = results[0]['label']
        return answers
    

if __name__ == "__main__":
    data = {1:["text1"], 2:['text2'], 3:['text3']}
    analyser = Analyser()
    print(analyser.classify(data))