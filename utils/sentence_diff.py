import nltk
import difflib
nltk.download("punkt")
from nltk.tokenize import sent_tokenize

def normalize(s):
    return s.lower().strip()

def highlight_changes(original, rewritten):
    orig = [normalize(s) for s in sent_tokenize(original)]
    new = sent_tokenize(rewritten)

    matcher = difflib.SequenceMatcher(None, orig, [normalize(s) for s in new])

    results = []

    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        for sent in new[j1:j2]:
            results.append({
                "text": sent,
                "changed": tag != "equal"
            })

    return results
