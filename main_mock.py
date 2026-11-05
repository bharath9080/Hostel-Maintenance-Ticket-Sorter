
import csv
import re
from gemini_classifier import classify_with_gemini
from datetime import datetime, timedelta
from pathlib import Path

# ==========================================
# HOSTEL MAINTENANCE TICKET SORTER
# COMPLETE MOCK PROCESSING PROGRAM
# ==========================================

BASE_DIR = Path(__file__).resolve().parent

COMPLAINTS_FILE = BASE_DIR / "complaints.csv"
OPEN_TICKETS_FILE = BASE_DIR / "open_tickets.csv"

TEAM_MAPPING = {
    "electrical": "Electrical Maintenance Team",
    "plumbing": "Plumbing Maintenance Team",
    "carpentry": "Carpentry Maintenance Team",
    "cleaning": "Housekeeping Team",
    "internet": "IT Support Team",
    "other": "General Maintenance Team"
}


# ==========================================
# 1. CLASSIFY COMPLAINT
# ==========================================

def classify(complaint):

    text = complaint.lower()

    # Water near electrical fittings
    if "water" in text and (
        "electrical fitting" in text
        or "electrical fittings" in text
        or "near the switch" in text
    ):
        issue = "electrical"

    elif any(word in text for word in [
        "spark", "switchboard", "electric shock",
        "electrical", "burning smell", "fan"
    ]):
        issue = "electrical"

    # Plumbing complaints
    elif any(word in text for word in [
        "leaking", "leak", "tap", "pipe",
        "bathroom", "water"
    ]):
        issue = "plumbing"

    # Internet complaints
    elif any(word in text for word in [
        "wifi", "wi-fi", "internet", "network"
    ]):
        issue = "internet"

    # Cleaning complaints
    elif any(word in text for word in [
        "cleaning", "dirty", "housekeeping", "clean"
    ]):
        issue = "cleaning"

    # Carpentry complaints
    elif any(word in text for word in [
        "door", "lock", "handle", "window",
        "glass", "wood"
    ]):
        issue = "carpentry"

    else:
        issue = "other"

    # Extract explicitly mentioned room number
    room_match = re.search(
        r"(?<![A-Za-z0-9])([A-Za-z]-?\d{3})(?!\d)",
        complaint
    )

    room = room_match.group(1) if room_match else None

    urgent = apply_safety_net(complaint, False)

    summary = " ".join(complaint.split()[:10])

    return {
        "room": room,
        "issue": issue,
        "urgent": urgent,
        "summary": summary
    }


# ==========================================
# 2. ROOM VALIDATION
# ==========================================

def check_room(room, complaint):

    if room is None:
        return False

    pattern = r"^[A-D][1-4](0[1-9]|1[0-9]|20)$"

    if not re.fullmatch(pattern, room):
        return False

    if room not in complaint:
        return False

    return True


# ==========================================
# 3. CLASSIFICATION VALIDATION
# ==========================================

def is_valid(result, complaint):

    required_fields = {
        "room", "issue", "urgent", "summary"
    }

    if set(result.keys()) != required_fields:
        return False

    if result["issue"] not in TEAM_MAPPING:
        return False

    if not isinstance(result["urgent"], bool):
        return False

    if len(result["summary"].split()) > 10:
        return False

    return True


# ==========================================
# 4. PYTHON SAFETY NET
# ==========================================

def apply_safety_net(complaint, ai_urgent):

    text = complaint.lower()

    safety_words = [
        "spark",
        "burning smell",
        "electric shock",
        "shock from",
        "flooding",
        "overflowing"
    ]

    water_near_fittings = (
        "water" in text
        and (
            "electrical fitting" in text
            or "electrical fittings" in text
            or "near the switch" in text
            or "near switch" in text
        )
    )

    safety_detected = (
        any(word in text for word in safety_words)
        or water_near_fittings
    )

    # Python must never downgrade AI urgency
    return ai_urgent or safety_detected


# ==========================================
# 5. MAINTENANCE TEAM ASSIGNMENT
# ==========================================

def assign(issue):

    return TEAM_MAPPING.get(
        issue,
        "General Maintenance Team"
    )


# ==========================================
# 6. DUE DATE CALCULATION
# ==========================================

def due_date(opened_date, urgent):

    date_object = datetime.strptime(
        opened_date, "%Y-%m-%d"
    ).date()

    if urgent:
        deadline = date_object
    else:
        deadline = date_object + timedelta(days=2)

    return deadline.strftime("%Y-%m-%d")


# ==========================================
# 7. LOAD EXISTING TICKETS
# ==========================================

