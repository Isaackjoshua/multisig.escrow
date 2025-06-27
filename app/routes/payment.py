# app/routes/payment.py

from fastapi import APIRouter, Query
from app.utils import payment  # Import the module, not the function

router = APIRouter()

@router.post("/pay/test")
def test_stk_push(phone_number: str = Query(...), amount: int = Query(...)):
    return payment.initiate_stk_push(phone_number, amount)
