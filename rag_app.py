import os
import tempfile

import streamlit as st
from dotenv import load_dotenv

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain_core.messages import HumanMessage, SystemMessage


# ============================================================
# 1. PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Endress+Hauser Sensor Datasheet RAG",
    page_icon="📘",
    layout="wide"
)

st.title("📘 Multi-PDF RAG Application")
st.caption("Ask technical questions about the Endress+Hauser sensor datasheets.")

load_dotenv()


# ============================================================
# 2. SESSION STATE
# ============================================================

if "vector_store" not in st.session_state:
    st.session_state.vector_store = None

if "pdf_count" not in st.session_state:
    st.session_state.pdf_count = 0

if "chunk_count" not in st.session_state:
    st.session_state.chunk_count = 0

if "indexed_files" not in st.session_state:
    st.session_state.indexed_files = []


# ============================================================
# 3. PDF UPLOAD SECTION
# ============================================================

st.subheader("1. Upload PDF datasheets")

uploaded_files = st.file_uploader(
    "Select the two sensor datasheets (PDF format)",
    type=["pdf"],
    accept_multiple_files=True,
    help=(
        "Upload Endress-Hauser_Micropilot_FMR51_EN.pdf and "
        "Endress-Hauser_Promag_H_200_5H2B_EN.pdf."
    )
)

if uploaded_files:
    st.write(f"**PDF files selected:** {len(uploaded_files)}")
    for uploaded_file in uploaded_files:
        st.write(f"📄 {uploaded_file.name}")


# ============================================================
# 4. INDEX THE UPLOADED PDF DOCUMENTS
# ============================================================

st.subheader("2. Process and index documents")

if st.button("🔍 Index Documents", type="primary"):
    if not uploaded_files:
        st.error("Please upload at least one PDF file.")
    elif not os.getenv("OPENAI_API_KEY"):
        st.error(
            "OPENAI_API_KEY was not found. Add it to a .env file "
            "in the same folder as rag_app.py."
        )
    else:
        all_documents = []
        successfully_loaded_files = []
        failed_files = []

        with st.spinner("Reading and processing PDF documents..."):
            for uploaded_file in uploaded_files:
                try:
                    # PyPDFLoader reads from a file path, so save the upload temporarily.
                    with tempfile.NamedTemporaryFile(
                        delete=False, suffix=".pdf"
                    ) as temporary_pdf:
                        temporary_pdf.write(uploaded_file.getvalue())
                        temporary_path = temporary_pdf.name

                    try:
                        loader = PyPDFLoader(temporary_path)
                        pdf_pages = loader.load()
                    finally:
                        # Remove the temporary file after loading.
                        if os.path.exists(temporary_path):
                            os.remove(temporary_path)

                    # Keep the original uploaded filename in every page's metadata.
                    valid_pages = []
                    for page in pdf_pages:
                        page.page_content = page.page_content.strip()
                        page.metadata["source"] = uploaded_file.name
                        if page.page_content:
                            valid_pages.append(page)

                    if not valid_pages:
                        failed_files.append(
                            f"{uploaded_file.name}: no readable text found."
                        )
                    else:
                        all_documents.extend(valid_pages)
                        successfully_loaded_files.append(uploaded_file.name)

                except Exception as error:
                    failed_files.append(
                        f"{uploaded_file.name}: could not read PDF ({error})."
                    )

            if all_documents:
                try:
                    # Split pages into smaller sections for retrieval.
                    text_splitter = RecursiveCharacterTextSplitter(
                        chunk_size=1000,
                        chunk_overlap=150
                    )
                    chunks = text_splitter.split_documents(all_documents)

                    if not chunks:
                        st.error("No text chunks were created from the uploaded PDFs.")
                    else:
                        # Create embeddings and one FAISS index for all uploaded PDFs.
                        embeddings = OpenAIEmbeddings(
                            model="text-embedding-3-small"
                        )
                        vector_store = FAISS.from_documents(chunks, embeddings)

                        # Save the index and summary in Streamlit session state.
                        st.session_state.vector_store = vector_store
                        st.session_state.pdf_count = len(successfully_loaded_files)
                        st.session_state.chunk_count = len(chunks)
                        st.session_state.indexed_files = successfully_loaded_files

                        st.success("PDF documents indexed successfully.")

                except Exception as error:
                    st.session_state.vector_store = None
                    st.error(f"Indexing failed: {error}")
            else:
                st.session_state.vector_store = None
                st.error(
                    "No readable PDF text was found. Check that the PDFs contain "
                    "selectable text and are not image-only scanned documents."
                )

        for message in failed_files:
            st.warning(message)


