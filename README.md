# Hostel Maintenance Ticket Sorter

An AI-assisted hostel maintenance complaint classification and ticket management system built using Python and the Google Gemini API.

## 1. Project Overview

The Hostel Maintenance Ticket Sorter automates the initial processing of student maintenance complaints.

It uses Google's Gemini API to classify complaints, extract room numbers, identify issue categories, determine urgency, and generate short summaries.

Python handles response validation, room verification, safety checks, duplicate detection, maintenance team assignment, due-date calculation, and report generation.

The system supports human-supervised maintenance management. All generated tickets require appropriate human review.

## 2. Project Objectives

- Automatically classify hostel maintenance complaints.
- Extract and validate room numbers.
- Identify urgent maintenance issues.
- Assign complaints to appropriate maintenance teams.
- Detect duplicate complaints and link them to existing tickets.
- Generate structured maintenance reports.
- Maintain human oversight of maintenance decisions.

## 3. Technologies Used

- Python 3
- Google Gemini API
- Google Gen AI Python SDK
- Python-dotenv
- CSV and JSON
- Regular expressions
- Python datetime module

## 4. System Architecture

The project follows a combination of AI-based classification and rule-based Python processing.

**Processing workflow:**

1. Read complaints from the CSV dataset.
2. Send each complaint to the Gemini API.
3. Receive structured JSON classification.
4. Validate the Gemini response.
5. Verify the room number.
6. Apply Python safety checks.
7. Detect duplicate complaints.
8. Assign the appropriate maintenance team.
9. Calculate ticket due dates.
10. Generate CSV reports and a processing summary.

### Issue Categories

- Electrical
- Plumbing
- Carpentry
- Cleaning
- Internet
- Other

### Maintenance Team Assignment

Complaints are routed to the appropriate maintenance team based on their issue category.

## 5. Project Files

| File | Description |
|---|---|
| complaints.csv | Student complaint dataset |
| open_tickets.csv | Existing maintenance tickets |
| system_prompt.txt | Gemini classification instructions |
| gemini_classifier.py | Gemini API integration and response validation |
| main_mock.py | Main complaint processing workflow |
| cp2_test_mock.py | Single-complaint mock workflow test |
| test_gemini_classifier.py | Classification validation tests |
| test_gemini.py | Gemini API connectivity test |
| test_real_gemini.py | Live Gemini classification test |
| list_models.py | Lists available Gemini models |
| results.csv | Complaint processing results |
| work_orders.csv | Generated maintenance work orders |
| needs_info.csv | Complaints requiring clarification |
| urgent_tickets.csv | Urgent maintenance tickets |
| summary.txt | Processing summary |
| evaluation_results.md | Testing and evaluation results |
| judgment_framework.md | Human decision-making framework |
| ai_decision_journal.md | AI development decision journal |
| cost_latency.md | Cost and latency planning |
| reflection.md | Project reflection |

## 6. Installation and Setup

### Prerequisites

- Python 3
- Internet connection
- Google Gemini API key

### Install dependencies

```bash
pip install google-genai python-dotenv
```

### Configure the API key

Create a `.env` file in the project directory:

```env
GEMINI_API_KEY=your_api_key_here
```

Never upload your `.env` file or expose your API key publicly.

The `.gitignore` file excludes the API key file from Git tracking.

## 7. How to Run

Run the following commands from the project directory.

### Test Gemini API connectivity

```bash
python3 test_gemini.py
```

### Test live complaint classification

```bash
python3 test_real_gemini.py
```

### Test response validation

```bash
python3 test_gemini_classifier.py
```

### Run the complete complaint processing workflow

```bash
python3 main_mock.py
```

The main program processes complaints and generates the output reports.

## 8. Error Handling and Validation

The Gemini integration includes:

- Structured JSON response generation.
- Validation of required response fields.
- Validation of issue categories and urgency types.
- Summary length validation.
- Empty response and invalid JSON handling.
- Automatic retries for temporary API failures.

The retry mechanism handles temporary server and rate-limit errors using increasing wait times.

Python remains responsible for ticket creation and maintenance routing.

## 9. Testing and Evaluation

The project was tested using a dataset of 20 maintenance complaints.

### Processing Results

| Metric | Result |
|---|---:|
| Total complaints | 20 |
| New tickets created | 12 |
| Duplicate complaints joined | 6 |
| Complaints needing information | 2 |
| Urgent tickets | 3 |
| Total tickets | 15 |

### Tests Performed

- Live Gemini API connectivity testing.
- Real complaint classification testing.
- JSON response validation.
- Invalid issue category testing.
- Invalid urgency type testing.
- Summary length validation.
- Duplicate complaint detection.
- Invalid room number testing.
- Red-team testing for misleading urgency.
- Full dataset processing.

## 10. Human Review and Safety

The system assists maintenance staff but does not replace human decision-making.

- Urgent tickets should receive prompt human attention.
- Maintenance teams must review assigned work orders.
- Complaints requiring clarification must be investigated.
- Tickets are not automatically closed by the AI.
- Human supervision is required for maintenance decisions.

The system is a project prototype and should not be treated as a production emergency-response system.

## 11. Future Improvements

- Develop a web interface for students and wardens.
- Add a maintenance staff dashboard.
- Integrate email or notification alerts.
- Improve duplicate detection.
- Track ticket completion and maintenance history.
- Evaluate classification accuracy using a larger labelled dataset.
- Measure API cost and response latency.

## 12. Conclusion

The Hostel Maintenance Ticket Sorter demonstrates how generative AI and Python automation can improve the initial organization of hostel maintenance complaints.

By combining Gemini-based classification, rule-based validation, duplicate detection, and human supervision, the project provides a structured approach to maintenance ticket management.

**The project demonstrates practical integration of an LLM API into a Python-based automation workflow.**