# Implementation Quickstart: Four-Engine System Architecture

**Version**: 1.0
**Date**: November 21, 2025
**Audience**: Development Team

This guide provides a rapid path to understanding and implementing the Four-Engine System Architecture.

---

## 1. Architecture Overview (5 minutes)

### The Four Engines

```
┌─────────────────┐    ┌─────────────────┐
│   LLM           │    │  Calculation    │
│ Orchestrator    │    │  Engine         │
│                 │    │                 │
│ • Intent        │    │ • Tax/Super     │
│ • State Hyd.    │    │ • Projections   │
│ • Explanation   │    │ • Deterministic │
└─────────────────┘    └─────────────────┘
        ▲                       ▲
        │                       │
        └──────┬────────────────┘
               │
        ┌─────────────────┐    ┌─────────────────┐
        │   Strategy      │    │    Advice       │
        │   Engine        │    │    Engine       │
        │                 │    │                 │
        │ • Optimization  │    │ • Compliance    │
        │ • What-if       │    │ • BID Rules     │
        │ • Solver        │    │ • Safety        │
        └─────────────────┘    └─────────────────┘
```

### Key Principles

1. **Probabilistic Interface / Deterministic Core**: LLM handles language, Calculation Engine handles numbers
2. **Separation of Concerns**: Each engine has one job
3. **Constitution First**: All decisions guided by the constitution
4. **Spec-Driven Development**: Specs before code

---

## 2. Development Environment Setup (10 minutes)

### Prerequisites

```bash
# Required software
Python 3.11+
Node.js 18+
PostgreSQL 15+
Git

# Development tools
VS Code with Python/Pylance extensions
Docker Desktop (for local Postgres)
```

### Repository Setup

```bash
# Clone the repository
git clone <repository-url>
cd app-version-7

# Create feature branch
git checkout -b feature/001-four-engine-architecture

# Set up Python virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Set up Node.js environment
cd frontend/web
npm install
cd ../..

# Start local PostgreSQL (Docker)
docker run -d \
  --name postgres-dev \
  -e POSTGRES_DB=finance_dev \
  -e POSTGRES_USER=finance_user \
  -e POSTGRES_PASSWORD=finance_pass \
  -p 5432:5432 \
  postgres:15
```

### Environment Configuration

Create `.env` file in project root:

```env
# Database
DATABASE_URL=postgresql://finance_user:finance_pass@localhost:5432/finance_dev

# LLM Service
OPENAI_API_KEY=your-openai-key-here
OPENROUTER_API_KEY=your-openrouter-key-here

# Application
SECRET_KEY=your-secret-key-here
DEBUG=True
ENVIRONMENT=development

# External Services (for future use)
BANK_API_KEY=your-bank-api-key
REGULATORY_API_KEY=your-regulatory-api-key
```

---

## 3. Key Architecture Concepts (15 minutes)

### CalculationState: The Universal Input

Every calculation starts with a `CalculationState`:

```python
from pydantic import BaseModel

class CalculationState(BaseModel):
    """Complete financial snapshot."""

    # Global rules and assumptions
    global_context: GlobalContext

    # Who (people, entities)
    entity_context: EntityContext

    # What they own/owe
    position_context: FinancialPositionContext

    # Income, expenses, flows
    cashflow_context: CashflowContext

    # Working state (populated by CALs)
    intermediates: CalculatedIntermediariesContext
```

### ProjectionOutput: The Time Series Result

Calculations produce timelines:

```python
class ProjectionOutput(BaseModel):
    """Year-by-year financial projection."""

    base_state: CalculationState  # Year 0
    timeline: List[YearSnapshot]  # Years 1-N

class YearSnapshot(BaseModel):
    """Financial state at end of year."""

    year_index: int
    financial_year: int
    position_snapshot: FinancialPositionContext
    intermediaries: CalculatedIntermediariesContext
```

### TraceLog: The Explanation System

Every number has an explanation:

```python
class TraceEntry(BaseModel):
    """Audit trail for explainability."""

    calc_id: str           # "CAL-PIT-001"
    entity_id: str         # "person_001"
    year_index: int        # 0
    field: str             # "net_tax_payable"
    severity: str          # "info"
    explanation: str       # "Tax calculated using..."
    metadata: Dict[str, Any]
```

---

## 4. First Working Example (20 minutes)

### Step 1: Create a Simple Scenario

