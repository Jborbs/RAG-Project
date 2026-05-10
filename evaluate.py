from __future__ import annotations

import argparse
from statistics import mean

from config import CUSTOM_QRELS_PATH, CUSTOM_QUERIES_PATH, OUTPUT_DIR, QRELS_PATH, QUERIES_PATH
from utils import ensure_dirs, write_json
from search_bm25 import bm25_search


def load_queries(path: str, limit: int | None = None):
    queries = []
    with open(path, "r", encoding="utf-8") as f:
        for idx, line in enumerate(f):
            if "\t" in line:
                qid, text = line.rstrip("\n").split("\t", 1)
            else:
                qid, text = f"custom_{idx+1}", line.strip()
            queries.append((qid, text))
            if limit is not None and len(queries) >= limit:
                break
    return queries


def load_qrels(path: str):
    qrels = {}
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            qid, pid, rel = line.rstrip("\n").split("\t")
            if int(rel) > 0:
                qrels.setdefault(qid, set()).add(pid)
    return qrels


def precision_at_k(retrieved: list[str], relevant: set[str], k: int = 10) -> float:
    retrieved_k = retrieved[:k]
    hits = sum(1 for pid in retrieved_k if pid in relevant)
    return hits / k


def evaluate_query_set(queries_path: str, qrels_path: str, limit: int | None = None, label: str = "run"):
    queries = load_queries(queries_path, limit=limit)
    qrels = load_qrels(qrels_path)
    results = {}
    scores = []

    for qid, query_text in queries:
        ranked = bm25_search(query_text, top_k=10)
        retrieved_pids = [r["passage_id"] for r in ranked]
        rel = qrels.get(qid, set())
        p10 = precision_at_k(retrieved_pids, rel, k=10)
        results[qid] = {
            "query": query_text,
            "retrieved": retrieved_pids,
            "relevant_count": len(rel),
            "p@10": p10,
        }
        scores.append(p10)

    avg = mean(scores) if scores else 0.0
    out = {
        "label": label,
        "avg_p@10": avg,
        "details": results,
    }
    return out


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--msmarco_limit", type=int, default=5)
    parser.add_argument("--run_custom", action="store_true")
    args = parser.parse_args()

    ensure_dirs(OUTPUT_DIR)
    msmarco_out = evaluate_query_set(QUERIES_PATH, QRELS_PATH, limit=args.msmarco_limit, label="msmarco")
    write_json(msmarco_out, f"{OUTPUT_DIR}/metrics_msmarco.json")
    print(f"MS MARCO avg P@10: {msmarco_out['avg_p@10']:.4f}")

    if args.run_custom:
        custom_out = evaluate_query_set(CUSTOM_QUERIES_PATH, CUSTOM_QRELS_PATH, limit=None, label="custom")
        write_json(custom_out, f"{OUTPUT_DIR}/metrics_custom.json")
        print(f"Custom avg P@10: {custom_out['avg_p@10']:.4f}")
