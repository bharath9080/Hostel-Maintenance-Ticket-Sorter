
import json
import re
import csv
from datetime import datetime, timedelta


# ==========================================
# 1. STUDENT COMPLAINT
# ==========================================

complaint = "Sparks coming from the switchboard in A105."


# ==========================================
# 2. SIMULATED LLM RESPONSE
# ==========================================

# This is a simulated response for local testing.
# It is NOT a live Gemini API response.

result = {
    "room": "A105",
    "issue": "electrical",
    "urgent": True,
    "summary": "Sparks coming from the switchboard"
}


# ==========================================
# 3. DISPLAY AND VALIDATE JSON
# ==========================================

print("\n========== HOSTEL MAINTENANCE SORTER ==========")

print("\nStudent Complaint:")
print(complaint)

print("\nClassification Result:")
print(json.dumps(result, indent=4))

required_fields = {"room", "issue", "urgent", "summary"}

if set(result.keys()) != required_fields:
    raise ValueError("Invalid JSON fields!")

if result["issue"] not in [
    "electrical", "plumbing", "carpentry",
    "cleaning", "internet", "other"
]:
    raise ValueError("Invalid issue category!")

if not isinstance(result["urgent"], bool):
    raise ValueError("Urgency must be True or False!")

if len(result["summary"].split()) > 10:
    raise ValueError("Summary exceeds 10 words!")

print("\nJSON validation successful!")


# ==========================================
# 4. ROOM VALIDATION
# ==========================================

def check_room(room, complaint):

    if room is None:
        return False

    pattern = r"^[A-D][1-4](0[1-9]|1[0-9]|20)$"

    if not re.fullmatch(pattern, room):
        return False

    if room.lower() not in complaint.lower():
        return False

    return True


room = result["room"]

if check_room(room, complaint):
    print("Room validation successful!")
else:
    print("Invalid room number or room not mentioned.")


# ==========================================
# 5. SAFETY NET
# ==========================================

def apply_safety_net(complaint, ai_urgent):

    safety_words = [
        "spark",
        "shock",
        "overflowing",
        "near the switch",
        "flooding",
        "burning smell"
    ]

    complaint_lower = complaint.lower()

    safety_detected = any(
        word in complaint_lower
        for word in safety_words
    )

    # Python can increase urgency but never decrease it.
    final_urgent = ai_urgent or safety_detected

    return final_urgent


final_urgent = apply_safety_net(
    complaint,
    result["urgent"]
)

print("\nFinal Urgency:", final_urgent)


# ==========================================
# 6. MAINTENANCE TEAM ASSIGNMENT
# ==========================================

def assign(issue):

    team_mapping = {
        "electrical": "Electrical Maintenance Team",
        "plumbing": "Plumbing Maintenance Team",
        "carpentry": "Carpentry Maintenance Team",
        "cleaning": "Housekeeping Team",
        "internet": "IT Support Team",
        "other": "General Maintenance Team"
    }

    return team_mapping.get(
        issue.lower(),
        "General Maintenance Team"
    )


assigned_team = assign(result["issue"])

print("\nAssigned Team:", assigned_team)


# ==========================================
# 7. DUE DATE CALCULATION
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


opened_date = datetime.now().strftime("%Y-%m-%d")

deadline = due_date(opened_date, final_urgent)

print("\nOpened Date:", opened_date)
print("Urgent:", final_urgent)
print("Due Date:", deadline)


# ==========================================
# 8. FINAL OUTPUT
# ==========================================

print("\n========== FINAL TICKET DETAILS ==========")

print("Room          :", room)
print("Issue         :", result["issue"])
print("Urgent        :", final_urgent)
print("Summary       :", result["summary"])
print("Assigned Team :", assigned_team)
print("Due Date      :", deadline)

print("\nProgram executed successfully!")

# ==========================================
# 9. DUPLICATE TICKET DETECTION
# ==========================================

def load_open_tickets(filename):

    ticket_dictionary = {}

    try:
        with open(filename, "r", newline="") as file:

            reader = csv.DictReader(file)

            for row in reader:

                key = (row["room"], row["issue"].lower())

                ticket_dictionary[key] = {
                    "ticket": row["ticket"],
                    "opened": row["opened"],
                    "complaints": []
                }

    except FileNotFoundError:
        print("Open tickets file not found!")

    return ticket_dictionary


