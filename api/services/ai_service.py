from transformers import pipeline

class AIService:
    def __init__(self):
        self.summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

    async def summarize(self, text: str, max_length: int) -> str:
        summary = self.summarizer(text, max_length=max_length, min_length=30, do_sample=False)
        return summary[0]['summary_text']