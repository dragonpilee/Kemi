# Kemi 🧪
**Biochemical Lab & Pharmacology Analyzer**

Kemi is a privacy-first, fully containerized AI application designed to scan, parse, and analyze chemical pathology reports and medication lists. By merging Chemistry and Computer Science, Kemi doesn't just read medical data—it explains the **biochemical mechanisms** and **chemical pathways** causing abnormalities in the body using local, open-weights AI models.

## 🚀 Features

- **Document Scanning:** Upload clinical PDFs or images. Uses `PyMuPDF` for PDF parsing and `Tesseract` for Optical Character Recognition (OCR).
- **Retrieval-Augmented Generation (RAG):** Extracts chemical markers and chunks them into a local **ChromaDB** vector database using `nomic-embed-text` embeddings.
- **Biochemical Intelligence:** Uses Google's **MedGemma** (`medgemma1.5:4b`) to analyze the retrieved context and generate highly scientific, yet readable, biochemical breakdowns.
- **Premium UI:** A stunning, responsive Next.js frontend featuring dark-mode aesthetics and glassmorphism.
- **100% Local & Private:** All inference and data storage happens locally on your machine. No data is sent to the cloud.
- **Native GPU Acceleration:** Offloads the heavy AI inference natively to your host machine's NVIDIA GPU, avoiding Docker GPU virtualization bottlenecks.

---

## 🛠️ Tech Stack

### Infrastructure
- **Docker & Docker Compose** (Full orchestration)
- **NVIDIA Container Toolkit** (For GPU CUDA acceleration)

### Frontend (`/frontend`)
- **Framework:** Next.js (React)
- **Styling:** Vanilla CSS (CSS Variables, Glassmorphism, Responsive Grid)

### Backend (`/backend`)
- **API Framework:** Python FastAPI
- **Document Processing:** PyMuPDF (`fitz`), Tesseract OCR, Pillow
- **AI/RAG Framework:** LangChain
- **Vector Database:** ChromaDB

### AI Engine (Host Machine)
- **Server:** Ollama (Running natively on the host PC)
- **LLM:** `medgemma1.5:4b` (Medical-domain reasoning)
- **Embeddings:** `nomic-embed-text:latest` (Semantic text embedding)

---

## ⚙️ Prerequisites

Before you begin, ensure you have the following installed on your host machine:
1. **Docker Desktop** (or Docker Engine)
2. **NVIDIA GPU Drivers** (If using GPU acceleration)
3. **NVIDIA Container Toolkit** (Required for Docker to access your GPU)

---

## 💻 Installation & Setup

1. **Clone the repository** and navigate to the project root:
   ```bash
   cd d:\Projects\med
   ```

2. **Build and start the Docker containers** in detached mode:
   ```bash
   docker-compose up -d --build
   ```

3. **Ensure Ollama is Running on Your PC**
   Since Kemi connects to your host machine's Ollama instance, ensure Ollama is running and you have the required models pulled:
   ```bash
   ollama run medgemma1.5:4b
   ollama pull nomic-embed-text
   ```

4. **Access the Application**
   Open your browser and navigate to: **[http://localhost:3005](http://localhost:3005)**

---

## 🩺 Usage

1. Open Kemi at `http://localhost:3005`.
2. Drag and drop a PDF or image of a lab report (e.g., a Comprehensive Metabolic Panel or a Blood Test result) into the upload zone.
3. Click **Scan & Analyze**.
4. The system will extract the raw data, isolate the most chemically relevant information via ChromaDB, and present a detailed biochemical breakdown of the patient's state.

---

## 🧠 Architecture & Pipeline

Kemi utilizes a Retrieval-Augmented Generation (RAG) architecture split between Docker containers and your host machine's native hardware for maximum GPU efficiency.

1. **Upload Phase:** The user uploads a PDF or image via the **Next.js Frontend** (Port 3005).
2. **Extraction Phase:** The **FastAPI Backend** (Port 8000) intercepts the file and uses `PyMuPDF` or `Tesseract OCR` to extract raw text.
3. **Embedding Phase:** The backend chunks the text and calls the host machine's Ollama service (`host.docker.internal:11434`) to generate embeddings using `nomic-embed-text`.
4. **Vector Storage:** The embeddings and text chunks are stored in the Dockerized **ChromaDB** container.
5. **Retrieval Phase:** The backend queries ChromaDB for the most chemically relevant data points (enzymes, biomarkers).
6. **Generation Phase:** The highly specific context is injected into a prompt and sent to the host machine's `medgemma1.5:4b` model to generate the biochemical analysis.
7. **Delivery:** The final report is sent back and rendered on the frontend.

---

## 🏗️ Project Structure

```text
├── backend/
│   ├── Dockerfile          # FastAPI environment & system OCR dependencies
│   ├── main.py             # API routes, LangChain RAG pipeline, AI prompting
│   └── requirements.txt    # Python dependencies
├── frontend/
│   ├── src/app/            # Next.js React components and pages
│   ├── Dockerfile          # Node.js build environment
│   └── package.json        # Frontend dependencies
├── docker-compose.yml      # Orchestrates Frontend, Backend, and ChromaDB
└── README.md
```

---
*Built to bridge the gap between Computer Science and Biochemistry.*
