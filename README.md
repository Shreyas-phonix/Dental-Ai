import React, { useEffect, useState } from 'react';
import { Navbar, UploadBox, XrayPreview, PredictionCard, HeatmapViewer, HistoryTable } from './components/ui';
import { analyzeImage, fetchHistory } from './services/api';

function App() {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string>('');
  const [result, setResult] = useState<any>(null);
  const [history, setHistory] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string>('');

  useEffect(() => {
    fetchHistory().then(setHistory).catch(() => setHistory([]));
  }, []);

  useEffect(() => {
    return () => {
      if (previewUrl) URL.revokeObjectURL(previewUrl);
    };
  }, [previewUrl]);

  const handleFileSelected = (file: File) => {
    setSelectedFile(file);
    setPreviewUrl((prev) => {
      if (prev) URL.revokeObjectURL(prev);
      return URL.createObjectURL(file);
    });
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
      const normalized = {
        ...prediction,
        heatmap_url: prediction.heatmap_url ? `http://localhost:8000${prediction.heatmap_url}` : null,
      };
      setResult(normalized);
      setHistory((prev) => [{
        id: prediction.id,
        predicted_age: prediction.predicted_age,
        uncertainty: prediction.uncertainty,
        model_version: prediction.model_version,
        created_at: prediction.created_at,
        status: prediction.status || 'completed',
        original_filename: selectedFile.name,
      }, ...prev]);
    } catch (err: any) {
      setError(err.message || 'Something went wrong while analyzing the image.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-shell">
      <Navbar />

      <section className="hero">
        <div className="hero-panel">
          <div className="hero-kicker">Research-grade dental AI</div>
          <h1>Explainable panoramic X-ray age estimation.</h1>
          <p>
            DentalAge AI estimates biological age from dental radiographs using a transparent AI pipeline with a Grad-CAM explainability overlay and a responsible-use disclaimer.
          </p>
          <div style={{ display: 'flex', gap: 12, marginTop: 18, flexWrap: 'wrap' }}>
            <button className="primary-button" onClick={() => document.getElementById('analyze')?.scrollIntoView({ behavior: 'smooth' })}>Analyze now</button>
            <button className="secondary-button">See how it works</button>
          </div>
        </div>
        <div className="preview-card">
          <img src="https://images.unsplash.com/photo-1584515933487-779824d29309?auto=format&fit=crop&w=900&q=80" alt="Dental radiograph" style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
        </div>
      </section>

      <section className="section-grid">
        <div className="panel info-card">
          <h3>How it works</h3>
          <p>1. Upload panoramic dental image<br />2. Validate and preprocess<br />3. Run regression model<br />4. Review explainability</p>
        </div>
        <div className="panel info-card">
          <h3>Model</h3>
          <p>PyTorch CNN regression for continuous age estimation with Grad-CAM explainability overlays.</p>
        </div>
        <div className="panel info-card">
          <h3>Responsible use</h3>
          <p>This AI output is not a definitive age determination and is intended for research or educational review.</p>
        </div>
      </section>

      <section id="analyze" className="analyze-layout">
        <div>
          <UploadBox onFileSelected={handleFileSelected} />
          {selectedFile && <p style={{ marginTop: 12 }}>Selected file: {selectedFile.name}</p>}
          {error && <div className="panel" style={{ marginTop: 12, color: '#b42318' }}>{error}</div>}
          <div style={{ marginTop: 18 }}>
            <button className="primary-button" onClick={handleAnalyze} disabled={loading || !selectedFile}>{loading ? 'Analyzing...' : 'Analyze image'}</button>
          </div>
          {loading && <div className="panel" style={{ marginTop: 12 }}>Uploading X-ray → Validating image → Preprocessing → Running AI model → Generating explanation → Preparing result</div>}
        </div>
        <div>
          <XrayPreview src={previewUrl} />
        </div>
      </section>

      <section style={{ marginTop: 32 }}>
        <PredictionCard result={result} />
      </section>

      <section style={{ marginTop: 32, display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 24 }}>
        <HeatmapViewer src={result?.heatmap_url} />
        <div className="panel">
          <h3>Explainability note</h3>
          <p>The heatmap highlights regions that influenced the regression model. It indicates visual saliency rather than clinical causality.</p>
        </div>
      </section>

      <section id="history" style={{ marginTop: 36 }}>
        <h2>Analysis history</h2>
        <HistoryTable items={history} />
      </section>

      <section id="about" style={{ marginTop: 36 }}>
        <div className="panel">
          <h2>About the method</h2>
          <p>This prototype uses a lightweight PyTorch regression model designed for exploratory dental-age estimation from panoramic radiographs. The project includes preprocessing and explainability steps for educational and research use.</p>
        </div>
      </section>
    </div>
  );
}

export default App;