def find_duplicate(room, issue, ticket_dictionary):

    key = (room, issue.lower())

    if key in ticket_dictionary:
        return ticket_dictionary[key]["ticket"]

    return None


# Load existing tickets
tickets = load_open_tickets("open_tickets.csv")

# Check for duplicate
duplicate_ticket = find_duplicate(
    room,
    result["issue"],
    tickets
)

if duplicate_ticket:
    print("\nDuplicate found!")
    print("Join existing ticket:", duplicate_ticket)

else:
    print("\nNo duplicate found.")
    print("A new ticket can be created.")

# ==========================================
# 10. GENERATE PROJECT REPORTS
# ==========================================

def write_reports(
    complaint,
    result,
    room_valid,
    urgent,
    team,
    deadline,
    duplicate_ticket,
    tickets
):

    # Create a list for complaint results
    results = []

    needs_info = []

    # Decide the complaint status
    if not room_valid:

        status = "needs more info"

        needs_info.append({
            "complaint": complaint,
            "reason": "Missing or invalid room number"
        })

    elif duplicate_ticket:

        status = "duplicate"

        tickets[(result["room"], result["issue"])]["complaints"].append(
            complaint
        )

        tickets[(result["room"], result["issue"])]["urgent"] = (
            tickets[(result["room"], result["issue"])].get("urgent", False)
            or urgent
        )

    else:

        status = "new ticket"

        new_ticket = f"T{len(tickets) + 1:03d}"

        tickets[(result["room"], result["issue"])] = {
            "ticket": new_ticket,
            "opened": datetime.now().strftime("%Y-%m-%d"),
            "complaints": [complaint],
            "urgent": urgent,
            "team": team,
            "due_date": deadline
        }

    results.append({
        "complaint": complaint,
        "room": result["room"],
        "issue": result["issue"],
        "urgent": urgent,
        "status": status
    })

    # Write results.csv
    with open("results.csv", "w", newline="") as file:

        fields = [
            "complaint", "room", "issue",
            "urgent", "status"
        ]

        writer = csv.DictWriter(file, fieldnames=fields)

        writer.writeheader()
        writer.writerows(results)

    # Write needs_info.csv
    with open("needs_info.csv", "w", newline="") as file:

        fields = ["complaint", "reason"]

        writer = csv.DictWriter(file, fieldnames=fields)

        writer.writeheader()
        writer.writerows(needs_info)

    # Write work_orders.csv
    with open("work_orders.csv", "w", newline="") as file:

        fields = [
            "ticket", "room", "issue", "team",
            "urgent", "opened", "due_date", "complaints"
        ]

        writer = csv.DictWriter(file, fieldnames=fields)

        writer.writeheader()

        orders = []

        for (ticket_room, issue), data in tickets.items():

            orders.append({
                "ticket": data["ticket"],
                "room": ticket_room,
                "issue": issue,
                "team": data.get("team", assign(issue)),
                "urgent": data.get("urgent", False),
                "opened": data["opened"],
                "due_date": data.get("due_date", ""),
                "complaints": " | ".join(data["complaints"])
            })

        orders.sort(key=lambda x: not x["urgent"])

        writer.writerows(orders)

    # Write summary.txt
    team_counts = {}
    block_counts = {}

    for (ticket_room, issue), data in tickets.items():

        assigned = data.get("team", assign(issue))

        team_counts[assigned] = team_counts.get(assigned, 0) + 1

        block = ticket_room[0]

        block_counts[block] = block_counts.get(block, 0) + 1

    with open("summary.txt", "w") as file:

        file.write("HOSTEL MAINTENANCE SUMMARY\n\n")

        file.write("TICKETS BY TEAM\n")

        for team_name, count in team_counts.items():
            file.write(f"{team_name}: {count}\n")

        file.write("\nTICKETS BY BLOCK\n")

        for block, count in block_counts.items():
            file.write(f"Block {block}: {count}\n")

    print("\nAll four reports generated successfully!")
write_reports(
    complaint,
    result,
    check_room(room, complaint),
    final_urgent,
    assigned_team,
    deadline,
    duplicate_ticket,
    tickets
)