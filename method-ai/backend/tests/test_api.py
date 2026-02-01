"""Tests for API endpoints."""

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client() -> TestClient:
    """Create a test client."""
    return TestClient(app)


@pytest.fixture
def sample_request_body() -> dict:
    """Create a sample request body."""
    return {
        "target_smiles": "CC(=O)OC1=CC=CC=C1C(=O)O",
        "lab_context": {
            "scale_mg": 500,
            "equipment": ["rotovap", "heating_mantle"],
            "purification_methods": ["recrystallization"],
            "safety_constraints": ["no_open_flame"],
            "experience_level": "grad",
            "time_budget_hours": 8,
        },
    }


class TestHealthEndpoint:
    """Tests for /health endpoint."""

    def test_health_returns_ok(self, client: TestClient):
        """Test health endpoint returns OK status."""
        response = client.get("/health")

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert "version" in data
        assert "rxn_configured" in data

    def test_health_includes_version(self, client: TestClient):
        """Test health endpoint includes version."""
        response = client.get("/health")

        data = response.json()
        assert data["version"] == "0.1.0"


class TestGenerateProcedureEndpoint:
    """Tests for /v1/generate-procedure endpoint."""

    def test_generate_procedure_success(
        self, client: TestClient, sample_request_body: dict
    ):
        """Test successful procedure generation."""
        response = client.post("/v1/generate-procedure", json=sample_request_body)

        assert response.status_code == 200
        data = response.json()

        assert "procedure" in data
        assert "risk_flags" in data
        assert "fallback_options" in data
        assert "disclaimer" in data
        assert "version" in data
        assert "request_id" in data

    def test_generate_procedure_returns_steps(
        self, client: TestClient, sample_request_body: dict
    ):
        """Test that procedure contains steps."""
        response = client.post("/v1/generate-procedure", json=sample_request_body)

        data = response.json()
        procedure = data["procedure"]

        assert len(procedure) >= 6
        assert len(procedure) <= 10

        for step in procedure:
            assert "step_number" in step
            assert "action" in step
            assert "parameters" in step

    def test_generate_procedure_includes_disclaimer(
        self, client: TestClient, sample_request_body: dict
    ):
        """Test that response includes safety disclaimer."""
        response = client.post("/v1/generate-procedure", json=sample_request_body)

        data = response.json()
        disclaimer = data["disclaimer"]

        assert "DRAFT" in disclaimer
        assert "qualified" in disclaimer.lower()
        assert "verify" in disclaimer.lower() or "verification" in disclaimer.lower()

    def test_generate_procedure_with_notes(
        self, client: TestClient, sample_request_body: dict
    ):
        """Test procedure generation with notes."""
        sample_request_body["notes"] = "This is a test note"
        response = client.post("/v1/generate-procedure", json=sample_request_body)

        assert response.status_code == 200

    def test_generate_procedure_with_plan(
        self, client: TestClient, sample_request_body: dict
    ):
        """Test procedure generation with provided plan."""
        sample_request_body["retrosynthesis_plan"] = {
            "source": "user_provided",
            "steps": [
                {
                    "rxn_smiles": "A>>B",
                    "confidence": 0.9,
                    "notes": "Test step",
                }
            ],
        }
        response = client.post("/v1/generate-procedure", json=sample_request_body)

        assert response.status_code == 200

    def test_generate_procedure_invalid_request(self, client: TestClient):
        """Test that invalid request returns 422."""
        response = client.post("/v1/generate-procedure", json={})

        assert response.status_code == 422

    def test_generate_procedure_missing_required_fields(self, client: TestClient):
        """Test that missing required fields returns 422."""
        response = client.post(
            "/v1/generate-procedure",
            json={"target_smiles": "CC"},
        )

        assert response.status_code == 422

    def test_generate_procedure_invalid_experience_level(
        self, client: TestClient, sample_request_body: dict
    ):
        """Test that invalid experience level returns 422."""
        sample_request_body["lab_context"]["experience_level"] = "invalid"
        response = client.post("/v1/generate-procedure", json=sample_request_body)

        assert response.status_code == 422


class TestFeedbackEndpoint:
    """Tests for /v1/feedback endpoint."""

    def test_feedback_success(self, client: TestClient):
        """Test successful feedback submission."""
        response = client.post(
            "/v1/feedback",
            json={
                "request_id": "test-request-001",
                "edits": "Changed temperature from 100C to 80C",
                "outcome": "success",
                "notes": "Worked well with modification",
            },
        )

        assert response.status_code == 200
        data = response.json()
        assert data["stored"] is True

    def test_feedback_minimal_request(self, client: TestClient):
        """Test feedback with minimal required fields."""
        response = client.post(
            "/v1/feedback",
            json={
                "request_id": "test-request-002",
                "edits": "Minor edits",
                "outcome": "partial",
            },
        )

        assert response.status_code == 200
        data = response.json()
        assert data["stored"] is True

    def test_feedback_all_outcomes(self, client: TestClient):
        """Test all valid outcome values."""
        outcomes = ["success", "failure", "partial", "unknown"]

        for outcome in outcomes:
            response = client.post(
                "/v1/feedback",
                json={
                    "request_id": f"test-{outcome}",
                    "edits": "Test edits",
                    "outcome": outcome,
                },
            )
            assert response.status_code == 200

    def test_feedback_invalid_outcome(self, client: TestClient):
        """Test that invalid outcome returns 422."""
        response = client.post(
            "/v1/feedback",
            json={
                "request_id": "test-invalid",
                "edits": "Test edits",
                "outcome": "invalid_outcome",
            },
        )

        assert response.status_code == 422

    def test_feedback_missing_required_fields(self, client: TestClient):
        """Test that missing required fields returns 422."""
        response = client.post(
            "/v1/feedback",
            json={"request_id": "test"},
        )

        assert response.status_code == 422
