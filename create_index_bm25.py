from elasticsearch import Elasticsearch
from config import ELASTIC_HOST, ELASTIC_USERNAME, ELASTIC_PASSWORD, INDEX_NAME

es = Elasticsearch(
    ELASTIC_HOST,
    basic_auth=(ELASTIC_USERNAME, ELASTIC_PASSWORD)
)

mapping = {
    "settings": {
        "number_of_shards": 1,
        "number_of_replicas": 0
    },
    "mappings": {
        "properties": {
            "passage_id": {"type": "keyword"},
            "text": {"type": "text"}
        }
    }
}

if es.indices.exists(index=INDEX_NAME):
    es.indices.delete(index=INDEX_NAME)

es.indices.create(index=INDEX_NAME, body=mapping)
print(f"Created index: {INDEX_NAME}")
