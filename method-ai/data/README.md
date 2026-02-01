# Data Directory

This directory contains sample data and templates for Method.AI.

## Structure

```
data/
├── README.md           # This file
└── sample/
    └── tiny_procedures.jsonl  # Sample procedure records
```

## Sample Data

The `sample/` directory contains example data for development and testing. This data is synthetic and not intended for actual use.

## Local Data

A `local/` directory (gitignored) can be created for development data that should not be committed.

## Data Formats

### Procedure Records (JSONL)

Each line is a JSON object representing a procedure record:

```json
{"id": "...", "target": "...", "steps": [...], "metadata": {...}}
```

## Notes

- Do not commit sensitive or proprietary data
- Sample data is for demonstration only
- See [DATA_SCHEMA.md](../docs/DATA_SCHEMA.md) for schema details
