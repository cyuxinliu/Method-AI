# Method.AI

**Chemist-in-the-loop system for translating retrosynthetic plans into draft, lab-ready experimental procedures adapted to lab constraints.**

> **DISCLAIMER**: This software generates *draft* procedures intended for review by qualified chemists. It does not guarantee safety, correctness, or regulatory compliance. Users are solely responsible for verifying all procedures before execution. See [SAFETY.md](docs/SAFETY.md) for details.

## Overview

Method.AI bridges the gap between computational retrosynthesis and practical laboratory execution. Given a target molecule (SMILES) and laboratory constraints, it produces structured procedural drafts with:

- Step-by-step protocol suggestions
- Risk flags based on equipment and experience level
- Fallback alternatives for common constraints
- Integration with IBM RXN for Chemistry (optional)

## Features

- **IBM RXN Integration**: Automatically fetch retrosynthesis plans via `rxn4chemistry`
- **Graceful Degradation**: Runs without external services using deterministic placeholders
- **Lab Context Awareness**: Adapts procedures based on available equipment, time, and experience
- **Risk Annotation**: Flags potential safety concerns based on constraints
- **Feedback Loop**: Capture chemist feedback for continuous improvement

## Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+ (for frontend, optional)
- Docker (optional)

### Installation

```bash
# Clone the repository
git clone https://github.com/your-org/method-ai.git
cd method-ai

# Set up Python environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -e .

# Copy environment template
cp .env.example .env
# Edit .env to add RXN_API_KEY if available
```

### Running Locally

```bash
# Start the backend
make dev

# Or manually:
cd backend && uvicorn app.main:app --reload --port 8000
```

The API will be available at `http://localhost:8000`. View the interactive docs at `http://localhost:8000/docs`.

### Running with Docker

```bash
docker-compose -f docker/docker-compose.yml up --build
```

### Running Tests

```bash
make test

# Or manually:
pytest backend/tests -v
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check |
| POST | `/v1/generate-procedure` | Generate a draft procedure |
| POST | `/v1/feedback` | Submit feedback on a procedure |

### Example Request

```bash
curl -X POST http://localhost:8000/v1/generate-procedure \
  -H "Content-Type: application/json" \
  -d '{
    "target_smiles": "CC(=O)Oc1ccccc1C(=O)O",
    "lab_context": {
      "scale_mg": 500,
      "equipment": ["rotovap", "heating_mantle", "reflux_condenser"],
      "purification_methods": ["recrystallization", "filtration"],
      "safety_constraints": ["no_open_flame"],
      "experience_level": "grad",
      "time_budget_hours": 8
    }
  }'
```

## Project Structure

```
method-ai/
├── backend/
│   ├── app/
│   │   ├── api/          # FastAPI routes
│   │   ├── core/         # Configuration, logging
│   │   ├── models/       # Pydantic schemas
│   │   ├── services/     # Business logic
│   │   └── utils/        # Utilities
│   └── tests/            # Unit tests
├── frontend/             # Next.js frontend (optional)
├── docker/               # Docker configuration
├── docs/                 # Documentation
├── examples/             # Example inputs/outputs
├── data/                 # Sample data
└── scripts/              # Development scripts
```

## Configuration

See [.env.example](.env.example) for available configuration options.

Key environment variables:

| Variable | Description | Required |
|----------|-------------|----------|
| `RXN_API_KEY` | IBM RXN for Chemistry API key | No |
| `RXN_PROJECT_ID` | IBM RXN project ID | No |
| `LOG_LEVEL` | Logging level (DEBUG, INFO, WARNING, ERROR) | No |

## Documentation

- [Architecture](docs/ARCHITECTURE.md) - System design and data flow
- [Safety Policy](docs/SAFETY.md) - Safety boundaries and disclaimers
- [RXN Integration](docs/RXN_INTEGRATION.md) - IBM RXN setup guide
- [Data Schema](docs/DATA_SCHEMA.md) - API schemas and data formats
- [Roadmap](docs/ROADMAP.md) - Future development plans

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

This project is licensed under the MIT License - see [LICENSE](LICENSE) for details.

## Security

For security concerns, see [SECURITY.md](SECURITY.md).
