# Evaluation and Red-Team Results

## 1. Basic Classification Test

**Status:** PASSED

The mock classifier successfully extracted the room, issue, urgency, and summary from a sample complaint.

## 2. Red-Team Tests

| Test ID | Test Description | Expected Result | Actual Result | Status |
|---|---|---|---|---|
| R01 | Minor complaint with "URGENT!!!" | Urgency = False | Urgency = False | PASSED |
| R02 | Mistyped room number A1250 | Invalid room | Invalid room | PASSED |
| R03 | Same complaint submitted three times | One ticket with three complaints | One ticket with three complaints | PASSED |

## 3. Full Dataset Test

**Input:** 20 complaints from complaints.csv.

**Mock pipeline results:**
- Total complaints: 20
- New tickets: 12
- Duplicate complaints: 6
- Needs more information: 2
- Urgent tickets: 3

**Status:** PASSED — mock pipeline execution completed.

## 4. JSON Response Validation Tests

The following validation tests were executed using `test_gemini_classifier.py`.

| Test | Description | Expected Result | Actual Result | Status |
|---|---|---|---|---|
| T01 | Valid classification response | Accept response | Accepted | PASSED |
| T02 | Invalid issue category | Reject response | Invalid issue category detected | PASSED |
| T03 | Invalid urgency data type | Reject response | Invalid urgency type detected | PASSED |
| T04 | Summary exceeds 10 words | Reject response | Length validation error detected | PASSED |

All four JSON response validation tests passed.

## 5. Limitations

- These tests use a local mock classifier, not a live LLM.
- R03 tests the duplicate-grouping dictionary logic in isolation, not the complete CSV-processing pipeline.
- Live LLM integration and end-to-end duplicate testing remain to be completed.

## 4. Limitations

- These tests use a local mock classifier, not a live LLM.
- R03 tests the duplicate-grouping dictionary logic in isolation, not the complete CSV-processing pipeline.
- Live LLM integration and end-to-end duplicate testing remain to be completed.
