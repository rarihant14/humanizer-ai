from langgraph.graph import StateGraph
from typing import TypedDict, List
import nltk
nltk.download("punkt")
from nltk.tokenize import sent_tokenize

from agents.groq_refacer import human_style_rewriter
from agents.flow_enhancer import enhance_flow
from agents.meaning_checker import preserve_meaning
from agents.burstiness_checker import burstiness_score
from tools.realism_score import calculate_realism


class State(TypedDict):
    original: str
    rewritten: str
    burstiness: float
    realism: dict
    meaning: dict | str
    trace: List[str]


# 🔹 NODE 1: SENTENCE-BY-SENTENCE REWRITE
def rewrite_node(state: State):
    sentences = sent_tokenize(state["original"])
    rewritten_sentences = []

    for s in sentences:
        r = human_style_rewriter.invoke({
            "text": s,
            "persona": "default"
        })
        rewritten_sentences.append(str(r))

    rewritten_text = " ".join(rewritten_sentences)

    return {
        "rewritten": rewritten_text,
        "trace": state["trace"] + [
            f"🧠 Rewrite Agent: Rewrote {len(sentences)} sentences individually."
        ]
    }


# 🔹 NODE 2: FLOW ENHANCER (SECOND PASS)
def flow_node(state: State):
    refined = enhance_flow.invoke(state["rewritten"])

    return {
        "rewritten": str(refined),
        "trace": state["trace"] + [
            "✨ Flow Enhancer: Improved transitions and sentence rhythm."
        ]
    }


# 🔹 NODE 3: SCORING + MEANING
def score_node(state: State):
    burst = burstiness_score(state["rewritten"])
    realism = calculate_realism(state["rewritten"])
    meaning = preserve_meaning(
        state["original"],
        state["rewritten"]
    )

    trace = state["trace"] + [
        f"📊 Scoring Agent: Burstiness={burst}, Human-likeness={realism['human_likeness']}",
    ]

    if isinstance(meaning, dict) and meaning.get("disagreement"):
        trace.append("⚠️ Meaning Agents Disagree")
    else:
        trace.append("✅ Meaning preserved")

    return {
        "burstiness": burst,
        "realism": realism,
        "meaning": meaning,
        "trace": trace
    }


# 🧬 BUILD GRAPH
graph = StateGraph(State)

graph.add_node("rewrite", rewrite_node)
graph.add_node("flow", flow_node)
graph.add_node("score", score_node)

graph.set_entry_point("rewrite")
graph.add_edge("rewrite", "flow")
graph.add_edge("flow", "score")

humanizer_graph = graph.compile()
