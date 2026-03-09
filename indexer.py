import os
import re
import json
import math
from bs4 import BeautifulSoup
from collections import defaultdict, Counter

# TASK 1 – Load HTML Documents

def load_documents(folder="pages"):
    documents = {}
    doc_id = 0

    for filename in os.listdir(folder):
        if filename.endswith(".html"):
            path = os.path.join(folder, filename)
            with open(path, "r", encoding="utf-8") as f:
                documents[doc_id] = f.read()
                doc_id += 1

    
    return documents

# TASK 2 – Extract Visible Text

def extract_text(html):
    soup = BeautifulSoup(html, "html.parser")

    
    for tag in soup(["script", "style"]):
        tag.decompose()

    text = soup.get_text(separator=" ")
    return text

# TASK 3 – Tokenization
def tokenize(text):
    text = text.lower()
    text = re.sub(r"[^\w\s]", "", text) 
    words = text.split()
    return words

# TASK 4 – Compute Term Frequency

def compute_tf(documents):
    tf = {}

    for doc_id, html in documents.items():
        text = extract_text(html)
        words = tokenize(text)
        tf[doc_id] = Counter(words)

    return tf

# TASK 5 – Build Inverted Index

def build_inverted_index(tf):
    inverted_index = defaultdict(list)

    for doc_id, word_counts in tf.items():
        for word, freq in word_counts.items():
            inverted_index[word].append((doc_id, freq))

    return dict(inverted_index)

# TASK 7 – Compute IDF

def compute_idf(inverted_index, total_docs):
    idf = {}

    for word, postings in inverted_index.items():
        df = len(postings)
        idf[word] = math.log(total_docs / df)

    return idf

# TASK 6 & 8 – Save to Disk

def save_json(data, filename):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

# TASK 9 – Validation

def validate(documents, inverted_index, idf):
    print("\n--- VALIDATION ---")
    print("Number of documents indexed:", len(documents))
    print("Number of unique terms:", len(inverted_index))

# MAIN PROGRAM
if __name__ == "__main__":

    # --- Task 1: Load documents ---
    documents = load_documents("pages")
    print("Total Documents:", len(documents))

    # --- Task 2: Extract visible text ---
    if documents:
        first_doc = documents[0]
        text = extract_text(first_doc)
        print("\n--- SAMPLE EXTRACTED TEXT ---\n")
        print(text[:500])  # first 500 chars

        # --- Task 3: Tokenization ---
        tokens = tokenize(text)
        print("\n--- SAMPLE TOKENS ---\n")
        print(tokens[:30])  # first 30 tokens

    # --- Task 4: Compute Term Frequency ---
    tf = compute_tf(documents)
    print("\n--- SAMPLE TERM FREQUENCY FOR DOC 0 ---")
    print(list(tf[0].items())[:10])

    # --- Task 5: Build Inverted Index ---
    inverted_index = build_inverted_index(tf)
    print("\n--- SAMPLE INVERTED INDEX ENTRIES ---")
    for word in list(inverted_index.keys())[:5]:
        print(word, "->", inverted_index[word])

    # --- Task 6: Save Inverted Index ---
    save_json(inverted_index, "inverted_index.json")
    print("\nInverted index saved to inverted_index.json")

    # --- Task 7: Compute IDF ---
    idf = compute_idf(inverted_index, len(documents))
    print("\n--- SAMPLE IDF VALUES ---")
    for word in list(idf.keys())[:5]:
        print(word, ":", round(idf[word], 4))

    # --- Task 8: Save IDF ---
    save_json(idf, "idf.json")
    print("\nIDF values saved to idf.json")

    # --- Task 9: Validation ---
    validate(documents, inverted_index, idf)