from langchain_core.tools import tool
import nltk
nltk.download("punkt")
from nltk.tokenize import sent_tokenize, word_tokenize

@tool
def burstiness_score(text: str) -> float:
    """
    Returns burstiness (variance of sentence lengths) in the given text.
    """
    sentences = sent_tokenize(text)
    lengths = [len(word_tokenize(s)) for s in sentences]
    if len(lengths) < 2:
        return 0
    mean = sum(lengths) / len(lengths)
    variance = sum((l - mean) ** 2 for l in lengths) / (len(lengths) - 1)
    return round(variance, 2)
