# DentalAge AI dataset README

This repository does not ship a clinical dental radiograph training set by default. The project includes a documented research workflow so a dataset can be added legally and responsibly.

## Recommended dataset acquisition

Use a public dataset with:

- panoramic dental radiographs
- chronological age labels
- documented provenance
- clear research license
- de-identified patient metadata

## Example dataset checklist

- Source
- License
- Number of images
- Age range
- Population
- Image format
- Label format
- Split strategy
- Data cleaning and preprocessing steps

## Local setup timeline

```bash
python scripts/download_dataset.py
python scripts/prepare_dataset.py
```

## Research caution

Do not use private, copyrighted, or unauthorized medical radiographs. Always confirm you have permission and a valid license before training on external data.
