import os

import streamlit as st
from langchain_ollama import ChatOllama

import config
import knowledge_base

st.set_page_config(page_title="PDF RAG Demo", page_icon="📚", layout="wide")

@st.cache_resource
def load_vectorstore():
    # st.cache_resource keeps this from being recreated on every rerun -
    # the embedding model only needs to be loaded once per session.
    return knowledge_base.get_vectorstore()


vectorstore = load_vectorstore()

# -----------------------------------------------------------------------------
# Sidebar: settings + knowledge base management
# -----------------------------------------------------------------------------
with st.sidebar:
    st.header("Knowledge Base")

    documents = knowledge_base.list_documents(vectorstore)
    st.caption(f"{len(documents)} document(s) currently ingested")
    for doc_name in documents:
        st.write(f"- {doc_name}")

# -----------------------------------------------------------------------------
# Main area: ask a question
# -----------------------------------------------------------------------------
st.title("PDF RAG Demo")
st.write(
    "Ask a question about the ingested PDFs. The answer cites the exact "
    "pages it came from, including any tables and images."
)

question = st.text_input("Your question")
ask_clicked = st.button("Ask", type="primary")

if ask_clicked and question.strip():
    if not documents:
        st.warning("The knowledge base is empty. Ingest a PDF first (see the sidebar).")
    else:
        with st.spinner("Searching the knowledge base..."):
            results = vectorstore.similarity_search(question, k=config.TOP_K_RESULTS)

        if not results:
            st.info("No relevant content found for that question.")
        else:
            # Build a numbered context string. The same numbering is used
            # both in the LLM prompt and in the "Sources" section below, so
            # a citation like [2] in the answer always matches source [2].
            context_blocks = [
                f"[{i}] (from {doc.metadata['source']}, page {doc.metadata['page']}):\n{doc.page_content}"
                for i, doc in enumerate(results, start=1)
            ]
            context_text = "\n\n".join(context_blocks)

            st.subheader("Answer")
            prompt = (
                "You are answering strictly from the numbered context below. "
                "Do not use any outside knowledge and do not invent references, "
                "URLs, or sources that are not in the context. "
                "Cite the numbered source(s) you used inline, like [1] or [2]. "
                "If the context doesn't contain the answer, say so instead of guessing.\n\n"
                f"Context:\n{context_text}\n\n"
                f"Question: {question}\n\nAnswer:"
            )
            try:
                llm = ChatOllama(model=config.LLM_MODEL, temperature=0)
                with st.spinner(f"Asking {config.LLM_MODEL} (via Ollama)..."):
                    response = llm.invoke(prompt)
                st.write(response.content)
            except Exception as e:
                st.error(
                    f"Couldn't reach Ollama ({e}). Make sure it's running "
                    f"(`ollama serve`) and the model is pulled "
                    f"(`ollama pull {config.LLM_MODEL}`). Showing the raw "
                    "matching sources below instead."
                )

            st.subheader("Sources")
            icons = {"text": "📄", "table": "📊", "image": "🖼️"}
            for i, doc in enumerate(results, start=1):
                meta = doc.metadata
                content_type = meta.get("content_type", "text")
                icon = icons.get(content_type, "📄")
                label = f"[{i}] {icon} {meta['source']} — page {meta['page']} ({content_type})"
                with st.expander(label):
                    if content_type == "image":
                        image_path = meta.get("image_path")
                        if image_path and os.path.exists(image_path):
                            st.image(image_path)
                        # Prefer the AI-generated description; fall back to
                        # the raw chunk text if descriptions were disabled.
                        st.caption(meta.get("description") or doc.page_content)
                    elif content_type == "table":
                        if meta.get("description"):
                            st.caption(meta["description"])
                        st.markdown(meta.get("table_markdown", doc.page_content))
                    else:
                        st.write(doc.page_content)
