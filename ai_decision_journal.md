# AI Decision Journal

## Project: Hostel Maintenance Ticket Sorter

### Entry 1: Project Planning

**Decision:** Develop a Python-based hostel maintenance complaint classification system.

**Reason:** Manual complaint sorting can take time and make it difficult to identify urgent issues.

**Approach:** Use an LLM for complaint classification and Python for validation and processing.

### Entry 2: Selecting the Classification Method

**Decision:** Use structured JSON output.

**Reason:** JSON makes it easier for Python to access the room, issue, urgency, and summary fields.

**Expected Output:**

```json
{
    "room": "A105",
    "issue": "electrical",
    "urgent": true,
    "summary": "Sparks coming from the switchboard"
}
```

### Entry 3: Room Validation

**Decision:** Implement room validation using Python regular expressions.

**Reason:** The system must not accept invalid or guessed room numbers.

**Expected Result:** Invalid or missing room numbers should be sent for additional information.

### Entry 4: Urgency Detection

**Decision:** Implement an additional Python safety check.

**Reason:** Safety-related complaints must not be missed during classification.

**Expected Result:** Python should preserve AI urgency and identify additional specified safety keywords.

### Entry 5: Team Assignment

**Decision:** Use a Python dictionary to map issue categories to maintenance teams.

**Reason:** This provides consistent team assignment.

### Entry 6: Duplicate Detection

**Decision:** Use room number and issue category as the duplicate identification key.

**Reason:** Multiple complaints about the same issue in the same room should be linked to an existing ticket.

### Entry 7: Mock Testing

**Test Complaint:** Sparks coming from the switchboard in A105.

**Mock Classification:**

- Room: A105
- Issue: electrical
- Urgent: True
- Summary: Sparks coming from the switchboard

**Observed Result:** JSON validation successful, room validation successful, and urgency detection successful.

**Testing Status:** One sample complaint successfully passed the local mock test. Full dataset testing remains to be completed.

### Entry 8: Human Supervision

**Decision:** Keep the warden responsible for reviewing urgent tickets, assigning work, and closing tickets.

**Reason:** The system should assist human decision-making rather than independently make final maintenance decisions.

## Conclusion

The project uses AI for complaint classification and Python for rule-based processing. Testing and evaluation will continue as the project develops.