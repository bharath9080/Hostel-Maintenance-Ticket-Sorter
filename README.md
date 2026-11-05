# Hostel Maintenance Ticket Sorter

## 1. Project Overview

The Hostel Maintenance Ticket Sorter is a Python-based project designed to classify student maintenance complaints and organize them into maintenance work orders.

The system uses an LLM-based classification approach to identify the room number, issue category, urgency, and a short complaint summary.

Python handles validation, urgency checks, team assignment, duplicate detection, and due-date calculation.

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
- Gemini API (planned for live integration)
- JSON
- Python datetime module
- Regular expressions

## 4. Project Files

| File | Description |
|---|---|
| complaints.csv | Student complaint dataset |
| open_tickets.csv | Existing maintenance tickets |
| system_prompt.txt | Instructions for the LLM |
| cp2_test_mock.py | Mock classification test |
| main_mock.py | Main mock processing program |
| results.csv | Classification results |
| work_orders.csv | Maintenance work orders |
| needs_info.csv | Complaints requiring clarification |
| urgent_tickets.csv | Urgent maintenance tickets |
| summary.txt | Processing summary |
| .env | API configuration |
| .gitignore | Files excluded from Git |

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

## 7. Current Development Status

- Local mock classifier implemented and tested.
- Single-complaint mock workflow tested successfully.
- Full dataset of 20 complaints processed successfully.
- Duplicate detection and red-team tests completed.
- JSON response validation tested successfully.
- Five output files generated.
- Live Gemini API integration is pending faculty-managed access and verification.

The current classifier uses local Python logic and does not make external Gemini API calls.

## 8. How to Run

Run the mock test using:

```bash
python3 cp2_test_mock.py
```

Run the full mock-processing program using:

```bash
python3 main_mock.py
```

**Note:** Live Gemini API integration is a separate development step and requires approved access.