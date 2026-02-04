# Tests Directory

## Overview

This directory contains test files following **Test-Driven Development (TDD)** principles.

## TDD Approach

- Tests are written **before** implementation
- Tests should **fail initially** (defining the "empty slot" the AI must fill)
- Tests define the contract that implementation must satisfy

## Test Files

### Current Tests

- `test_mcp_connection.py`: ✅ **Available** - Verifies Tenx MCP Sense configuration and connection setup
  - Tests MCP config file existence and validity
  - Verifies tenxfeedbackanalytics server configuration
  - Checks required headers (X-Device, X-Coding-Tool)
  - Validates MCP connection log exists

### Planned Tests (Task 3.1)

- `test_trend_fetcher.py`: Asserts trend data structure matches API contract
- `test_skills_interface.py`: Asserts skills accept correct parameters
- `test_content_generator.py`: Validates content generation outputs
- `test_judge_confidence.py`: Tests confidence scoring logic

## Status

🚧 **Placeholder** - Tests will be written in Task 3.1

## Running Tests

```bash
# Once implemented
make test
# or
pytest tests/
```

