import React from 'react';

export type PredictionResult = {
  id: string;
  predicted_age: number;
  uncertainty: string | null;
  model_version: string;
  explanation_available: boolean;
  heatmap_url: string | null;
  created_at: string;
  status?: string;
};

export type HistoryItem = {
  id: string;
  predicted_age: number | null;
  uncertainty: string | null;
  model_version: string;
  created_at: string;
  status: string;
  original_filename: string | null;
};

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export async function analyzeImage(file: File): Promise<PredictionResult> {
  const formData = new FormData();
  formData.append('file', file);

  const response = await fetch(`${API_BASE}/api/v1/predict`, {
    method: 'POST',
    body: formData,
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'Unable to connect to the analysis server.' }));
    throw new Error(error.detail || 'Something went wrong while analyzing the image.');
  }

  return response.json();
}

export async function fetchHistory(): Promise<HistoryItem[]> {
  const response = await fetch(`${API_BASE}/api/v1/history`);
  if (!response.ok) {
    return [];
  }
  return response.json();
}
