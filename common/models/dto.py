from pydantic import BaseModel

class UniMsg(BaseModel):
    content: str
    round: int
    role_type: str