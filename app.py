from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# -----------------------------
# Dummy Knowledge Base Loader
# -----------------------------
def load_knowledge_base():
    chunks = []
    current_topic = None
    current_text = []

    with open("data/knowledge_base.txt", "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()

            if line.startswith("[TOPIC:"):
                if current_topic and current_text:
                    chunks.append({
                        "topic": current_topic,
                        "text": " ".join(current_text)
                    })
                current_topic = line.replace("[TOPIC:", "").replace("]", "").strip().upper()
                current_text = []
            elif line:
                current_text.append(line)

        if current_topic and current_text:
            chunks.append({
                "topic": current_topic,
                "text": " ".join(current_text)
            })

    return chunks

knowledge_chunks = load_knowledge_base()

# -----------------------------
# Dummy Retriever (Keyword Based)
# -----------------------------
import re

STOPWORDS = {
    "what", "is", "are", "the", "a", "an", "in", "on", "for",
    "to", "of", "and", "with", "how", "does"
}

import re

STOPWORDS = {
    "what", "is", "are", "the", "a", "an", "in", "on", "for",
    "to", "of", "and", "how", "does"
}

import re

STOPWORDS = {
    "what", "is", "are", "the", "a", "an", "in", "on",
    "for", "to", "of", "and", "how", "does"
}

import re

STOPWORDS = {
    "what", "is", "are", "the", "a", "an", "in", "on",
    "for", "to", "of", "and", "how", "does"
}

def retrieve_context(query):
    intent = detect_intent(query)

    # KEY FIX: If intent is detected, return that topic directly
    if intent:
        for chunk in knowledge_chunks:
            if chunk["topic"] == intent:
                return [chunk["text"]]
        return []

    # Fallback: keyword-based retrieval (only if no intent)
    query_words = {
        w for w in re.findall(r"\w+", query.lower())
        if w not in STOPWORDS 
    }

    scored = []

    for chunk in knowledge_chunks:
        text = chunk["text"].lower()
        score = sum(1 for w in query_words if w in text)
        if score > 0:
            scored.append((score, chunk["text"]))

    scored.sort(reverse=True, key=lambda x: x[0])
    return [scored[0][1]] if scored else []


# -----------------------------
# Dummy LLM Response Generator
# -----------------------------
def generate_response(query, context):
    if not context:
        return (
            "I could not find relevant information for your query. "
            "Please try rephrasing."
        )

    return f"Here is the information related to **{query}**:\n\n{context[0]}"



def detect_intent(query):
    q = query.lower()

    if any(w in q for w in ["security", "secure", "guardrail", "safety"]):
        return "GUARDRAILS"

    if any(w in q for w in ["vector", "embedding", "faiss", "chromadb"]):
        return "VECTOR DATABASES"

    if "rag" in q:
        return "RAG"

    return None

def load_kb():
    kb = {}
    with open("data/knowledge_base.txt", "r", encoding="utf-8") as f:
        for line in f:
            if ":" in line:
                key, value = line.split(":", 1)
                kb[key.strip().lower()] = value.strip()
    return kb

KB = load_kb()

# -----------------------------
# Routes
# -----------------------------
@app.route("/")
def index():
    return render_template("chat.html")

@app.route("/chat", methods=["POST"])
def chat():
    query = request.json.get("message", "").lower()

    if "leave" in query:
        answer = KB.get("leave")
    elif "onboarding" in query or "joining" in query:
        answer = KB.get("onboarding")
    elif "security" in query or "data" in query:
        answer = KB.get("security")
    elif "rag" in query:
        answer = KB.get("rag")
    else:
        answer = "Sorry, I could not find relevant HR information for your query."

    return jsonify({"response": answer})


if __name__ == "__main__":
    app.run(debug=True)
