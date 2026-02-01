import { useState, FormEvent, ChangeEvent } from 'react';

interface LabContext {
  scale_mg: number;
  equipment: string[];
  purification_methods: string[];
  safety_constraints: string[];
  experience_level: string;
  time_budget_hours: number;
}

interface ProcedureStep {
  step_number: number;
  action: string;
  parameters: Record<string, unknown>;
  rationale?: string;
}

interface GenerateResponse {
  procedure: ProcedureStep[];
  risk_flags: string[];
  fallback_options: string[];
  disclaimer: string;
  version: string;
  request_id: string;
}

const EQUIPMENT_OPTIONS = [
  'rotovap',
  'heating_mantle',
  'magnetic_stirrer',
  'reflux_condenser',
  'balance',
  'ph_meter',
  'fume_hood',
];

const PURIFICATION_OPTIONS = [
  'recrystallization',
  'filtration',
  'column_chromatography',
  'distillation',
  'washing',
];

export default function Home() {
  const [targetSmiles, setTargetSmiles] = useState<string>('');
  const [scaleMg, setScaleMg] = useState<number>(500);
  const [experienceLevel, setExperienceLevel] = useState<string>('grad');
  const [timeBudget, setTimeBudget] = useState<number>(8);
  const [equipment, setEquipment] = useState<string[]>(['rotovap', 'heating_mantle']);
  const [purification, setPurification] = useState<string[]>(['recrystallization']);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<GenerateResponse | null>(null);

  const handleEquipmentChange = (item: string) => {
    setEquipment((prev) =>
      prev.includes(item) ? prev.filter((e) => e !== item) : [...prev, item]
    );
  };

  const handlePurificationChange = (item: string) => {
    setPurification((prev) =>
      prev.includes(item) ? prev.filter((e) => e !== item) : [...prev, item]
    );
  };

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setResult(null);

    const requestBody = {
      target_smiles: targetSmiles,
      lab_context: {
        scale_mg: scaleMg,
        equipment,
        purification_methods: purification,
        safety_constraints: [],
        experience_level: experienceLevel,
        time_budget_hours: timeBudget,
      } as LabContext,
    };

    try {
      const response = await fetch('/api/v1/generate-procedure', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestBody),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Failed to generate procedure');
      }

      const data: GenerateResponse = await response.json();
      setResult(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={styles.container}>
      <header style={styles.header}>
        <h1 style={styles.title}>Method.AI</h1>
        <p style={styles.subtitle}>
          Draft Procedure Generator for Laboratory Synthesis
        </p>
      </header>

      <div style={styles.disclaimer}>
        <strong>DISCLAIMER:</strong> This tool generates DRAFT procedures for
        review by qualified professionals. Generated content is not validated
        and may contain errors. Users must verify all steps before execution.
      </div>

      <form onSubmit={handleSubmit} style={styles.form}>
        <div style={styles.formGroup}>
          <label style={styles.label}>Target Molecule (SMILES)</label>
          <textarea
            value={targetSmiles}
            onChange={(e: ChangeEvent<HTMLTextAreaElement>) =>
              setTargetSmiles(e.target.value)
            }
            placeholder="e.g., CC(=O)OC1=CC=CC=C1C(=O)O"
            style={styles.textarea}
            required
          />
        </div>

        <div style={styles.row}>
          <div style={styles.formGroup}>
            <label style={styles.label}>Scale (mg)</label>
            <input
              type="number"
              value={scaleMg}
              onChange={(e: ChangeEvent<HTMLInputElement>) =>
                setScaleMg(Number(e.target.value))
              }
              min={1}
              style={styles.input}
              required
            />
          </div>

          <div style={styles.formGroup}>
            <label style={styles.label}>Time Budget (hours)</label>
            <input
              type="number"
              value={timeBudget}
              onChange={(e: ChangeEvent<HTMLInputElement>) =>
                setTimeBudget(Number(e.target.value))
              }
              min={1}
              style={styles.input}
              required
            />
          </div>

          <div style={styles.formGroup}>
            <label style={styles.label}>Experience Level</label>
            <select
              value={experienceLevel}
              onChange={(e: ChangeEvent<HTMLSelectElement>) =>
                setExperienceLevel(e.target.value)
              }
              style={styles.select}
            >
              <option value="undergrad">Undergraduate</option>
              <option value="grad">Graduate</option>
              <option value="postdoc">Postdoc</option>
              <option value="industry">Industry</option>
            </select>
          </div>
        </div>

        <div style={styles.formGroup}>
          <label style={styles.label}>Available Equipment</label>
          <div style={styles.checkboxGroup}>
            {EQUIPMENT_OPTIONS.map((item) => (
              <label key={item} style={styles.checkboxLabel}>
                <input
                  type="checkbox"
                  checked={equipment.includes(item)}
                  onChange={() => handleEquipmentChange(item)}
                />
                {item.replace(/_/g, ' ')}
              </label>
            ))}
          </div>
        </div>

        <div style={styles.formGroup}>
          <label style={styles.label}>Purification Methods</label>
          <div style={styles.checkboxGroup}>
            {PURIFICATION_OPTIONS.map((item) => (
              <label key={item} style={styles.checkboxLabel}>
                <input
                  type="checkbox"
                  checked={purification.includes(item)}
                  onChange={() => handlePurificationChange(item)}
                />
                {item.replace(/_/g, ' ')}
              </label>
            ))}
          </div>
        </div>

        <button type="submit" style={styles.button} disabled={loading}>
          {loading ? 'Generating...' : 'Generate Draft Procedure'}
        </button>
      </form>

      {error && <div style={styles.error}>{error}</div>}

      {result && (
        <div style={styles.result}>
          <h2 style={styles.resultTitle}>Generated Procedure</h2>

          <div style={styles.disclaimerResult}>{result.disclaimer}</div>

          <div style={styles.meta}>
            <span>Request ID: {result.request_id}</span>
            <span>Version: {result.version}</span>
          </div>

          <h3 style={styles.sectionTitle}>Procedure Steps</h3>
          <ol style={styles.stepsList}>
            {result.procedure.map((step) => (
              <li key={step.step_number} style={styles.step}>
                <strong>{step.action}</strong>
                {step.rationale && (
                  <p style={styles.rationale}>{step.rationale}</p>
                )}
                <pre style={styles.parameters}>
                  {JSON.stringify(step.parameters, null, 2)}
                </pre>
              </li>
            ))}
          </ol>

          {result.risk_flags.length > 0 && (
            <>
              <h3 style={styles.sectionTitle}>Risk Flags</h3>
              <ul style={styles.flagsList}>
                {result.risk_flags.map((flag, idx) => (
                  <li key={idx} style={styles.flag}>
                    {flag}
                  </li>
                ))}
              </ul>
            </>
          )}

          {result.fallback_options.length > 0 && (
            <>
              <h3 style={styles.sectionTitle}>Fallback Options</h3>
              <ul style={styles.fallbackList}>
                {result.fallback_options.map((option, idx) => (
                  <li key={idx}>{option}</li>
                ))}
              </ul>
            </>
          )}

          <h3 style={styles.sectionTitle}>Raw JSON</h3>
          <pre style={styles.json}>{JSON.stringify(result, null, 2)}</pre>
        </div>
      )}
    </div>
  );
}

