from elasticsearch import Elasticsearch
from config import ELASTIC_HOST, ELASTIC_USERNAME, ELASTIC_PASSWORD, INDEX_NAME

es = Elasticsearch(
    ELASTIC_HOST,
    basic_auth=(ELASTIC_USERNAME, ELASTIC_PASSWORD)
)

def bm25_search(query: str, top_k: int = 5):
    body = {
        "size": top_k,
        "query": {
            "match": {
                "text": query
            }
        }
    }

    resp = es.search(index=INDEX_NAME, body=body)
    return [
        {
            "passage_id": hit["_source"]["passage_id"],
            "text": hit["_source"]["text"],
            "score": hit["_score"]
        }
        for hit in resp["hits"]["hits"]
    ]
