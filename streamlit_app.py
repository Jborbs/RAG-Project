import streamlit as st
from elasticsearch import Elasticsearch

from config import ELASTIC_HOST, ELASTIC_USERNAME, ELASTIC_PASSWORD, INDEX_NAME
from search_bm25 import bm25_search
from rag_generate import answer_query


st.set_page_config(
    page_title="BM25 + RAG Search Demo",
    page_icon="🔎",
    layout="wide"
)


@st.cache_resource
def get_es_client():
    return Elasticsearch(
        ELASTIC_HOST,
        basic_auth=(ELASTIC_USERNAME, ELASTIC_PASSWORD)
    )


def check_elasticsearch():
    try:
        es = get_es_client()
        return es.ping()
    except Exception:
        return False


st.title("BM25 + RAG Search Demo")
st.write(
    "Search the MS MARCO passage index with Elasticsearch BM25, "
    "then generate an answer using the retrieved passages as context."
)

with st.sidebar:
    st.header("Settings")
    top_k = st.slider("Number of passages to retrieve", min_value=1, max_value=10, value=5)
    max_new_tokens = st.slider("Max answer tokens", min_value=32, max_value=256, value=64, step=16)
    show_passages = st.checkbox("Show retrieved passages", value=True)
    show_scores = st.checkbox("Show BM25 scores", value=True)

    st.divider()
    st.subheader("Elasticsearch")
    st.write(f"Host: `{ELASTIC_HOST}`")
    st.write(f"Index: `{INDEX_NAME}`")

    if check_elasticsearch():
        st.success("Elasticsearch is connected")
    else:
        st.error("Elasticsearch is not connected")


query = st.text_input(
    "Enter a question",
    value="who wrote pride and prejudice",
    placeholder="Type a question here..."
)

col1, col2 = st.columns([1, 1])

with col1:
    run_retrieval = st.button("Run BM25 Search", use_container_width=True)

with col2:
    run_rag = st.button("Run RAG Answer", use_container_width=True)


if run_retrieval or run_rag:
    if not query.strip():
        st.warning("Please enter a query first.")
    elif not check_elasticsearch():
        st.error("Elasticsearch is not running. Start Docker/Elasticsearch first, then try again.")
    else:
        try:
            if run_rag:
                with st.spinner("Retrieving passages and generating answer..."):
                    result = answer_query(
                        query=query,
                        top_k=top_k,
                        max_new_tokens=max_new_tokens
                    )

                st.subheader("Generated Answer")
                st.success(result["answer"])

                passages = result["passages"]

            else:
                with st.spinner("Searching with BM25..."):
                    passages = bm25_search(query, top_k=top_k)

            if show_passages:
                st.subheader("Retrieved Passages")

                for i, passage in enumerate(passages, start=1):
                    title = f"Passage {i} | ID: {passage['passage_id']}"
                    if show_scores:
                        title += f" | BM25 Score: {passage['score']:.4f}"

                    with st.expander(title, expanded=(i == 1)):
                        st.write(passage["text"])

        except Exception as e:
            st.error("Something went wrong while running the search or RAG pipeline.")
            st.exception(e)


st.divider()

st.subheader("How to use this app")
st.markdown(
    """
1. Start Elasticsearch in Docker.
2. Run `python -X utf8 prepare_data.py --limit 50000`.
3. Run `python create_index_bm25.py`.
4. Run `python bulk_index_bm25.py`.
5. Start this app with `streamlit run streamlit_app.py`.
"""
)
