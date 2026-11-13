
# 📘 Multi-PDF RAG Application – Endress+Hauser Sensor Datasheets

A beginner-friendly **Retrieval-Augmented Generation (RAG)** application developed using Python, Streamlit, LangChain, FAISS, and OpenAI API.

This application allows users to upload multiple Endress+Hauser sensor datasheets, extract technical information, and ask questions using an AI-powered question-answering interface with source PDF and page number references.

---

## 🎯 1. Project Objectives

The main objective is to develop a Multi-PDF RAG application that can:

- Upload multiple PDF datasheets simultaneously.
- Extract text from PDF documents.
- Split extracted text into smaller chunks.
- Generate embeddings using OpenAI.
- Store document embeddings in a FAISS vector database.
- Retrieve relevant information from multiple PDF documents.
- Generate answers using OpenAI ChatGPT.
- Display source PDF filename and exact page number.
- Compare technical specifications of two instruments.
- Avoid generating incorrect or unsupported technical specifications.

---

## 📂 2. Input PDF Documents

The application supports the following Endress+Hauser sensor datasheets:

**PDF 1:**
`Endress-Hauser_Micropilot_FMR51_EN.pdf`

**PDF 2:**
`Endress-Hauser_Promag_H_200_5H2B_EN.pdf`

Both PDF documents are processed together and stored in a single FAISS vector database.

> Note: PDF documents are uploaded through the Streamlit application. They are not hardcoded into the Python application.

---

## 🛠️ 3. Technologies Used

| Technology | Purpose |
|---|---|
| Python | Programming language |
| Streamlit | Web application interface |
| LangChain | RAG application framework |
| PyPDFLoader | Extract PDF text |
| RecursiveCharacterTextSplitter | Split text into chunks |
| OpenAIEmbeddings | Generate text embeddings |
| FAISS | Vector database |
| ChatOpenAI | AI-generated answers |
| python-dotenv | Manage API keys |

---

## 📁 4. Project Structure

```text
Multi_PDF_RAG/
│
├── rag_app.py
├── README.md
├── .env
├── .gitignore
│
├── Endress-Hauser_Micropilot_FMR51_EN.pdf
└── Endress-Hauser_Promag_H_200_5H2B_EN.pdf
```

---

## ⚙️ 5. Installation and Setup

### Step 1: Create Project Folder

```bash
mkdir Multi_PDF_RAG
cd Multi_PDF_RAG
```

Place `rag_app.py` inside this folder.

### Step 2: Create Virtual Environment

```bash
python -m venv venv
```

Activate the virtual environment.

**Windows Command Prompt:**

```bash
venv\Scripts\activate
```

**Windows PowerShell:**

```powershell
.\venv\Scripts\Activate.ps1
```

### Step 3: Install Required Libraries

Run the following command:

```bash
pip install streamlit langchain langchain-community langchain-openai langchain-text-splitters faiss-cpu pypdf python-dotenv
```

### Step 4: Configure OpenAI API Key

Create a file named `.env` in the project folder.

Add your OpenAI API key:

```env
OPENAI_API_KEY=your_openai_api_key_here
```

Replace the example value with your actual API key.

**Important:** Never upload your API key or `.env` file to GitHub.

### Step 5: Run the Application

Execute:

```bash
streamlit run rag_app.py
```

The application will open in your default browser.

Local URL:

```text
http://localhost:8501
```

---

## 🚀 6. Application Workflow

The application follows a basic RAG architecture.

```text
       PDF Upload
            |
            v
     PDF Text Extraction
        (PyPDFLoader)
            |
            v
      Text Splitting
  (RecursiveCharacterTextSplitter)
            |
            v
    Generate Embeddings
     (OpenAIEmbeddings)
            |
            v
     FAISS Vector Database
            |
            v
       User Question
            |
            v
   Similarity Search / Retrieval
            |
            v
      Relevant PDF Context
            |
            v
      ChatOpenAI (LLM)
            |
            v
      Generated Answer
            |
            v
     Source PDF + Page Number
```

---

## 💡 7. Application Features

### 1. Multiple PDF Upload

- Upload both sensor datasheets simultaneously.
- Support multiple PDF documents.
- Validate PDF files before processing.

### 2. Document Processing

- Extract PDF text using PyPDFLoader.
- Split documents into smaller text chunks.
- Preserve original filename and page metadata.

### 3. Vector Database

