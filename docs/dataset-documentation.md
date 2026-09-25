# Dataset documentation

## Recommended dataset pathway

A real production deployment should use a public, research-appropriate dental panoramic radiograph dataset with age labels. Suitable options include well-documented dental age estimation datasets from public research repositories or academic collaborations. The specific dataset should be reviewed for licensing, consent, and provenance before use.

## Example data acquisition plan

- Search for public dental panoramic radiograph datasets with age labels.
- Verify license and ethical usage terms.
- Confirm that the dataset includes anonymized or de-identified radiographs.
- Prefer image sets with known acquisition parameters, image format, and age annotations.

## Dataset placeholder fields

The repository is designed to work with a real dataset but does not bundle one by default. A production setup should include:

- Number of images: project-specific
- Age range: project-specific
- Population: project-specific
- Image format: PNG/JPG/DICOM depending on source
- Label format: chronological age (years) or CSV metadata
- Split methodology: train/validation/test with subject-level splitting to prevent leakage

## Limitations

- Public dental datasets may have acquisition variability.
- Model generalization depends on population and imaging protocol.
- Without subject-level split, leakage can distort evaluation metrics.
- A development fallback model is included for local testing but should not be treated as a real trained dental-age model.

## Preprocessing

- Validate file integrity.
- Resize to model-compatible dimensions.
- Convert to grayscale or RGB as appropriate.
- Normalize pixel intensity.
- Use training and inference preprocessing consistently.

## Split strategy

- Group by subject/patient when subject metadata is available.
- Ensure no same-person image appears in both training and test sets.
- Document the split in training logs and evaluation output.
