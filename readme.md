# Kemi 🧪
> **Biochemical Lab & Pharmacology Analyzer**

![Status](https://img.shields.io/badge/Status-Stable-blue?style=for-the-badge) ![Docker](https://img.shields.io/badge/Deployment-Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white) ![FastAPI](https://img.shields.io/badge/Framework-FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white) ![Next.js](https://img.shields.io/badge/Frontend-Next.js-black?style=for-the-badge&logo=next.js&logoColor=white) ![Python](https://img.shields.io/badge/Language-Python-3776AB?style=for-the-badge&logo=python&logoColor=white)

**Kemi** is a privacy-first, fully containerized AI application designed to scan, parse, and analyze chemical pathology reports and medication lists. By merging Chemistry and Computer Science, Kemi doesn't just read medical data—it explains the **biochemical mechanisms** and **chemical pathways** causing abnormalities in the body using local, open-weights AI models.

---

## ✨ Features

- **📄 Universal Document Parsing**: Upload any medical report—supports PDFs, DOCX, TXT, CSV, and all major Image formats natively.
- **👁️ Optical Character Recognition**: Built-in PyMuPDF and Tesseract engines to flawlessly extract text from clinical scans.
- **🧠 Retrieval-Augmented Generation (RAG)**: Extracts chemical markers and chunks them into a local **ChromaDB** vector database.
- **🧬 Biochemical Intelligence**: Uses Google's **MedGemma** (`medgemma1.5:4b`) to generate highly scientific, yet readable, biochemical breakdowns.
- **🎨 Premium UI**: A stunning, responsive Next.js frontend featuring dark-mode aesthetics and glassmorphism.
- **🔒 100% Local & Private**: All inference and data storage happens locally on your machine. No patient data is sent to the cloud.
- **⚡ Native GPU Acceleration**: Offloads the heavy AI inference natively to your host machine's NVIDIA GPU, avoiding Docker GPU virtualization bottlenecks.

---

## 🚀 Quick Start

### Prerequisites

1.  **Docker Desktop**: Ensure Docker is installed and running.
2.  **Ollama**: Installed and running on your host machine.
3.  **Git**: To clone the repository.
    * *Note: No Node.js or Python environments are required to run the frontend or backend servers.*

### Installation & Run

1.  Clone the repository and navigate to the root:
    ```bash
    git clone https://github.com/dragonpilee/Kemi.git
    cd Kemi
    ```

2.  Ensure Ollama is running and has the required models:
    ```bash
    ollama run medgemma1.5:4b
    ollama pull nomic-embed-text
    ```

3.  Build and launch the containers:
    ```bash
    docker-compose up -d --build
    ```

4.  Open your browser and visit:
    **[http://localhost:3005](http://localhost:3005)**

---

## 🧠 Architecture & Pipeline

Kemi utilizes a highly optimized Retrieval-Augmented Generation (RAG) architecture split between Docker containers and your host machine's native hardware:

1. **Upload Phase:** The user uploads a report via the Next.js Frontend (Port 3005).
2. **Extraction Phase:** The FastAPI Backend (Port 8000) parses the file using PyMuPDF or Tesseract OCR to extract raw text.
3. **Embedding Phase:** The text is chunked and sent to the host machine's Ollama service (`host.docker.internal:11434`) to generate embeddings using `nomic-embed-text`.
4. **Vector Storage:** The embeddings are stored in the Dockerized ChromaDB container.
5. **Retrieval Phase:** The backend queries ChromaDB for the most chemically relevant data points (enzymes, biomarkers).
6. **Generation Phase:** The context is injected into a prompt and sent to the host machine's `medgemma1.5:4b` model to generate the biochemical analysis.
7. **Delivery:** The final report is rendered cleanly on the frontend.

---

## 🛠️ Technology Stack

| Component | Technology |
|----------|------------|
| **Frontend Framework** | Next.js (React) |
| **Backend Framework** | Python FastAPI |
| **Styling** | Vanilla CSS (Glassmorphism) |
| **Vector Database** | ChromaDB |
| **Language Models** | `medgemma1.5:4b`, `nomic-embed-text` |
| **Document Processing** | PyMuPDF, Tesseract OCR, python-docx |
| **Infrastructure** | Docker, Docker Compose |
| **AI Engine** | Ollama |

---

## 🤝 Contributing

**Important:** This project enforces a strict Docker-only workflow for its services.

1.  **Fork & Branch**: Create a new branch for your feature (`git checkout -b feature/improvement`).
2.  **Develop**: Test all changes inside the container (`docker-compose up`).
3.  **Commit & Push**: Submit your changes via Pull Request.

---

## 📄 License & Acknowledgements

This project is licensed under the [MIT License](LICENSE).

* **Google** for MedGemma
* **Nomic** for embedding models
* **Chroma** for the vector database

<div align="center">
  <sub>Developed with ❤️ by dragonpilee</sub><br>
  <sub>If you find this project helpful, please consider ⭐ <a href="https://github.com/dragonpilee/Kemi">starring the repository!</a></sub>
</div>
