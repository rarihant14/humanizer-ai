# 🧠 Humanizer AI
### Explainable, Memory-Driven AI Text Humanization

Humanizer AI is an **agentic AI system** that rewrites AI-generated text to sound more **human, natural, and conversational**.

Unlike simple paraphrasers, this project uses **sentence-by-sentence rewriting**, **multi-agent reasoning**, **style memory**, and **explainable traces** to show *how* and *why* text changes.

---

## ✨ Key Features

### 🧬 LangGraph Multi-Agent Flow
- Sentence Rewrite Agent  
- Flow Enhancer Agent  
- Meaning Validation Agent (Gemini)  
- Scoring Agent (burstiness & realism)

### 🧠 Memory-Based Style Learning
- Learns writing patterns over time  
- Adapts sentence length and tone  
- Persists style across runs  

### 🔍 Explainability
- Agent reasoning trace visible in UI  
- Meaning-preservation checks  
- Agent disagreement detection  

### ✏️ What Changed Highlighting
- Sentence-level difference detection  
- Highlights modified vs unchanged lines  

### 🎨 Clean Dark UI
- Copyable output box  
- Funny but sensible loading messages  
- Developer-friendly interface  

---

## 🧩 Architecture Overview
          User Input
              
              ↓
        
        Sentence Rewrite Agent
      
              ↓
    
    
        Flow Enhancer Agent
↓
Meaning Checker (Gemini)
↓
Scoring Agent
↓
Post-processing (Diff + Highlight)
↓
UI (Output + Trace + Highlights)