- Generate embeddings using OpenAI.
- Store all document vectors in one FAISS database.
- Retrieve relevant document sections using similarity search.

### 4. AI Question Answering

- Ask technical questions about individual sensors.
- Retrieve information from both datasheets.
- Generate answers using ChatOpenAI.
- Support comparison between instruments.

### 5. Source Citations

Every answer displays:

- Original PDF filename.
- PDF page number.
- Unique source references without duplicate filename/page combinations.

Page numbering starts from 1.

### 6. Error Handling

The application handles:

- Missing OpenAI API key.
- Invalid PDF documents.
- Empty PDF text.
- PDF processing errors.
- API and indexing errors.

---

## ❓ 8. Example Questions

### Micropilot FMR51

1. What is the measurement range of Micropilot FMR51?
2. What is the measuring principle of FMR51?
3. What are the available output signals?
4. What are the available communication protocols?

### Promag H 200

1. What is the flow measurement range of Promag H 200?
2. What is the accuracy of Promag H 200?
3. What is the measuring principle?
4. What are the available communication protocols?

### Instrument Comparison

1. Compare the technical specifications of both instruments.
2. Compare the measuring principles of FMR51 and Promag H 200.
3. What are the differences between the two instruments?
4. Compare the available communication protocols.

---

## 📚 9. RAG Response Rules

The application is designed to follow these rules:

- Generate answers using retrieved information from uploaded datasheets only.
- Never invent technical specifications.
- Do not assume missing measurement ranges, accuracy, units, or communication protocols.
- For comparison questions, compare only available information.
- Display source filename and page number.

If information is unavailable, the application should respond:

```text
Information not available in the uploaded datasheets.
```

**Engineering Note:** Always verify important technical specifications against the original manufacturer's datasheet before making engineering, procurement, or installation decisions.

---

## 🔍 10. Troubleshooting

| Error / Issue | Solution |
|---|---|
| ModuleNotFoundError | Install the required Python libraries. |
| OPENAI_API_KEY not found | Check the `.env` file and API key variable. |
| OpenAI Authentication Error | Verify your API key. |
| OpenAI API quota error | Check your API billing and usage limits. |
| Invalid PDF | Check whether the PDF file is corrupted or password-protected. |
| No readable PDF text | Check whether the PDF is scanned or image-only. |
| Streamlit command not found | Install Streamlit in the active virtual environment. |
| Port 8501 already in use | Run Streamlit using another port. |

To use another port:

```bash
streamlit run rag_app.py --server.port 8502
```

**Note:** This basic application does not include OCR support for scanned PDF documents.

---

## 🔐 11. GitHub Security – .gitignore

Create a `.gitignore` file to prevent sensitive files and unnecessary generated files from being uploaded.

```gitignore
# Environment variables
.env
.env.*

# Python cache
__pycache__/
*.py[cod]

# Virtual environment
venv/
.venv/

# Streamlit secrets
.streamlit/secrets.toml

# Generated vector database
faiss_index/
*.faiss
*.pkl
```

Never upload API keys, passwords, or confidential datasheets to a public GitHub repository without authorization.

---

## 🔮 12. Future Improvements

Possible future enhancements:

- Add OCR support for scanned datasheets.
- Display retrieved text snippets.
- Add chat history.
- Allow downloading AI-generated answers.
- Implement persistent FAISS vector storage.
- Add document-specific search filters.
- Develop a technical datasheet comparison dashboard.

These enhancements are not included in the current version.

---

## 👨‍💻 13. Author

**Rajesh B**

Project Engineer | Electrical, Electronics & Instrumentation

Interested in:

- Industrial Instrumentation
- Sensor Integration
- Data Acquisition Systems (DAQ)
- IoT and Cloud Connectivity
- Python Programming
- Generative AI
- Retrieval-Augmented Generation (RAG)

---

## 🏁 14. Project Summary

**Project Name:** Multi-PDF RAG Application – Endress+Hauser Sensor Datasheets

**Objective:** Develop an AI-powered technical document assistant capable of retrieving and answering engineering questions from multiple sensor datasheets with source citations.

**Key Learning Outcomes:**

- Python application development.
- LangChain framework.
- OpenAI API integration.
- Text embedding generation.
- FAISS vector database.
- Retrieval-Augmented Generation (RAG).
- Streamlit web application development.
- PDF-based technical information retrieval.

**Developed as a practical Python and Generative AI learning project.**
