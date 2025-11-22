#!/usr/bin/env python3

import sys
import os

# Add backend/src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend', 'src'))

try:
    from engines.calculation.registry import get_registered_calculations, run_calculation
    print('PASS: Registry import successful')

    registered = get_registered_calculations()
    print(f'PASS: Registered calculations: {len(registered)}')

    expected_ids = [
        'CAL-PIT-001', 'CAL-PIT-002', 'CAL-PIT-004', 'CAL-PIT-005',
        'CAL-CGT-001', 'CAL-CGT-002',
        'CAL-SUP-002', 'CAL-SUP-003', 'CAL-SUP-007', 'CAL-SUP-008', 'CAL-SUP-009',
        'CAL-PFL-104'
    ]

    print('Checking for expected CAL-IDs:')
    missing = []
    for cal_id in expected_ids:
        if cal_id in registered:
            print(f'  PASS: {cal_id}')
        else:
            print(f'  FAIL: {cal_id} - MISSING')
            missing.append(cal_id)

    if missing:
        print(f'\nFAIL: Missing CAL-IDs: {missing}')
        sys.exit(1)
    else:
        print('\nPASS: All expected CAL-IDs found!')

    # Test that we can access functions
    try:
        func = registered['CAL-PIT-001']
        print('PASS: Can access CAL-PIT-001 function from registry')
    except KeyError:
        print('FAIL: Cannot access CAL-PIT-001 function')
        sys.exit(1)

    print('\nSUCCESS: Registry validation PASSED!')

except ImportError as e:
    print(f'FAIL: Import error: {e}')
    sys.exit(1)
except Exception as e:
    print(f'FAIL: Unexpected error: {e}')
    sys.exit(1)