const styles: Record<string, React.CSSProperties> = {
  container: {
    maxWidth: '900px',
    margin: '0 auto',
    padding: '20px',
    fontFamily: 'system-ui, -apple-system, sans-serif',
  },
  header: {
    textAlign: 'center',
    marginBottom: '30px',
  },
  title: {
    fontSize: '2.5rem',
    margin: '0',
    color: '#1a1a1a',
  },
  subtitle: {
    color: '#666',
    marginTop: '10px',
  },
  disclaimer: {
    backgroundColor: '#fff3cd',
    border: '1px solid #ffc107',
    borderRadius: '4px',
    padding: '15px',
    marginBottom: '30px',
    fontSize: '0.9rem',
  },
  form: {
    backgroundColor: '#f8f9fa',
    padding: '25px',
    borderRadius: '8px',
    marginBottom: '30px',
  },
  formGroup: {
    marginBottom: '20px',
  },
  label: {
    display: 'block',
    marginBottom: '8px',
    fontWeight: '600',
    color: '#333',
  },
  textarea: {
    width: '100%',
    minHeight: '80px',
    padding: '10px',
    border: '1px solid #ddd',
    borderRadius: '4px',
    fontSize: '1rem',
    fontFamily: 'monospace',
    boxSizing: 'border-box',
  },
  row: {
    display: 'flex',
    gap: '20px',
    flexWrap: 'wrap',
  },
  input: {
    width: '150px',
    padding: '10px',
    border: '1px solid #ddd',
    borderRadius: '4px',
    fontSize: '1rem',
  },
  select: {
    padding: '10px',
    border: '1px solid #ddd',
    borderRadius: '4px',
    fontSize: '1rem',
    minWidth: '150px',
  },
  checkboxGroup: {
    display: 'flex',
    flexWrap: 'wrap',
    gap: '15px',
  },
  checkboxLabel: {
    display: 'flex',
    alignItems: 'center',
    gap: '5px',
    cursor: 'pointer',
  },
  button: {
    backgroundColor: '#0066cc',
    color: 'white',
    padding: '12px 24px',
    border: 'none',
    borderRadius: '4px',
    fontSize: '1rem',
    cursor: 'pointer',
    width: '100%',
  },
  error: {
    backgroundColor: '#f8d7da',
    border: '1px solid #f5c6cb',
    color: '#721c24',
    padding: '15px',
    borderRadius: '4px',
    marginBottom: '20px',
  },
  result: {
    backgroundColor: '#fff',
    border: '1px solid #ddd',
    borderRadius: '8px',
    padding: '25px',
  },
  resultTitle: {
    marginTop: '0',
    color: '#1a1a1a',
  },
  disclaimerResult: {
    backgroundColor: '#e7f3ff',
    border: '1px solid #b6d4fe',
    borderRadius: '4px',
    padding: '15px',
    marginBottom: '20px',
    fontSize: '0.9rem',
  },
  meta: {
    display: 'flex',
    gap: '20px',
    color: '#666',
    fontSize: '0.9rem',
    marginBottom: '20px',
  },
  sectionTitle: {
    borderBottom: '1px solid #eee',
    paddingBottom: '10px',
    marginTop: '25px',
  },
  stepsList: {
    paddingLeft: '20px',
  },
  step: {
    marginBottom: '20px',
    paddingBottom: '15px',
    borderBottom: '1px solid #f0f0f0',
  },
  rationale: {
    color: '#666',
    fontStyle: 'italic',
    margin: '5px 0',
  },
  parameters: {
    backgroundColor: '#f8f9fa',
    padding: '10px',
    borderRadius: '4px',
    fontSize: '0.85rem',
    overflow: 'auto',
  },
  flagsList: {
    listStyle: 'none',
    padding: '0',
  },
  flag: {
    backgroundColor: '#fff3cd',
    padding: '10px',
    marginBottom: '5px',
    borderRadius: '4px',
    borderLeft: '4px solid #ffc107',
  },
  fallbackList: {
    paddingLeft: '20px',
  },
  json: {
    backgroundColor: '#1a1a1a',
    color: '#00ff00',
    padding: '15px',
    borderRadius: '4px',
    overflow: 'auto',
    fontSize: '0.85rem',
    maxHeight: '400px',
  },
};
