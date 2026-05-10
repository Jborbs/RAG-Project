from elasticsearch import Elasticsearch, helpers
from config import ELASTIC_HOST, ELASTIC_USERNAME, ELASTIC_PASSWORD, INDEX_NAME, COLLECTION_PATH

es = Elasticsearch(
    ELASTIC_HOST,
    basic_auth=(ELASTIC_USERNAME, ELASTIC_PASSWORD)
)

def actions():
    with open(COLLECTION_PATH, "r", encoding="utf-8") as f:
        for line in f:
            pid, text = line.rstrip("\n").split("\t", 1)
            yield {
                "_index": INDEX_NAME,
                "_source": {
                    "passage_id": pid,
                    "text": text
                }
            }

helpers.bulk(es, actions(), chunk_size=200, request_timeout=120)
print("BM25 indexing complete.")
