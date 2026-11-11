# Hostel Maintenance Ticket Sorter

## 1. Project Overview

The Hostel Maintenance Ticket Sorter is a Python-based project designed to classify student maintenance complaints and organize them into maintenance work orders.

The project demonstrates an LLM-based classification approach to identify the room number, issue category, urgency, and a short complaint summary.

Python handles validation, urgency checks, team assignment, duplicate detection, and due-date calculation.

**Note:** The current implementation uses a local mock classifier. Live Gemini API integration is planned for a future development stage.

## 2. Project Objectives

- Automatically classify hostel maintenance complaints.
- Identify urgent maintenance issues.
- Validate room numbers.
- Assign complaints to the appropriate maintenance team.
- Detect duplicate complaints and join existing tickets.
- Generate reports for maintenance staff.
- Keep the warden responsible for reviewing and closing tickets.

## 3. Technologies Used

- Python
- CSV files
- JSON
- Python datetime module
- Regular expressions
- Gemini API (planned for future live integration)

## 4. Project Files

| File | Description |
|---|---|
| complaints.csv | Student complaint dataset |
| open_tickets.csv | Existing maintenance tickets |
| system_prompt.txt | Instructions for the planned LLM classifier |
| gemini_classifier.py | Local mock classification logic |
| cp2_test_mock.py | Single-complaint mock workflow test |
| main_mock.py | Main mock processing program |
| test_gemini_classifier.py | Classification response validation tests |
| results.csv | Classification results |
| work_orders.csv | Maintenance work orders |
| needs_info.csv | Complaints requiring clarification |
| urgent_tickets.csv | Urgent maintenance tickets |
| summary.txt | Processing summary |
| evaluation_results.md | Testing and evaluation results |
| judgment_framework.md | Human decision-making framework |
| ai_decision_journal.md | AI development decision journal |
| cost_latency.md | Cost and latency planning |
| reflection.md | Project reflection |
| README.md | Project documentation |

## 5. How the System Works

1. Read student complaints from the CSV file.
2. Classify complaints into predefined issue categories.
3. Extract the room number and urgency.
4. Validate the extracted information.
5. Apply Python safety checks.
6. Assign the appropriate maintenance team.
7. Detect duplicate complaints.
8. Calculate the due date.
9. Generate output reports.

## 6. Human Review

The warden reviews all urgent tickets, assigns maintenance work, and decides when a ticket can be closed.

The system does not automatically close tickets.

Human supervision is important because maintenance decisions may affect student safety.

## 7. Testing and Evaluation

The project includes:

- Single-complaint mock workflow testing.
- Full dataset processing with 20 complaints.
- Duplicate detection testing.
- Red-team testing for misleading urgency and invalid room numbers.
- JSON response validation testing.
- Generation of five output files.

The evaluation results are documented in `evaluation_results.md`.

## 8. Current Development Status

- Local mock classifier implemented and tested.
- Single-complaint mock workflow tested successfully.
- Full dataset of 20 complaints processed successfully.
- Duplicate detection and red-team tests completed.
- JSON response validation tested successfully.
- Five output files generated.
- Live Gemini API integration is pending faculty-managed access and verification.

**Important:** The current classifier uses local Python logic and does not make external Gemini API calls. The current test results demonstrate mock processing and validation, not live LLM performance.

## 9. How to Run

Make sure Python 3 is installed and open the project directory in Terminal.

Run the single-complaint mock test:

```bash
python3 cp2_test_mock.py
```

Run the full mock-processing program:

```bash
python3 main_mock.py
```

Run the classifier validation tests:

```bash
python3 test_gemini_classifier.py
```

## 10. Future Improvements

- Complete approved live Gemini API integration.
- Improve classification accuracy using real LLM responses.
- Measure actual API response time and cost.
- Test duplicate detection through the complete processing pipeline.
- Develop a user-friendly interface for students and hostel wardens.

## 11. Conclusion

The Hostel Maintenance Ticket Sorter demonstrates how AI-assisted classification and Python automation can help organize hostel maintenance complaints.

The project combines automated processing with human supervision to support better complaint management, prioritization, and maintenance tracking.