from langgraph_flow import humanizer_graph
from agents.style_memory import update_style_from_text
from utils.sentence_diff import highlight_changes

def run_humanizer_pipeline(text, persona):
    # 1️Run agent 
    result = humanizer_graph.invoke({
        "original": text,
        "rewritten": "",
        "burstiness": 0.0,
        "realism": {},
        "meaning": "",
        "trace": []
    })

    #Update style memory
    update_style_from_text(result["rewritten"])


    highlighted = highlight_changes(text, result["rewritten"])

    #combined response
    return {
        "output": result["rewritten"],
        "burstiness": result["burstiness"],
        "meaning": result["meaning"],
        "realism": result["realism"],
        "trace": result["trace"],
        "highlighted": highlighted  
    }
