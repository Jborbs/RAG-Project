from __future__ import annotations

import os
os.environ["PYTHONUTF8"] = "1"

import argparse
import ir_datasets
from tqdm import tqdm

from config import COLLECTION_PATH, QUERIES_PATH, QRELS_PATH, DATA_DIR
from utils import ensure_dirs


def export_collection(limit: int | None = None) -> None:
    dataset = ir_datasets.load("msmarco-passage/train")
    count = 0
    with open(COLLECTION_PATH, "w", encoding="utf-8") as f:
        for doc in tqdm(dataset.docs_iter(), desc="Exporting collection"):
            f.write(f"{doc.doc_id}\t{doc.text}\n")
            count += 1
            if limit is not None and count >= limit:
                break
    print(f"Saved {count} passages to {COLLECTION_PATH}")


def export_dev_queries_and_qrels() -> None:
    dataset = ir_datasets.load("msmarco-passage/dev/small")

    q_count = 0
    with open(QUERIES_PATH, "w", encoding="utf-8") as fq:
        for q in dataset.queries_iter():
            fq.write(f"{q.query_id}\t{q.text}\n")
            q_count += 1

    r_count = 0
    with open(QRELS_PATH, "w", encoding="utf-8") as fr:
        for qr in dataset.qrels_iter():
            fr.write(f"{qr.query_id}\t{qr.doc_id}\t{qr.relevance}\n")
            r_count += 1

    print(f"Saved {q_count} dev queries to {QUERIES_PATH}")
    print(f"Saved {r_count} qrels to {QRELS_PATH}")


def create_custom_query_template() -> None:
    path = f"{DATA_DIR}/custom_queries.txt"
    with open(path, "w", encoding="utf-8") as f:
        f.write(
            "what year did the first iphone come out\n"
            "who painted the mona lisa\n"
            "what is the capital of australia\n"
            "when did world war ii end\n"
            "who developed relativity\n"
        )
    print(f"Saved custom query template to {path}")
    print("After retrieving top 10 for these, create data/custom_qrels.tsv manually if you want P@10 for custom queries.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=None, help="Number of passages to export from MS MARCO train")
    args = parser.parse_args()

    ensure_dirs(DATA_DIR)
    export_collection(limit=args.limit)
    export_dev_queries_and_qrels()
    create_custom_query_template()