```python
# backend/engines/calc/examples/simple_tax_calc.py

from decimal import Decimal
from datetime import date
from engines.calc.state_models import (
    CalculationState, GlobalContext, EntityContext,
    Person, CashflowContext, EntityCashflow
)

def create_simple_scenario() -> CalculationState:
    """Create a basic tax calculation scenario."""

    # Global context (rules)
    global_context = GlobalContext(
        financial_year=2025,
        effective_date=date.today(),
        inflation_rate=Decimal("0.03"),
        wage_growth_rate=Decimal("0.04"),
        property_growth_rate=Decimal("0.05"),
        tax_brackets=[
            {"threshold": Decimal("0"), "rate": Decimal("0.0")},
            {"threshold": Decimal("18200"), "rate": Decimal("0.19")},
            {"threshold": Decimal("45000"), "rate": Decimal("0.325")},
            {"threshold": Decimal("135000"), "rate": Decimal("0.37")}
        ]
    )

    # Entity context (who)
    person = Person(
        id="person_001",
        date_of_birth=date(1980, 1, 1),
        residency_status="RESIDENT",
        work_status="FULL_TIME"
    )

    entity_context = EntityContext(
        people={"person_001": person}  # Dict, not List
    )

    # Cashflow context (income)
    entity_cashflow = EntityCashflow(
        entity_id="person_001",
        salary_wages_gross=Decimal("75000")
    )

    cashflow_context = CashflowContext(
        flows={"person_001": entity_cashflow}
    )

    return CalculationState(
        global_context=global_context,
        entity_context=entity_context,
        cashflow_context=cashflow_context
    )
```

### Step 2: Run a CAL

```python
# backend/engines/calc/cal_pit_001.py

def run_CAL_PIT_001(
    state: CalculationState,
    entity_id: str,
    year_index: int = 0
) -> CalculationResult:
    """
    Calculate PAYG tax for residents.
    CAL-PIT-001: Personal Income Tax
    """

    # Get entity cashflow
    cashflow = state.cashflow_context.flows[entity_id]

    # Calculate taxable income (simplified)
    assessable_income = cashflow.salary_wages_gross
    deductions = Decimal("0")  # Simplified
    taxable_income = assessable_income - deductions

    # Calculate tax using brackets
    tax = calculate_tax_from_brackets(
        taxable_income,
        state.global_context.tax_brackets
    )

    # Create trace entry
    trace_entry = TraceEntry(
        calc_id="CAL-PIT-001",
        entity_id=entity_id,
        year_index=year_index,
        field="net_tax_payable",
        severity="info",
        explanation=f"Tax calculated using resident marginal rates for {taxable_income} taxable income",
        metadata={
            "assessable_income": assessable_income,
            "deductions": deductions,
            "taxable_income": taxable_income,
            "tax_brackets_used": len(state.global_context.tax_brackets)
        }
    )

    # Update intermediates
    if entity_id not in state.intermediates.results:
        state.intermediates.results[entity_id] = EntityResults()

    state.intermediates.results[entity_id].tax.net_tax_payable = tax
    state.intermediates.trace_log.append(trace_entry)

    return CalculationResult(
        success=True,
        value=tax,
        trace_entries=[trace_entry]
    )
```

### Step 3: Test the Calculation

```python
# tests/golden/test_pit_basic.py

def test_basic_resident_tax():
    """Test CAL-PIT-001 with basic resident tax scenario."""

    # Create scenario
    scenario = create_simple_scenario()

    # Run calculation
    result = run_CAL_PIT_001(scenario, "person_001")

    # Assert results
    assert result.success == True
    assert result.value == Decimal("14247.00")  # Expected tax

    # Check trace
    assert len(result.trace_entries) == 1
    trace = result.trace_entries[0]
    assert trace.calc_id == "CAL-PIT-001"
    assert trace.explanation is not None
```

---

## 5. API Development Workflow (15 minutes)

### Starting a New Endpoint

```python
# backend/main.py

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from .database import get_db
from .auth import get_current_user

app = FastAPI(title="Frankie Finance API", version="1.0.0")

@app.post("/api/v1/scenarios")
async def create_scenario(
    request: CreateScenarioRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new financial scenario."""

    try:
        # Validate request
        if not request.name:
            raise HTTPException(400, "Scenario name is required")

        # Create scenario
        scenario = Scenario(
            name=request.name,
            description=request.description,
            owner_id=current_user.id,
            state_payload=request.calculation_state.json()
        )

        db.add(scenario)
        db.commit()

        return {"scenario_id": scenario.id}

    except Exception as e:
        db.rollback()
        raise HTTPException(500, f"Failed to create scenario: {str(e)}")
```

### Testing the API

