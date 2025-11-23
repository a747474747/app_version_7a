# Test Scenarios

This directory contains sample financial scenarios for testing the calculation engine functions.

## Available Scenarios

### `basic_income_tax.json`
- **Purpose**: Test basic personal income tax calculations (CAL-PIT-001 through CAL-PIT-005)
- **Features**: Salary income, basic deductions, Medicare levy, tax offsets
- **Expected Results**: Complete tax calculation workflow

### `superannuation_scenario.json`
- **Purpose**: Test superannuation contribution calculations (CAL-SUP-002, 003, 007, 009)
- **Features**: Multiple contribution types, concessional cap calculations, contributions tax
- **Expected Results**: Super contribution processing and taxation

### `capital_gains_scenario.json`
- **Purpose**: Test capital gains tax calculations (CAL-CGT-001, 002)
- **Features**: Asset disposal, capital gain calculation, CGT discount
- **Expected Results**: CGT assessment and discount application

### `comprehensive_scenario.json`
- **Purpose**: Test integrated financial scenario across multiple domains
- **Features**: Income tax, superannuation, and property investment calculations
- **Expected Results**: Complete financial position calculation

## Usage

These scenarios can be used to:

1. **Manual Testing**: Load the JSON data and run individual calculations
2. **Integration Testing**: Verify calculation chains work together
3. **Debug Dashboard**: Use as input for the dev dashboard testing
4. **Regression Testing**: Ensure calculations remain accurate after changes

## Data Structure

Each scenario follows the `CalculationState` schema:

- `global_context`: System-wide settings (dates, rates)
- `entities`: People and legal entities
- `asset_context`: Assets, liabilities, and ownership
- `cashflow_context`: Income, expenses, and contributions
- `expected_results`: Expected outputs for verification

## Running Tests

```python
# Load a scenario
import json
with open('backend/tests/test_scenarios/basic_income_tax.json', 'r') as f:
    scenario = json.load(f)

# Convert to CalculationState and run calculations
# (See calculation engine documentation for details)
```
