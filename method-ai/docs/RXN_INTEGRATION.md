# IBM RXN Integration Guide

## Overview

Method.AI integrates with IBM RXN for Chemistry to obtain retrosynthesis plans. This integration is **optional** - the application functions without RXN credentials using deterministic placeholder logic.

## Getting an API Key

1. Visit [IBM RXN for Chemistry](https://rxn.res.ibm.com/)
2. Create an account or sign in
3. Navigate to your profile/settings
4. Generate or copy your API key

## Configuration

### Environment Variables

Add to your `.env` file:

```bash
# Required for RXN integration
RXN_API_KEY=your_api_key_here

# Optional: specify a project ID
RXN_PROJECT_ID=your_project_id
```

### Verification

Test your configuration:

```bash
# Start the server
make dev

# Check health (should show RXN status)
curl http://localhost:8000/health
```

## How It Works

### With RXN Credentials

1. Request received with target molecule
2. System calls IBM RXN API for retrosynthesis
3. Response normalized to internal schema
4. Procedure generated from plan

### Without RXN Credentials (Fallback)

1. Request received with target molecule
2. System uses deterministic placeholder plan
3. Procedure generated from placeholder
4. Response clearly marked as placeholder-based

## Internal Schema

RXN responses are normalized to:

```json
{
  "source": "ibm_rxn",
  "target_smiles": "...",
  "steps": [
    {
      "rxn_smiles": "...",
      "confidence": 0.95,
      "notes": ""
    }
  ]
}
```

For fallback mode:

```json
{
  "source": "placeholder",
  "target_smiles": "...",
  "steps": []
}
```

## Error Handling

The adapter handles:

- Network errors → fallback to placeholder
- Authentication errors → logged, fallback used
- Rate limiting → logged, fallback used
- Malformed responses → fallback used

All errors are logged for debugging.

## Usage Notes

- RXN API has rate limits; check IBM documentation
- Retrosynthesis calls may take several seconds
- Results are not cached by default
- All RXN-derived content is clearly attributed

## Troubleshooting

### "RXN not configured" in logs

API key not set. Check `.env` file.

### Authentication errors

Verify API key is correct and active.

### Timeout errors

RXN service may be slow; consider increasing timeout.

### Falling back to placeholder unexpectedly

Check logs for specific error messages.
