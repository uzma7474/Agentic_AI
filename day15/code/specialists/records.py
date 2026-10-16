from agents import Agent, Runner, function_tool
from config import MODEL
from database import get_connection

@function_tool
def find_records(record_type: str = "") -> str:
    """Find medical records, optionally filtered by type (Lab Report, Imaging, Discharge Summary)."""
    conn = get_connection()
    cur = conn.cursor()
    if record_type:
        cur.execute(
            "SELECT id, title, type, date FROM medical_records WHERE patient_id = %s AND type LIKE %s ORDER BY date DESC",
            ("PAT-001", f"%{record_type}%"),
        )
    else:
        cur.execute(
            "SELECT id, title, type, date FROM medical_records WHERE patient_id = %s ORDER BY date DESC",
            ("PAT-001",),
        )
    rows = cur.fetchall()
    cur.close()
    conn.close()
    if not rows:
        return f"No records found matching '{record_type}'. Available types: Lab Report, Imaging, Discharge Summary"
    lines = [f"  {r['id']}: {r['title']} ({r['type']}) - {r['date']}" for r in rows]
    return "Your medical records:\n" + "\n".join(lines)

@function_tool
def get_record_detail(record_id: str) -> str:
    """Get the full details of a specific medical record by its ID (e.g., REC-001)."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT title, type, date, summary FROM medical_records WHERE id = %s",
        (record_id,),
    )
    row = cur.fetchone()
    cur.close()
    conn.close()
    if not row:
        return f"Record {record_id} not found."
    return (
        f"Record: {row['title']}\n"
        f"Type: {row['type']}\n"
        f"Date: {row['date']}\n"
        f"Summary: {row['summary']}"
    )

@function_tool
def find_discharge_documents() -> str:
    """Find all discharge summaries and documents."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT id, title, date FROM medical_records WHERE patient_id = %s AND type = %s ORDER BY date DESC",
        ("PAT-001", "Discharge Summary"),
    )
    rows = cur.fetchall()
    cur.close()
    conn.close()
    if not rows:
        return "No discharge documents found."
    lines = [f"  {r['id']}: {r['title']} ({r['date']})" for r in rows]
    return "Discharge Documents:\n" + "\n".join(lines)


agent = Agent(
    name="Records Agent",
    instructions=(
        "You are a medical records specialist. Help users find their previous reports, "
        "explain report contents, and locate discharge documents. Use the available tools "
        "to look up records. Present information clearly and note that this is for "
        "informational purposes — always recommend discussing results with their doctor."
    ),
    model=MODEL,
    tools=[find_records, get_record_detail, find_discharge_documents],
)


def run_records_agent(query: str) -> str:
    """Run the records agent on a user query."""
    result = Runner.run_sync(agent, query)
    return result.final_output