def load_open_tickets():

    tickets = {}

    try:
        with open(
            OPEN_TICKETS_FILE,
            "r",
            newline="",
            encoding="utf-8"
        ) as file:

            reader = csv.DictReader(file)

            for row in reader:

                room = row["room"]
                issue = row["issue"].lower()

                key = (room, issue)

                tickets[key] = {
                    "ticket": row["ticket"],
                    "room": room,
                    "issue": issue,
                    "team": assign(issue),
                    "opened": row["opened"],
                    "urgent": False,
                    "complaint_ids": [],
                    "status": "Open"
                }

    except FileNotFoundError:
        print("Warning: open_tickets.csv not found.")

    return tickets


# ==========================================
# 8. GENERATE UNIQUE TICKET NUMBER
# ==========================================

def next_ticket_number(tickets):

    numbers = []

    for ticket in tickets.values():

        match = re.fullmatch(
            r"T(\d+)",
            ticket["ticket"]
        )

        if match:
            numbers.append(int(match.group(1)))

    next_number = max(numbers, default=0) + 1

    return f"T{next_number:03d}"


# ==========================================
# 9. PROCESS ALL COMPLAINTS
# ==========================================

def process_complaints():

    tickets = load_open_tickets()

    results = []
    needs_info = []

    new_count = 0
    duplicate_count = 0

    try:
        with open(
            COMPLAINTS_FILE,
            "r",
            newline="",
            encoding="utf-8"
        ) as file:

            reader = csv.DictReader(file)
            complaints = list(reader)

    except FileNotFoundError:
        print("ERROR: complaints.csv not found!")
        return None

    for row in complaints:

        complaint_id = row["id"]
        complaint_date = row["date"]
        complaint = row["complaint"]

        result = classify_with_gemini(complaint)

        if not is_valid(result, complaint):
            print("Invalid classification:", complaint_id)
            continue

        room = result["room"]
        issue = result["issue"]

        final_urgent = apply_safety_net(
            complaint,
            result["urgent"]
        )

        result["urgent"] = final_urgent

        # Handle missing or invalid room numbers
        if not check_room(room, complaint):

            needs_info.append({
                "complaint_id": complaint_id,
                "date": complaint_date,
                "complaint": complaint,
                "room": room or "",
                "reason": "Missing or invalid room number"
            })

            results.append({
                "complaint_id": complaint_id,
                "room": room or "",
                "issue": issue,
                "urgent": final_urgent,
                "summary": result["summary"],
                "ticket": "",
                "status": "Needs information"
            })

            continue

        key = (room, issue)

        # Check for duplicate complaints
        if key in tickets:

            ticket = tickets[key]

            ticket["complaint_ids"].append(
                complaint_id
            )

            ticket["urgent"] = (
                ticket["urgent"] or final_urgent
            )

            duplicate_count += 1

            status = "Joined existing ticket"

        else:

            ticket_id = next_ticket_number(tickets)

            tickets[key] = {
                "ticket": ticket_id,
                "room": room,
                "issue": issue,
                "team": assign(issue),
                "opened": complaint_date,
                "urgent": final_urgent,
                "complaint_ids": [complaint_id],
                "status": "Open"
            }

            new_count += 1

            ticket = tickets[key]

            status = "New ticket created"

        results.append({
            "complaint_id": complaint_id,
            "room": room,
            "issue": issue,
            "urgent": final_urgent,
            "summary": result["summary"],
            "ticket": ticket["ticket"],
            "status": status
        })

    # Collect all urgent tickets
    urgent_tickets = [
        ticket for ticket in tickets.values()
        if ticket["urgent"]
    ]

    urgent_count = len(urgent_tickets)

    # Generate reports
    write_reports(
        tickets,
        results,
        needs_info,
        urgent_tickets,
        new_count,
        duplicate_count,
        urgent_count
    )

    return {
        "total": len(complaints),
        "new": new_count,
        "duplicates": duplicate_count,
        "needs_info": len(needs_info),
        "urgent": urgent_count
    }


# ==========================================
# 10. GENERATE REPORT FILES
# ==========================================

