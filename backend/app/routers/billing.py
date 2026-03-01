from fastapi import APIRouter
import uuid

router = APIRouter()

@router.get("/packages")
def list_packages():
    return [
        {"id": "basic", "credits": 100, "price": 5},
        {"id": "pro", "credits": 300, "price": 10},
        {"id": "ultimate", "credits": 1000, "price": 25},
    ]

@router.post("/create-session")
def create_checkout_session(package_id: str):
    checkout_id = str(uuid.uuid4())
    checkout_url = f"https://buy.polar.sh/{checkout_id}"

    return {"url": checkout_url}