# ============================================================
# 5. DISPLAY INDEX SUMMARY
# ============================================================

st.subheader("3. Index summary")

col1, col2 = st.columns(2)
col1.metric("Indexed PDF documents", st.session_state.pdf_count)
col2.metric("Indexed text chunks", st.session_state.chunk_count)

if st.session_state.indexed_files:
    st.write("**Indexed files:**")
    for filename in st.session_state.indexed_files:
        st.write(f"📄 {filename}")


st.divider()


# ============================================================
# 6. QUESTION AND ANSWER SECTION
# ============================================================

st.subheader("4. Ask questions about the datasheets")

st.write(
    "Ask about either instrument or compare the Micropilot FMR51 "
    "and Promag H 200."
)

example_questions = [
    "What is the measurement range of Micropilot FMR51?",
    "What is the measuring principle of FMR51?",
    "What is the flow measurement range of Promag H 200?",
    "What is the accuracy of Promag H 200?",
    "What are the available communication protocols?",
    "Compare the technical specifications of both instruments."
]

with st.expander("View example questions"):
    for question in example_questions:
        st.write(f"• {question}")

user_question = st.text_input(
    "Enter your technical question:",
    placeholder="Example: Compare the measuring principles of both instruments."
)

if st.button("💬 Get Answer"):
    if not user_question.strip():
        st.warning("Please enter a question.")
    elif st.session_state.vector_store is None:
        st.warning("Please upload and index the PDF documents first.")
    elif not os.getenv("OPENAI_API_KEY"):
        st.error("OPENAI_API_KEY was not found in the .env file.")
    else:
        with st.spinner("Searching the datasheets and preparing an answer..."):
            try:
                # Retrieve the most relevant text sections from the combined index.
                retrieved_documents = st.session_state.vector_store.similarity_search(
                    user_question,
                    k=6
                )

                if not retrieved_documents:
                    st.info(
                        "Information not available in the uploaded datasheets."
                    )
                else:
                    # Build unique source references using filename and 1-based page.
                    source_references = []
                    seen_sources = set()
                    context_sections = []

                    for document in retrieved_documents:
                        filename = document.metadata.get("source", "Unknown PDF")

                        # PyPDFLoader page metadata is zero-based; show page numbers from 1.
                        page_index = document.metadata.get("page")
                        if page_index is None:
                            page_number = "Unknown"
                        else:
                            page_number = int(page_index) + 1

                        source_key = (filename, page_number)

                        if source_key not in seen_sources:
                            seen_sources.add(source_key)
                            source_references.append(source_key)

                        context_sections.append(
                            f"Source: {filename}, PDF page: {page_number}\n"
                            f"Content:\n{document.page_content}"
                        )

                    context = "\n\n---\n\n".join(context_sections)

                    system_prompt = """
You are a technical assistant answering questions using only the
provided Endress+Hauser sensor datasheet extracts.

Rules:
1. Use only facts explicitly supported by the supplied extracts.
2. Do not use outside knowledge or invent specifications, values,
   units, ranges, accuracy figures, protocols, or model details.
3. If the requested information is not present in the extracts,
   respond exactly:
   Information not available in the uploaded datasheets.
4. For comparison questions, compare only details supported by the
   extracts. Clearly say when a detail for one instrument is unavailable.
5. Be clear and concise. Preserve technical values and units exactly.
6. Do not create source filenames or page numbers. Source references
   will be displayed separately by the application.
"""

                    chat_model = ChatOpenAI(
                        model="gpt-4o-mini",
                        temperature=0
                    )

                    messages = [
                        SystemMessage(content=system_prompt),
                        HumanMessage(
                            content=(
                                f"Question:\n{user_question}\n\n"
                                f"Retrieved datasheet extracts:\n{context}"
                            )
                        )
                    ]

                    response = chat_model.invoke(messages)
                    answer = response.content

                    st.markdown("### Answer")
                    st.write(answer)

                    # Display each filename/page pair once.
                    st.markdown("### Sources")
                    if source_references:
                        for filename, page_number in source_references:
                            st.write(f"📄 **{filename}** — Page {page_number}")
                    else:
                        st.write("No source references were retrieved.")

            except Exception as error:
                st.error(f"An error occurred while answering your question: {error}")


# ============================================================
# 7. FOOTER
# ============================================================

st.divider()
st.caption(
    "This application answers questions from the uploaded datasheets only. "
    "Always verify critical engineering decisions against the original PDF."
)
