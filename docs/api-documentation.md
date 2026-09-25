# API documentation

## Health

- GET `/api/v1/health`

Returns service health and model availability.

## Prediction

- POST `/api/v1/predict`

Form-data fields:

- `file`: image file

Response fields:

- `id`
- `predicted_age`
- `uncertainty`
- `model_version`
- `explanation_available`
- `heatmap_url`
- `created_at`

## History

- GET `/api/v1/history`
- GET `/api/v1/history/{id}`
- GET `/api/v1/result/{id}`
- DELETE `/api/v1/history/{id}`

## Error handling

The API returns structured validation messages for:

- oversized files
- unsupported image types
- invalid/corrupted images
- missing files
- unavailable model
