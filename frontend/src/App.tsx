import { useEffect, useState } from 'react';
import {
  Navbar,
  UploadBox,
  XrayPreview,
  PredictionCard,
  HeatmapViewer,
  HistoryTable,
} from './components/ui';
import { analyzeImage, fetchHistory, type HistoryItem, type PredictionResult } from './services/api';

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export default function App() {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [previewUrl, setPreviewUrl] = useState('');
  const [result, setResult] = useState<PredictionResult | null>(null);
  const [history, setHistory] = useState<HistoryItem[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchHistory().then(setHistory).catch(() => setHistory([]));
  }, []);

  useEffect(() => () => {
    if (previewUrl) URL.revokeObjectURL(previewUrl);
  }, [previewUrl]);

  const handleFileSelected = (file: File) => {
    if (!['image/png', 'image/jpeg'].includes(file.type)) {
      setError('Please upload a JPG, JPEG, or PNG dental X-ray.');
      return;
    }
    setSelectedFile(file);
    setPreviewUrl((previous) => {
      if (previous) URL.revokeObjectURL(previous);
      return URL.createObjectURL(file);
    });
    setResult(null);
    setError('');
  };

  const handleAnalyze = async () => {
    if (!selectedFile) {
      setError('Please upload a dental X-ray before analyzing.');
      return;
    }
    setLoading(true);
    setError('');
    try {
      const prediction = await analyzeImage(selectedFile);
      setResult({
        ...prediction,
        heatmap_url: prediction.heatmap_url
          ? `${API_BASE}${prediction.heatmap_url}`
          : null,
      });
      setHistory((previous) => [
        {
          id: prediction.id,
          predicted_age: prediction.predicted_age,
          uncertainty: prediction.uncertainty,
          model_version: prediction.model_version,
          created_at: prediction.created_at,
          status: prediction.status || 'completed',
          original_filename: selectedFile.name,
        },
        ...previous,
      ]);
    } catch (caught) {
      setError(caught instanceof Error ? caught.message : 'Something went wrong while analyzing the image.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-shell">
      <Navbar />
      <main>
        <section className="hero">
          <div className="hero-panel">
            <div className="hero-kicker">Research prototype</div>
            <h1>Explainable panoramic X-ray age estimation.</h1>
            <p>Upload a dental radiograph, run the regression pipeline, and inspect the image regions that influenced the estimate.</p>
            <button className="primary-button" onClick={() => document.getElementById('analyze')?.scrollIntoView({ behavior: 'smooth' })}>
              Analyze an X-ray
            </button>
          </div>
          <div className="preview-card hero-visual">
            <div className="scan-lines" aria-hidden="true" />
            <span>DentalAge AI</span>
            <small>Explainable image analysis</small>
          </div>
        </section>

        <section className="section-grid">
          <div className="panel info-card"><h3>01 · Upload</h3><p>Provide a readable JPG, JPEG, or PNG panoramic radiograph.</p></div>
          <div className="panel info-card"><h3>02 · Estimate</h3><p>A PyTorch regression model returns a continuous age estimate.</p></div>
          <div className="panel info-card"><h3>03 · Explain</h3><p>Grad-CAM highlights visual regions used by the model.</p></div>
        </section>

        <section id="analyze" className="analyze-layout">
          <div>
            <UploadBox onFileSelected={handleFileSelected} />
            {selectedFile && <p className="file-name">Selected: {selectedFile.name}</p>}
            {error && <div className="panel error-message" role="alert">{error}</div>}
            <button className="primary-button analyze-button" onClick={handleAnalyze} disabled={loading || !selectedFile}>
              {loading ? 'Analyzing…' : 'Analyze image'}
            </button>
            {loading && <div className="panel loading-message">Validating image · preprocessing · running model · generating explanation</div>}
          </div>
          <XrayPreview src={previewUrl} />
        </section>

        <section className="results-grid">
          <PredictionCard result={result} />
          <HeatmapViewer src={result?.heatmap_url || undefined} />
        </section>

        <section className="panel explainability-panel">
          <h2>How to interpret the heatmap</h2>
          <p>Grad-CAM indicates image regions that influenced the model output. It is a visual-saliency aid, not proof of a medical or causal relationship.</p>
        </section>

        <section id="history" className="content-section">
          <h2>Analysis history</h2>
          <HistoryTable items={history} />
        </section>

        <section id="about" className="panel content-section">
          <h2>Responsible use</h2>
          <p>This application provides an AI-estimated dental age for research and educational purposes. It is not a definitive determination of chronological age and should not be used as the sole basis for medical, legal, forensic, or identity-related decisions.</p>
        </section>
      </main>
    </div>
  );
}
