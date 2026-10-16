from agents import Agent, Runner, function_tool
from config import MODEL
from database import get_connection

@function_tool
def check_appointments(patient_id: str = "PAT-001") -> str:
    """Check existing appointments for a patient."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT id, doctor, date, time, type FROM appointments WHERE patient_id = %s ORDER BY date",
        (patient_id,),
    )
    rows = cur.fetchall()
    cur.close()
    conn.close()
    if not rows:
        return "No appointments found for this patient ID."
    lines = [f"  {r['id']}: {r['type']} with {r['doctor']} on {r['date']} at {r['time']}" for r in rows]
    return "Your appointments:\n" + "\n".join(lines)

@function_tool
def book_appointment(doctor: str, date_str: str, time: str, apt_type: str = "General Checkup") -> str:
    """Book a new appointment with a doctor on a specific date and time. Use date in YYYY-MM-DD format."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) AS cnt FROM appointments")
    cnt = cur.fetchone()["cnt"]
    new_id = f"APT-{cnt + 1:03d}"
    cur.execute(
        "INSERT INTO appointments (id, patient_id, doctor, date, time, type) VALUES (%s, %s, %s, %s, %s, %s)",
        (new_id, "PAT-001", doctor, date_str, time, apt_type),
    )
    conn.commit()
    cur.close()
    conn.close()
    return f"Appointment booked successfully! Your appointment ID is {new_id} with {doctor} on {date_str} at {time} for {apt_type}."

@function_tool
def cancel_appointment(appointment_id: str) -> str:
    """Cancel an existing appointment by its ID."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, doctor, date, type FROM appointments WHERE id = %s", (appointment_id,))
    row = cur.fetchone()
    if not row:
        cur.close()
        conn.close()
        return f"Appointment {appointment_id} not found. Please check the ID and try again."
    cur.execute("DELETE FROM appointments WHERE id = %s", (appointment_id,))
    conn.commit()
    cur.close()
    conn.close()
    return f"Appointment {appointment_id} ({row['type']} with {row['doctor']} on {row['date']}) has been canceled."

@function_tool
def reschedule_appointment(appointment_id: str, new_date: str, new_time: str) -> str:
    """Reschedule an existing appointment to a new date (YYYY-MM-DD) and time."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, date, time FROM appointments WHERE id = %s", (appointment_id,))
    row = cur.fetchone()
    if not row:
        cur.close()
        conn.close()
        return f"Appointment {appointment_id} not found."
    cur.execute(
        "UPDATE appointments SET date = %s, time = %s WHERE id = %s",
        (new_date, new_time, appointment_id),
    )
    conn.commit()
    cur.close()
    conn.close()
    return f"Appointment {appointment_id} rescheduled from {row['date']} {row['time']} to {new_date} {new_time}."

@function_tool
def list_available_slots(doctor: str = "") -> str:
    """List available appointment slots, optionally filtered by doctor name."""
    conn = get_connection()
    cur = conn.cursor()
    if doctor:
        cur.execute("SELECT date, time, doctor FROM available_slots WHERE doctor LIKE %s ORDER BY date", (f"%{doctor}%",))
    else:
        cur.execute("SELECT date, time, doctor FROM available_slots ORDER BY date")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    if not rows:
        return "No available slots found."
    lines = [f"  {r['date']} at {r['time']} with {r['doctor']}" for r in rows]
    return "Available slots:\n" + "\n".join(lines)



agent = Agent(
    name="Appointment Agent",
    instructions=(
        "You are a healthcare appointment specialist. "
        "Help users book, reschedule, cancel, and check appointments. "
        "Always use the available tools to perform actions. "
        "Confirm details with the user before making changes."
    ),
    model=MODEL,
    tools=[check_appointments, book_appointment, cancel_appointment, reschedule_appointment, list_available_slots]   
)

def run_appointment_agent(user_query: str):
    response = Runner.run_sync(
        starting_agent=agent,
        input=user_query
    )
    return response.final_output