import uuid

def get_session_id():
    return f"si-{uuid.uuid4().hex}"