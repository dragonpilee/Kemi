import os
import io
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import fitz  # PyMuPDF
import pytesseract
from PIL import Image

from langchain_community.llms import Ollama
from langchain_community.embeddings import OllamaEmbeddings
from langchain_core.prompts import PromptTemplate
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
import chromadb
import uuid
import docx

app = FastAPI(title="Kemi: Biochemical Lab Analyzer API")

# Setup CORS to allow Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

OLLAMA_URL = os.getenv("OLLAMA_BASE_URL", "http://ollama:11434")
CHROMA_URL = os.getenv("CHROMA_DB_URL", "http://chromadb:8000")

# Initialize models
try:
    llm = Ollama(model="medgemma1.5:4b", base_url=OLLAMA_URL)
    embeddings = OllamaEmbeddings(model="nomic-embed-text", base_url=OLLAMA_URL)
    
    # Connect to remote ChromaDB container
    chroma_client = chromadb.HttpClient(host=CHROMA_URL.split("://")[1].split(":")[0], port=8000)
    vector_store = Chroma(client=chroma_client, collection_name="lab_reports", embedding_function=embeddings)
except Exception as e:
    print(f"Warning: Could not initialize AI models or Vector DB on startup. {e}")

class AnalysisResponse(BaseModel):
    document_id: str
    extracted_text: str
    biochemical_analysis: str

def extract_text_from_pdf(file_bytes: bytes) -> str:
    text = ""
    try:
        doc = fitz.open(stream=file_bytes, filetype="pdf")
        for page in doc:
            text += page.get_text()
    except Exception as e:
        raise Exception(f"PDF Parsing failed: {e}")
    return text

def extract_text_from_image(file_bytes: bytes) -> str:
    try:
        image = Image.open(io.BytesIO(file_bytes))
        # Convert to RGB if it's not (e.g., RGBA or P) to ensure Tesseract works well
        if image.mode != 'RGB':
            image = image.convert('RGB')
        text = pytesseract.image_to_string(image)
    except Exception as e:
        raise Exception(f"OCR failed: {e}")
    return text

def extract_text_from_docx(file_bytes: bytes) -> str:
    try:
        doc = docx.Document(io.BytesIO(file_bytes))
        text = "\n".join([para.text for para in doc.paragraphs])
    except Exception as e:
        raise Exception(f"DOCX Parsing failed: {e}")
    return text

def extract_text_from_raw(file_bytes: bytes) -> str:
    try:
        text = file_bytes.decode("utf-8")
    except Exception as e:
        raise Exception(f"Text decoding failed (ensure the file is UTF-8 encoded): {e}")
    return text

@app.post("/api/analyze", response_model=AnalysisResponse)
async def analyze_document(file: UploadFile = File(...)):
    contents = await file.read()
    extracted_text = ""
    filename = file.filename.lower()

    if file.content_type == "application/pdf" or filename.endswith(".pdf"):
        extracted_text = extract_text_from_pdf(contents)
    elif file.content_type.startswith("image/") or filename.endswith((".png", ".jpg", ".jpeg", ".tiff", ".bmp", ".webp", ".gif")):
        extracted_text = extract_text_from_image(contents)
    elif "wordprocessingml.document" in file.content_type or filename.endswith(".docx"):
        extracted_text = extract_text_from_docx(contents)
    elif file.content_type.startswith("text/") or filename.endswith((".txt", ".csv", ".md", ".json")):
        extracted_text = extract_text_from_raw(contents)
    else:
        raise HTTPException(status_code=400, detail="Unsupported file format. Please upload an Image, PDF, DOCX, or Text file.")

    if not extracted_text.strip():
        raise HTTPException(status_code=400, detail="Could not extract any text from the document.")

    # 1. Chunk the extracted text
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    chunks = text_splitter.split_text(extracted_text)

    # Generate a unique document ID
    document_id = str(uuid.uuid4())

    # 2. Store chunks in Chroma Vector Database with metadata
    try:
        doc_ids = [str(uuid.uuid4()) for _ in chunks]
        metadatas = [{"document_id": document_id} for _ in chunks]
        vector_store.add_texts(texts=chunks, metadatas=metadatas, ids=doc_ids)
    except Exception as e:
        print(f"Vector DB storage failed: {e}")

    # 3. Retrieve the most relevant chunks for analysis
    try:
        # We query the DB for the most chemically relevant parts of the text
        query = "abnormal lab values, chemical markers, enzymes, diseases, medications"
        relevant_docs = vector_store.similarity_search(
            query, 
            k=5, 
            filter={"document_id": document_id}
        )
        context = "\n\n".join([doc.page_content for doc in relevant_docs])
    except Exception as e:
        context = extracted_text[:4000] # Fallback to raw text if retrieval fails

    # Prepare LangChain prompt for biochemical analysis using RAG context
    template = """
    You are an expert Biochemist and Medical Pathologist. 
    Review the following retrieved context from a chemical pathology lab report or medication list.
    
    Identify any abnormal chemical markers, enzymes (like AST, ALT), or chemical compounds/drugs.
    Explain the biochemical mechanisms happening in the patient's body that would cause these abnormalities, and potential chemical interactions.
    Keep the explanation highly scientific but structured and easy to read.

    Retrieved Clinical Context:
    {context}

    Biochemical Analysis:
    """
    
    prompt = PromptTemplate(template=template, input_variables=["context"])
    
    try:
        chain = prompt | llm
        analysis = chain.invoke({"context": context})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI Analysis failed: {e}")

    return AnalysisResponse(
        document_id=document_id,
        extracted_text=extracted_text,
        biochemical_analysis=analysis
    )

@app.get("/api/health")
def health_check():
    return {"status": "ok", "service": "Kemi API"}
