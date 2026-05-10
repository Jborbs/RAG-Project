import argparse
from transformers import pipeline
from search_bm25 import bm25_search
from config import GEN_MODEL

generator = pipeline("text2text-generation", model=GEN_MODEL)

def build_prompt(query, passages):
    context = "\n\n".join(
        [f"Passage {i+1}: {p['text']}" for i, p in enumerate(passages)]
    )
    return f"""Answer the question using only the provided context. If the answer is not supported by the context, say that the context is insufficient.

Question: {query}

Context:
{context}

Answer:"""

def answer_query(query, top_k=5, max_new_tokens=64):
    passages = bm25_search(query, top_k=top_k)
    prompt = build_prompt(query, passages)
    output = generator(prompt, max_new_tokens=max_new_tokens)[0]["generated_text"]

    if "Answer:" in output:
        answer = output.split("Answer:")[-1].strip()
    else:
        answer = output.strip()

    answer = answer.split("\n")[0].strip()

    return {
        "query": query,
        "answer": answer,
        "passages": passages
    }

def load_custom_queries(path):
    queries = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            q = line.strip()
            if q:
                queries.append(q)
    return queries

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--query", type=str)
    parser.add_argument("--query_file", type=str)
    args = parser.parse_args()

    if args.query_file:
        queries = load_custom_queries(args.query_file)
        for query in queries:
            result = answer_query(query)
            print("\n====================")
            print("Query:", result["query"])
            print("Answer:", result["answer"])
    elif args.query:
        result = answer_query(args.query)
        print("Query:", result["query"])
        print("Answer:", result["answer"])
    else:
        print("Provide --query or --query_file")
