import os

ELASTIC_HOST = os.getenv("ELASTIC_HOST", "http://localhost:9200")
ELASTIC_USERNAME = os.getenv("ELASTIC_USERNAME", "elastic")
ELASTIC_PASSWORD = os.getenv("ELASTIC_PASSWORD", "changeme")

INDEX_NAME = "msmarco_bm25"

DATA_DIR = "data"
OUTPUT_DIR = "outputs"

COLLECTION_PATH = f"{DATA_DIR}/collection.tsv"
QUERIES_PATH = f"{DATA_DIR}/queries.dev.tsv"
QRELS_PATH = f"{DATA_DIR}/qrels.dev.tsv"
CUSTOM_QUERIES_PATH = f"{DATA_DIR}/custom_queries.txt"
CUSTOM_QRELS_PATH = f"{DATA_DIR}/custom_qrels.tsv"
EMBEDDINGS_PATH = f"{OUTPUT_DIR}/passage_embeddings.npy"
PID_MAPPING_PATH = f"{OUTPUT_DIR}/pid_mapping.json"

GEN_MODEL = "google/flan-t5-base"
TOP_K = 5
