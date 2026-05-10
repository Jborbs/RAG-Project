# BM25 + RAG Web App

This project runs a BM25-based Retrieval-Augmented Generation demo over MS MARCO passages.

## 1. Start Elasticsearch with Docker

Use the one-line command below:

```bash
docker run --name es-bm25 -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" -e "xpack.security.enabled=false" -e "ES_JAVA_OPTS=-Xms1g -Xmx1g" docker.elastic.co/elasticsearch/elasticsearch:8.19.0
```

If the container already exists, use:

```bash
docker start es-bm25
```

Check that Elasticsearch is running:

```bash
curl http://localhost:9200
```

## 2. Create and activate Python environment

```bash
python -m venv .venv
```

Windows Git Bash:

```bash
source .venv/Scripts/activate
```

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## 3. Prepare MS MARCO data with a limit

Use UTF-8 mode on Windows:

```bash
python -X utf8 prepare_data.py --limit 50000
```

For a larger run:

```bash
python -X utf8 prepare_data.py --limit 100000
```

## 4. Create the BM25 index

```bash
python create_index_bm25.py
```

## 5. Bulk index passages

```bash
python bulk_index_bm25.py
```

If Docker crashes during indexing, lower the `chunk_size` in `bulk_index_bm25.py`.

## 6. Run the web app

```bash
streamlit run streamlit_app.py
```

Then open the local URL Streamlit prints, usually:

```text
http://localhost:8501
```

## 7. Use the app

The app lets you:

- type a question
- run BM25 retrieval
- generate a RAG answer
- view retrieved passages and BM25 scores
