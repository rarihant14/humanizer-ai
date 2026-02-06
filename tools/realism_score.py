import textstat

def calculate_realism(text: str) -> dict:
    return {
        "readability": textstat.flesch_reading_ease(text),
        "complexity": textstat.dale_chall_readability_score(text),
        "human_likeness": 100 - abs(textstat.flesch_reading_ease(text) - 60),
    }
