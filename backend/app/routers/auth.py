from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import uuid

router = APIRouter()

fake_users_db = {}  # replace with Mongo/Postgres later

class SignupRequest(BaseModel):
    email: str
    password: str

@router.post("/signup")
def signup(data: SignupRequest):
    if data.email in fake_users_db:
        raise HTTPException(status_code=400, detail="User already exists")

    fake_users_db[data.email] = {
        "id": str(uuid.uuid4()),
        "email": data.email,
        "password": data.password,
        "credits": 0,
    }

    return {"message": "Account created", "email": data.email}

class LoginRequest(BaseModel):
    email: str
    password: str

@router.post("/login")
def login(data: LoginRequest):
    user = fake_users_db.get(data.email)

    if not user or user["password"] != data.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return {"message": "Login ok", "user": user}