def write_reports(
    tickets,
    results,
    needs_info,
    urgent_tickets,
    new_count,
    duplicate_count,
    urgent_count
):

    # Work orders report
    with open(
        BASE_DIR / "work_orders.csv",
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        fields = [
            "ticket", "room", "issue", "team",
            "opened", "due_date", "urgent",
            "complaint_ids", "complaint_count", "status"
        ]

        writer = csv.DictWriter(
            file,
            fieldnames=fields
        )

        writer.writeheader()

        for ticket in tickets.values():

            deadline = due_date(
                ticket["opened"],
                ticket["urgent"]
            )

            writer.writerow({
                "ticket": ticket["ticket"],
                "room": ticket["room"],
                "issue": ticket["issue"],
                "team": ticket["team"],
                "opened": ticket["opened"],
                "due_date": deadline,
                "urgent": ticket["urgent"],
                "complaint_ids": ";".join(
                    ticket["complaint_ids"]
                ),
                "complaint_count": len(
                    ticket["complaint_ids"]
                ),
                "status": ticket["status"]
            })

    # Complaints needing more information
    with open(
        BASE_DIR / "needs_info.csv",
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        fields = [
            "complaint_id", "date", "complaint",
            "room", "reason"
        ]

        writer = csv.DictWriter(
            file,
            fieldnames=fields
        )

        writer.writeheader()
        writer.writerows(needs_info)

    # Urgent tickets report
    with open(
        BASE_DIR / "urgent_tickets.csv",
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        fields = [
            "ticket", "room", "issue", "team",
            "opened", "due_date", "complaint_ids"
        ]

        writer = csv.DictWriter(
            file,
            fieldnames=fields
        )

        writer.writeheader()

        for ticket in urgent_tickets:

            writer.writerow({
                "ticket": ticket["ticket"],
                "room": ticket["room"],
                "issue": ticket["issue"],
                "team": ticket["team"],
                "opened": ticket["opened"],
                "due_date": due_date(
                    ticket["opened"],
                    True
                ),
                "complaint_ids": ";".join(
                    ticket["complaint_ids"]
                )
            })

    # Classification results
    with open(
        BASE_DIR / "results.csv",
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        fields = [
            "complaint_id", "room", "issue",
            "urgent", "summary", "ticket", "status"
        ]

        writer = csv.DictWriter(
            file,
            fieldnames=fields
        )

        writer.writeheader()
        writer.writerows(results)

    # Summary report
    with open(
        BASE_DIR / "summary.txt",
        "w",
        encoding="utf-8"
    ) as file:

        file.write(
            "HOSTEL MAINTENANCE SORTER SUMMARY\n"
        )

        file.write("=================================\n\n")

        file.write(
            f"Total complaints: {len(results)}\n"
        )

        file.write(
            f"New tickets created: {new_count}\n"
        )

        file.write(
            f"Duplicate complaints joined: {duplicate_count}\n"
        )

        file.write(
            f"Complaints needing information: {len(needs_info)}\n"
        )

        file.write(
            f"Urgent tickets: {urgent_count}\n"
        )

        file.write(
            f"Total tickets: {len(tickets)}\n"
        )

        file.write(
            "\nAll tickets require appropriate human review.\n"
        )
        print("\n========== RED-TEAM TEST R02 ==========")

test_complaint = "Room A1250 has a broken fan"

test_result = classify(test_complaint)

room = test_result["room"]

room_valid = check_room(room, test_complaint)

print("Complaint:", test_complaint)
print("Extracted Room:", room)
print("Room Valid:", room_valid)
print("Expected: Invalid room")
print("Actual:", "Valid" if room_valid else "Invalid")

print("\n========== RED-TEAM TEST R03 ==========")

test_complaint = "Room A115 fan making noise"

test_tickets = {}

for i in range(1, 4):

    complaint_id = f"R03-{i}"

    result = classify(test_complaint)

    room = result["room"]
    issue = result["issue"]

    key = (room, issue)

    if key in test_tickets:

        test_tickets[key]["complaint_ids"].append(
            complaint_id
        )

        print(complaint_id, "joined existing ticket:",
              test_tickets[key]["ticket"])

    else:

        test_tickets[key] = {
            "ticket": "T001",
            "complaint_ids": [complaint_id]
        }

        print(complaint_id, "created ticket: T001")

print("\nTotal Tickets Created:", len(test_tickets))
print("Total Complaints Linked:",
      len(test_tickets[("A115", "electrical")]["complaint_ids"]))

print("Expected Tickets: 1")
print("Expected Complaints: 3")

# ==========================================
# 11. MAIN PROGRAM
# ==========================================

if __name__ == "__main__":

    print("\n========================================")
    print(" HOSTEL MAINTENANCE TICKET SORTER")
    print(" FULL MOCK PROCESSING")
    print("========================================")

    report = process_complaints()

    if report is not None:

        print("\nPROCESSING COMPLETED SUCCESSFULLY!")

        print("\nTotal complaints:",
              report["total"])

        print("New tickets:",
              report["new"])

        print("Duplicate complaints:",
              report["duplicates"])

        print("Needs more information:",
              report["needs_info"])

        print("Urgent tickets:",
              report["urgent"])

        print("\nFour reports generated:")
        print("1. work_orders.csv")
        print("2. needs_info.csv")
        print("3. urgent_tickets.csv")
        print("4. summary.txt")

        print("\nClassification results saved in results.csv")

    else:
        print("\nProcessing failed. Check your CSV files.")
