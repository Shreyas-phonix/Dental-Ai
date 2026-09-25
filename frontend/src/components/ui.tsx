import React, { useState } from 'react';

export function Navbar() {
  return (
    <nav className="navbar">
      <div className="brand-group">
        <div className="brand-mark">DA</div>
        <div>
          <div className="brand-name">DentalAge AI</div>
          <div className="brand-subtitle">Explainable age estimation</div>
        </div>
      </div>
      <div className="nav-links">
        <a href="#">Home</a>
        <a href="#analyze">Analyze</a>
        <a href="#history">History</a>
        <a href="#about">About</a>
      </div>
    </nav>
  );
}

export function UploadBox({ onFileSelected }: { onFileSelected: (file: File) => void }) {
  const [isDragging, setIsDragging] = useState(false);

  const handleFile = (file?: File) => {
    if (file) onFileSelected(file);
  };

  return (
    <div
      className={`upload-box ${isDragging ? 'dragging' : ''}`}
      onDragOver={(e) => {
        e.preventDefault();
        setIsDragging(true);
      }}
      onDragLeave={() => setIsDragging(false)}
      onDrop={(e) => {
        e.preventDefault();
        setIsDragging(false);
        const file = e.dataTransfer.files?.[0];
        handleFile(file);
      }}
    >
      <div className="upload-title">Upload dental X-ray</div>
      <div className="upload-subtitle">JPG, JPEG, or PNG</div>
      <label className="primary-button">
        Browse files
        <input
          type="file"
          accept="image/png,image/jpeg,image/jpg"
          onChange={(e) => handleFile(e.target.files?.[0])}
          hidden
        />
      </label>
    </div>
  );
}

export function XrayPreview({ src }: { src?: string }) {
  if (!src) {
    return <div className="preview-card empty">No image selected</div>;
  }

  return (
    <div className="preview-card">
      <img src={src} alt="Dental X-ray preview" className="preview-image" />
    </div>
  );
}

export function PredictionCard({ result }: { result?: any }) {
  if (!result) return <div className="panel">No prediction ready</div>;

  return (
    <div className="panel prediction-panel">
      <div className="metric-row">
        <span>Estimated dental age</span>
        <strong>{result.predicted_age.toFixed(1)} years</strong>
      </div>
      <div className="metric-row">
        <span>Model version</span>
        <strong>{result.model_version}</strong>
      </div>
      <div className="metric-row">
        <span>Uncertainty</span>
        <strong>{result.uncertainty || 'Not available for this model.'}</strong>
      </div>
      <div className="disclaimer-box">
        This application provides an AI-estimated dental age for research and educational purposes. It is not a definitive determination of chronological age.
      </div>
    </div>
  );
}

export function HeatmapViewer({ src }: { src?: string }) {
  if (!src) return <div className="panel">No heatmap available</div>;
  return (
    <div className="panel"><img src={src} alt="Grad-CAM heatmap" className="heatmap-image" /></div>
  );
}

export function HistoryTable({ items }: { items: any[] }) {
  if (!items.length) {
    return <div className="panel">No previous analyses found.</div>;
  }

  return (
    <div className="panel table-panel">
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Date</th>
            <th>Age</th>
            <th>Model</th>
          </tr>
        </thead>
        <tbody>
          {items.map((item) => (
            <tr key={item.id}>
              <td>{item.id.slice(0, 8)}</td>
              <td>{new Date(item.created_at).toLocaleDateString()}</td>
              <td>{item.predicted_age?.toFixed(1) || '—'} yrs</td>
              <td>{item.model_version}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