```bash
# Start the server
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Test the endpoint
curl -X POST "http://localhost:8000/api/v1/scenarios" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "name": "My First Scenario",
    "description": "Testing the API",
    "calculation_state": {
      "global_context": {
        "financial_year": 2025,
        "effective_date": "2025-11-21"
      },
      "entity_context": {"persons": []},
      "cashflow_context": {"flows": {}},
      "position_context": {"assets": [], "liabilities": []}
    }
  }'
```

---

## 6. Testing Strategy (10 minutes)

### Golden Tests (ATO Parity)

```python
# tests/golden/test_ato_parity.py

def test_ato_tax_calculator_parity():
    """Test that our CAL-PIT-001 matches ATO calculator."""

    # Load ATO test case
    test_case = load_ato_test_case("TC001_basic_resident")

    # Create scenario
    scenario = create_scenario_from_ato_test_case(test_case)

    # Run calculation
    result = run_CAL_PIT_001(scenario, test_case.person_id)

    # Assert parity to cent
    assert result.value == test_case.expected_tax, \
        f"Expected ${test_case.expected_tax}, got ${result.value}"

    # Assert trace completeness
    assert len(result.trace_entries) > 0
    assert all(entry.explanation for entry in result.trace_entries)
```

### Unit Tests

```python
# tests/unit/test_calculation_engine.py

class TestCalculationEngine:

    def test_tax_calculation_edge_cases(self):
        """Test edge cases in tax calculations."""

        # Zero income
        scenario = create_scenario_with_income(Decimal("0"))
        result = run_CAL_PIT_001(scenario, "person_001")
        assert result.value == Decimal("0")

        # High income
        scenario = create_scenario_with_income(Decimal("200000"))
        result = run_CAL_PIT_001(scenario, "person_001")
        assert result.value > Decimal("50000")  # 37% bracket

    def test_trace_completeness(self):
        """Test that all calculations produce complete traces."""

        scenario = create_complete_scenario()
        result = run_CAL_PIT_001(scenario, "person_001")

        # Check trace structure
        for trace in result.trace_entries:
            assert trace.calc_id
            assert trace.entity_id
            assert trace.field
            assert trace.explanation
            assert isinstance(trace.metadata, dict)
```

### Integration Tests

```python
# tests/integration/test_full_workflow.py

def test_complete_scenario_workflow(client):
    """Test full scenario creation to results."""

    # Create scenario
    response = client.post("/api/v1/scenarios", json={
        "name": "Integration Test",
        "calculation_state": create_test_calculation_state()
    })
    assert response.status_code == 201
    scenario_id = response.json()["scenario_id"]

    # Run calculation
    response = client.post(f"/api/v1/scenarios/{scenario_id}/run")
    assert response.status_code == 200

    # Get results
    response = client.get(f"/api/v1/scenarios/{scenario_id}/results")
    assert response.status_code == 200

    results = response.json()
    assert "projection_output" in results
    assert len(results["projection_output"]["timeline"]) > 0
```

---

## 7. Deployment & Operations (10 minutes)

### Local Development

```bash
# Start all services
docker-compose up -d

# Run database migrations
alembic upgrade head

# Start backend
cd backend
uvicorn main:app --reload

# Start frontend (new terminal)
cd frontend/web
npm run dev
```

### Production Deployment

```bash
# Backend (Render)
# Environment variables set in Render dashboard
# Automatic deployments from main branch

# Frontend (Vercel)
# Connect GitHub repository
# Automatic deployments from main branch
# Environment variables for API URLs
```

### Health Checks

```bash
# API health
curl https://api.frankiefinance.com/health

# Database connectivity
curl https://api.frankiefinance.com/health/db

# LLM service availability
curl https://api.frankiefinance.com/health/llm
```

---

## 8. Next Steps & Resources

### Immediate Next Steps

1. **Run the example**: Execute the simple tax calculation
2. **Add a CAL**: Implement CAL-SUP-007 (Super tax)
3. **Create an API endpoint**: Expose tax calculation via REST
4. **Add tests**: Write golden tests for your CAL
5. **Update docs**: Document your new CAL following the pattern

### Key Resources

- **Constitution**: `design_docs/constitution.md` - Non-negotiable rules
- **Data Models**: `specs/001-four-engine-architecture/data-model.md` - Type definitions
- **API Contracts**: `specs/001-four-engine-architecture/contracts/` - Interface specs
- **Research Findings**: `specs/001-four-engine-architecture/research.md` - Technical decisions

### Getting Help

- **Specs First**: Update plan/spec before code changes
- **Test Early**: Golden tests prevent regressions
- **Trace Everything**: Every number needs explanation
- **Constitution Wins**: When in doubt, follow the constitution

---

**Time to Complete**: ~1 hour
**Result**: Working understanding of the four-engine architecture and ability to start implementation
