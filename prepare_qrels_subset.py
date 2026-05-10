from __future__ import annotations

import argparse
import os
import random
import ir_datasets
from tqdm import tqdm

from config import COLLECTION_PATH, QUERIES_PATH, QRELS_PATH, DATA_DIR
from utils import ensure_dirs


def clean_text(text: str) -> str:
    return text.replace("\t", " ").replace("\n", " ").strip()


def main(num_queries: int, distractors: int):
    ensure_dirs(DATA_DIR)

    dev = ir_datasets.load("msmarco-passage/dev/small")
    train = ir_datasets.load("msmarco-passage/train")

    queries = []
    for q in dev.queries_iter():
        queries.append((q.query_id, clean_text(q.text)))
        if len(queries) >= num_queries:
            break

    selected_qids = {qid for qid, _ in queries}

    relevant_doc_ids = set()
    qrels_rows = []

    for qr in dev.qrels_iter():
        if qr.query_id in selected_qids and int(qr.relevance) > 0:
            relevant_doc_ids.add(qr.doc_id)
            qrels_rows.append((qr.query_id, qr.doc_id, qr.relevance))

    needed_doc_ids = set(relevant_doc_ids)
    extra_count = 0

    with open(COLLECTION_PATH, "w", encoding="utf-8") as fc:
        for doc in tqdm(train.docs_iter(), desc="Building qrels-aware collection"):
            include = False

            if doc.doc_id in needed_doc_ids:
                include = True
            elif extra_count < distractors:
                include = True
                extra_count += 1

            if include:
                fc.write(f"{doc.doc_id}\t{clean_text(doc.text)}\n")

            #if needed_doc_ids.issubset(set()) and extra_count >= distractors:
             #   pass

    with open(QUERIES_PATH, "w", encoding="utf-8") as fq:
        for qid, text in queries:
            fq.write(f"{qid}\t{text}\n")

    with open(QRELS_PATH, "w", encoding="utf-8") as fr:
        for qid, doc_id, rel in qrels_rows:
            fr.write(f"{qid}\t{doc_id}\t{rel}\n")

    with open(f"{DATA_DIR}/custom_queries.txt", "w", encoding="utf-8") as f:
        f.write(
            "who wrote pride and prejudice\n"
            "what is the capital of france\n"
            "when did world war ii end\n"
            "who painted the mona lisa\n"
            "what is photosynthesis\n"
        )

    print(f"Saved {num_queries} queries to {QUERIES_PATH}")
    print(f"Saved {len(qrels_rows)} qrels to {QRELS_PATH}")
    print(f"Saved qrels-aware collection to {COLLECTION_PATH}")
    print(f"Relevant docs included: {len(relevant_doc_ids)}")
    print(f"Distractors included: {extra_count}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--num_queries", type=int, default=10)
    parser.add_argument("--distractors", type=int, default=50000)
    args = parser.parse_args()

    main(args.num_queries, args.distractors)