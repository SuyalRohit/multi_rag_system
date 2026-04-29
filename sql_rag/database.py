from sqlalchemy import create_engine, text
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "database", "mydb.db")

engine = create_engine(f"sqlite:///{DB_PATH}")

def run_query(sql_query):
    with engine.connect() as conn:
        result = conn.execute(text(sql_query))
        return result.fetchall()


def get_schema():
    return """
Tables:

customers(customer_id, name, email, phone, plan_type, created_at, status)
tickets(ticket_id, customer_id, issue_type, priority, status, created_at, resolved_at, assigned_to)
incidents(incident_id, severity, service, description, status, created_at, resolved_at, owner)
sla_tracking(record_id, entity_type, entity_id, priority_or_severity, response_time_minutes, resolution_time_minutes, sla_breached)
"""