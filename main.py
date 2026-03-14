import json
import re
import string
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


# -----------------------------------------
# Task 1: Load inverted index and IDF
# -----------------------------------------

with open("inverted_index.json", "r") as f:
    inverted_index = json.load(f)

with open("idf.json", "r") as f:
    idf = json.load(f)

# -----------------------------------------
# Initialize FastAPI
# -----------------------------------------

app = FastAPI()

# -----------------------------------------
# Task 2: Query Tokenization
# -----------------------------------------

def tokenize_query(query):

    # convert to lowercase
    query = query.lower()

    # remove punctuation
    query = re.sub(r"[^\w\s]", "", query)

    # split into tokens
    tokens = query.split()

    return tokens


# -----------------------------------------
# Task 3 & 4: Search + TF-IDF Ranking
# -----------------------------------------

def search_documents(query):

    tokens = tokenize_query(query)

    scores = {}

    for word in tokens:

        if word in inverted_index:

            for doc in inverted_index[word]:
                doc_id = doc[0]
                tf = doc[1]
                score = tf * idf.get(word, 0)

                if doc_id not in scores:
                    scores[doc_id] = 0

                scores[doc_id] += score

    return scores


# -----------------------------------------
# Task 5: Sort Results
# -----------------------------------------

def rank_results(scores, top_n=10):

    sorted_results = sorted(scores.items(), key=lambda x: x[1], reverse=True)

    return sorted_results[:top_n]


# -----------------------------------------
# Task 6: FastAPI Search Endpoint
# -----------------------------------------
@app.get("/", response_class=HTMLResponse)
def home():
    with open("templates/ui.html", "r", encoding="utf-8") as file:
        return file.read()

@app.get("/search")

def search(query: str):

    scores = search_documents(query)

    ranked_results = rank_results(scores)

    formatted_results = []

    for doc_id, score in ranked_results:
        formatted_results.append({
            "doc_id": doc_id,
            "score": round(score, 4)
        })

    return {
        "query": query,
        "results": formatted_results
    }
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)