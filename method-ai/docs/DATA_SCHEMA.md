# Data Schema

## API Schemas

### Lab Context

Describes laboratory constraints and capabilities.

```typescript
{
  scale_mg: number;              // Target scale in milligrams
  equipment: string[];           // Available equipment
  purification_methods: string[];// Available purification methods
  safety_constraints: string[];  // Safety limitations
  experience_level: enum;        // undergrad | grad | postdoc | industry
  time_budget_hours: number;     // Available time
}
```

### Generate Procedure Request

```typescript
{
  target_smiles: string;         // Target molecule in SMILES format
  lab_context: LabContext;       // Laboratory constraints
  retrosynthesis_plan?: object;  // Optional pre-computed plan
  notes?: string;                // Additional context
}
```

### Generate Procedure Response

```typescript
{
  procedure: ProcedureStep[];    // Ordered procedure steps
  risk_flags: string[];          // Identified concerns
  fallback_options: string[];    // Alternative approaches
  citations: string[];           // References (if any)
  disclaimer: string;            // Safety disclaimer
  version: string;               // API version
  request_id: string;            // Unique request identifier
}
```

### Procedure Step

```typescript
{
  step_number: number;           // Step order (1-indexed)
  action: string;                // Action description
  parameters: object;            // Step parameters
  rationale?: string;            // Explanation (optional)
}
```

### Feedback Request

```typescript
{
  request_id: string;            // Original request ID
  edits: string;                 // Description of changes made
  outcome: enum;                 // success | failure | partial | unknown
  notes?: string;                // Additional feedback
}
```

### Feedback Response

```typescript
{
  stored: boolean;               // Confirmation of storage
}
```

## Internal Schemas

### Normalized Retrosynthesis Plan

```typescript
{
  source: string;                // "ibm_rxn" | "placeholder" | "user_provided"
  target_smiles: string;         // Target molecule
  steps: RetroStep[];            // Retrosynthesis steps
}
```

### Retrosynthesis Step

```typescript
{
  rxn_smiles: string;            // Reaction SMILES
  confidence: number;            // Confidence score (0-1)
  notes: string;                 // Additional notes
}
```

## Enumerations

### Experience Level

| Value | Description |
|-------|-------------|
| `undergrad` | Undergraduate student |
| `grad` | Graduate student |
| `postdoc` | Postdoctoral researcher |
| `industry` | Industry professional |

### Feedback Outcome

| Value | Description |
|-------|-------------|
| `success` | Procedure worked as expected |
| `failure` | Procedure did not work |
| `partial` | Partial success |
| `unknown` | Outcome not determined |

## Storage Formats

### Feedback JSONL

Each line contains a complete feedback record:

```json
{"timestamp": "2024-01-01T00:00:00Z", "request_id": "...", "edits": "...", "outcome": "success", "notes": "..."}
```
