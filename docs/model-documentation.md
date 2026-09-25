# Model documentation

## Model choice

This project uses a compact PyTorch CNN regression model intended for dental image age estimation in a prototype setting. The architecture balances efficiency, ease of training, and compatibility with CPU-based inference.

## Regression target

The model predicts a continuous age value in years rather than a discrete age class.

## Training objective

- Loss: L1 (MAE) as the primary training objective
- Optimizer: Adam
- LR scheduler: ReduceLROnPlateau or step-based scheduler
- Checkpointing: best validation checkpoint saved

## Explainability

Grad-CAM is used to highlight regions that contributed most strongly to the prediction. This is intended for human interpretation and research review rather than proof of causal clinical relevance.

## Real-model deployment note

The shipped repository includes a development fallback model trained on a synthetic, non-clinical dataset. For production deployment, replace it with a model trained on a properly licensed clinical dataset and save the final weights to `ml/weights/best_model.pth`.
