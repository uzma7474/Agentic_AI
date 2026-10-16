from agents import Agent, Runner, function_tool
from config import MODEL
from database import get_connection

@function_tool
def get_invoices(patient_id: str = "PAT-001") -> str:
    """Retrieve all invoices for a patient."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT id, amount, status, date, description FROM invoices WHERE patient_id = %s ORDER BY date DESC",
        (patient_id,),
    )
    rows = cur.fetchall()
    cur.close()
    conn.close()
    if not rows:
        return "No invoices found for this patient."
    lines = [
        f"  {r['id']}: ${float(r['amount']):.2f} - {r['status'].upper()} - {r['description']} (Date: {r['date']})"
        for r in rows
    ]
    return "Invoices:\n" + "\n".join(lines)

@function_tool
def get_invoice_status(invoice_id: str) -> str:
    """Check the status of a specific invoice by its ID."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT id, amount, status, date, description FROM invoices WHERE id = %s",
        (invoice_id,),
    )
    row = cur.fetchone()
    cur.close()
    conn.close()
    if not row:
        return f"Invoice {invoice_id} not found."
    return (
        f"Invoice {row['id']}:\n"
        f"  Amount: ${float(row['amount']):.2f}\n"
        f"  Status: {row['status'].upper()}\n"
        f"  Description: {row['description']}\n"
        f"  Date: {row['date']}"
    )

@function_tool
def get_insurance_info(patient_id: str = "PAT-001") -> str:
    """Get current insurance coverage information for a patient."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT policy_number, provider, plan_name, deductible, out_of_pocket_max FROM insurance WHERE patient_id = %s",
        (patient_id,),
    )
    ins = cur.fetchone()
    if not ins:
        cur.close()
        conn.close()
        return "No insurance found for this patient."

    cur.execute(
        "SELECT service_type, coverage_detail FROM insurance_coverage WHERE policy_number = %s",
        (ins["policy_number"],),
    )
    coverages = cur.fetchall()
    cur.close()
    conn.close()

    lines = [
        f"Insurance Policy: {ins['policy_number']}",
        f"Provider: {ins['provider']}",
        f"Plan: {ins['plan_name']}",
        "",
        "Coverage:",
    ]
    for c in coverages:
        lines.append(f"  {c['service_type'].replace('_', ' ').title()}: {c['coverage_detail']}")
    lines.append(f"\nDeductible: {ins['deductible']}")
    lines.append(f"Out-of-pocket max: {ins['out_of_pocket_max']}")
    return "\n".join(lines)


@function_tool
def check_coverage(service_type: str) -> str:
    """Check insurance coverage for a specific service type (e.g., 'lab_work', 'imaging', 'office_visit')."""
    conn = get_connection()
    cur = conn.cursor()
    service_key = service_type.lower().replace(" ", "_")
    cur.execute(
        "SELECT coverage_detail FROM insurance_coverage WHERE service_type = %s",
        (service_key,),
    )
    row = cur.fetchone()
    cur.close()
    conn.close()
    if row:
        return f"Coverage for {service_type}: {row['coverage_detail']}"
    conn2 = get_connection()
    cur2 = conn2.cursor()
    cur2.execute("SELECT DISTINCT service_type FROM insurance_coverage")
    types = [r["service_type"].replace("_", " ") for r in cur2.fetchall()]
    cur2.close()
    conn2.close()
    return f"Service type '{service_type}' not found. Available types: {', '.join(types)}"


agent = Agent(
    name="Billing Agent",
    instructions=(
        "You are a healthcare billing and insurance specialist. "
        "Help users with invoice inquiries, payment status, and insurance coverage questions. "
        "Use the available tools to look up information. "
        "Always be clear about amounts and statuses."
    ),
    model=MODEL,
    tools=[get_invoices, get_invoice_status, get_insurance_info, check_coverage]   
)

def run_billng_agent(user_query: str):
    response = Runner.run_sync(
        starting_agent=agent,
        input=user_query
    )
    return response.final_output