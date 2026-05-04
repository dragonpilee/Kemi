"use client";

import { useState } from "react";

export default function Home() {
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<{
    document_id: string;
    extracted_text: string;
    biochemical_analysis: string;
  } | null>(null);
  const [error, setError] = useState("");

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      setFile(e.target.files[0]);
    }
  };

  const handleUpload = async () => {
    if (!file) {
      setError("Please select a file first.");
      return;
    }

    setLoading(true);
    setError("");
    setResult(null);

    const formData = new FormData();
    formData.append("file", file);

    try {
      // Use localhost:3005 which points to the Docker host frontend, but we hit the backend at 8000
      const res = await fetch("http://localhost:8000/api/analyze", {
        method: "POST",
        body: formData,
      });

      if (!res.ok) {
        let errorMsg = "Failed to analyze document.";
        try {
          const errorData = await res.json();
          errorMsg = errorData.detail || errorMsg;
        } catch (_) {}
        throw new Error(errorMsg);
      }

      const data = await res.json();
      setResult(data);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="container">
      <header className="header">
        <h1>🧪 Kemi</h1>
        <p>Biochemical Lab & Pharmacology Analyzer</p>
      </header>

      <section className="upload-section glass">
        <div className="upload-box">
          <input
            type="file"
            accept="image/*,.pdf,.docx,.doc,.txt,.csv,.md"
            onChange={handleFileChange}
            id="file-upload"
            className="file-input"
          />
          <label htmlFor="file-upload" className="file-label">
            {file ? file.name : "Drag & Drop or Click to Upload Lab Report"}
          </label>
        </div>
        <button onClick={handleUpload} disabled={loading || !file} className="btn">
          {loading ? "Analyzing Biochemistry... This may take 1-2 minutes." : "Scan & Analyze"}
        </button>
        {error && <p className="error">{error}</p>}
      </section>

      {result && (
        <section className="results-grid">
          <div className="card glass">
            <h2>Raw Extracted Data</h2>
            <pre className="text-box">{result.extracted_text}</pre>
          </div>
          <div className="card glass highlight analysis-card">
            <h2>🧬 Biochemical Analysis</h2>
            <div className="analysis-box">
              {result.biochemical_analysis.split("\n").map((line, i) => (
                <p key={i}>{line}</p>
              ))}
            </div>
          </div>
        </section>
      )}

      <footer className="footer">
        <p>Developed with ❤️ by Alan Cyril Sunny</p>
      </footer>
    </main>
  );
}
