from transformers import pipeline

class Analyser:
    def __init__(self, pipelineName:str = "sentiment-analysis"):
        self.pipeline = pipeline(pipelineName)

    def classify(self,data:list)->list:

        results = self.pipeline(data)
        answers = [i['label'] for i in results]
        return answers
    
    def classifyOne(self,data:str)->list:

        results = self.pipeline([data])
        answers = results[0]['label']
        return answers