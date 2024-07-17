import uuid

def generate_employee_id():
    return str(uuid.uuid4())[:8]