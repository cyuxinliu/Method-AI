# Architecture

## Overview

Method.AI follows a modular service-oriented architecture designed for extensibility and graceful degradation.

## System Components

```
┌─────────────────────────────────────────────────────────────────┐
│                          Frontend                                │
│                     (Next.js - Optional)                         │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                         FastAPI Backend                          │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                      API Layer                             │  │
│  │                    (routes.py)                             │  │
│  └───────────────────────────────────────────────────────────┘  │
│                                │                                 │
│  ┌─────────────┬───────────────┼───────────────┬─────────────┐  │
│  │             │               │               │             │  │
│  ▼             ▼               ▼               ▼             ▼  │
│ ┌───────┐ ┌─────────┐ ┌──────────────┐ ┌──────────┐ ┌───────┐  │
│ │Retro- │ │Procedure│ │    Risk      │ │ Feedback │ │Config │  │
│ │synth  │ │Generator│ │  Annotator   │ │  Store   │ │       │  │
│ │Adapter│ │         │ │              │ │          │ │       │  │
│ └───────┘ └─────────┘ └──────────────┘ └──────────┘ └───────┘  │
└─────────────────────────────────────────────────────────────────┘
       │
       ▼
┌─────────────────┐
│   IBM RXN API   │
│   (Optional)    │
└─────────────────┘
```

## Data Flow

### Generate Procedure Request

1. **Request Reception**: API receives target molecule (SMILES) and lab context
2. **Retrosynthesis Planning**:
   - If plan provided in request → use directly
   - Else if RXN API key configured → fetch from IBM RXN
   - Else → use deterministic placeholder
3. **Plan Normalization**: Convert to internal schema
4. **Procedure Generation**: Create step-by-step draft
5. **Risk Annotation**: Add flags based on lab constraints
6. **Response**: Return structured procedure with metadata

### Feedback Flow

1. User submits feedback with request_id
2. Feedback stored to local JSONL file
3. Acknowledgment returned

## Service Descriptions

### Retrosynthesis Adapter

Handles integration with IBM RXN for Chemistry:
- Manages API authentication
- Normalizes external responses to internal format
- Provides fallback when service unavailable

### Procedure Generator

Core logic for generating draft procedures:
- Template-based step generation
- Context-aware adjustments
- Deterministic behavior for reproducibility

### Risk Annotator

Analyzes lab context for potential concerns:
- Equipment constraints
- Experience level considerations
- Time budget limitations

### Feedback Store

Simple persistence layer:
- Appends feedback to JSONL file
- File locking for concurrent access
- Future: database integration

## Design Principles

1. **Graceful Degradation**: System functions without external services
2. **Deterministic Defaults**: Reproducible behavior without randomness
3. **Safety First**: Disclaimers and generic content by default
4. **Extensibility**: Service interfaces allow easy replacement
5. **Testability**: All components mockable and testable offline
