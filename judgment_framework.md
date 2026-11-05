# Judgment Framework

## 1. Purpose

The Judgment Framework defines which decisions can be handled by the AI system and which decisions require human supervision.

The main objective is to improve complaint classification while maintaining safety, accuracy, and accountability.

## 2. AI Decision Rules

| Decision | AI/Python Responsibility |
|---|---|
| Room extraction | Extract the explicitly mentioned room number |
| Issue classification | Identify the maintenance issue |
| Urgency classification | Identify potential safety-related complaints |
| Summary generation | Generate a short complaint summary |
| Room validation | Check whether the room number follows the required format |
| Team assignment | Assign the complaint to the correct team |
| Duplicate detection | Identify existing tickets for the same room and issue |
| Due-date calculation | Calculate the expected completion deadline |

## 3. Urgency Rules

A complaint must be marked urgent when it describes a specified safety concern, including:

- Sparks from electrical equipment.
- Burning smell.
- Electric shock.
- Water near electrical fittings.
- Flooding.

Python safety checks must not downgrade an urgent classification made by the AI.

## 4. Room Validation Rules

A valid room number must follow the required format:

- Block: A, B, C, or D.
- Floor: 1, 2, 3, or 4.
- Room number: 01 to 20.

The room number must be explicitly mentioned in the complaint.

If the room number is missing or invalid, the complaint must be sent for additional information.

## 5. Human Review Responsibilities

The warden is responsible for:

1. Reviewing every urgent ticket.
2. Verifying complaint details when necessary.
3. Assigning maintenance work.
4. Monitoring ticket progress.
5. Confirming that maintenance work is completed.
6. Closing tickets manually.

## 6. Decisions That Must Not Be Automated

- Final confirmation that maintenance work is completed.
- Closing maintenance tickets.
- Ignoring or downgrading safety concerns.
- Guessing missing room numbers.
- Making unsupported assumptions about complaints.

## 7. Accountability

The AI system assists with classification and organization. The warden remains responsible for final operational decisions.

This human-in-the-loop approach helps prevent incorrect automated decisions and improves maintenance management.

## 8. Current Implementation Status

The current project uses a local mock classifier to simulate the planned AI classification process.

Python handles room validation, safety checks, team assignment, duplicate detection, due-date calculation, and report generation.

Live Gemini API integration is pending approved access and verification.

The warden remains responsible for reviewing urgent tickets, assigning maintenance work, and closing tickets. The system does not automatically close tickets.

## 9. Human-in-the-Loop Decision Flow

1. Student submits a maintenance complaint.
2. Classifier extracts the complaint details.
3. Python validates the room and applies safety rules.
4. Python checks for duplicate tickets and assigns the maintenance team.
5. Urgent tickets are highlighted for warden review.
6. The warden reviews, assigns, and monitors maintenance work.
7. The warden confirms completion and closes the ticket manually.