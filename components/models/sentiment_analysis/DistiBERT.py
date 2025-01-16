from transformers import pipeline

class DistiBERT :

    def __init__(self):
        self.pipeline = pipeline(
            "text-classification", 
            model="lxyuan/distilbert-base-multilingual-cased-sentiments-student"
        )

    def analyze(self,text):
        return self.pipeline(text)

    def result(self, texts , results):
        for text, result in zip(texts, results):
            print(f"Texte: {text}")
            print(f"Sentiment: {result['label']}, Score: {result['score']:.2f}\n")
