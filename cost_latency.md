# API Cost and Latency Analysis

## Project: Hostel Maintenance Ticket Sorter

### 1. Objective

This document explains the expected API usage, response time, and cost considerations for integrating an LLM into the Hostel Maintenance Ticket Sorter.

### 2. API Usage

The LLM is intended to classify student complaints and return structured JSON containing:

- Room number
- Issue category
- Urgency
- Complaint summary

Python performs the remaining validation and ticket-processing operations locally.

### 3. API Calls

The expected API usage is one classification request per complaint.

For 20 complaints:

Expected API calls = 20

If the system is run multiple times, API usage will increase accordingly unless previously classified results are reused.

### 4. Latency Measurement

Actual API latency must be measured after live API integration.

Record the following:

| Measurement | Result |
|---|---|
| Number of API requests | To be measured |
| Average response time | Pending |
| Minimum response time | Pending |
| Maximum response time | Pending |

Average latency can be calculated using:

Average Latency = Total API Response Time / Number of API Requests

### 5. Cost Estimation

Actual API cost depends on the selected model, input tokens, output tokens, and current pricing.

Estimated Cost = (Input Tokens × Input Token Price) + (Output Tokens × Output Token Price)

The applicable token prices must be checked from the official provider pricing page before calculating the final estimate.

### 6. Cost-Control Measures

- Keep the system prompt concise.
- Request only the required JSON fields.
- Avoid unnecessary repeated API requests.
- Reuse valid classification results when appropriate.
- Perform room validation and duplicate detection using Python.

### 7. Current Status

The project has been tested using local mock classification.

Live API cost and latency measurements are pending approved API integration.

### 8. Conclusion

The system is designed to minimize unnecessary API usage by using the LLM only for complaint classification and handling the remaining operations locally through Python.