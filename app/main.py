# app/main.py

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine, Base
from app import models, schemas, crud

app = FastAPI()
Base.metadata.create_all(bind=engine)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# === Test ===
@app.get("/")
def read_root():
    return {"message": "Multisig Escrow API is running!"}


# === USERS ===
@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db, user)

@app.get("/users/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_users(db, skip=skip, limit=limit)

@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

# === ESCROWS ===
@app.post("/escrows/", response_model=schemas.Escrow)
def create_escrow(escrow: schemas.EscrowCreate, db: Session = Depends(get_db)):
    return crud.create_escrow(db, escrow)

@app.get("/escrows/", response_model=list[schemas.Escrow])
def read_escrows(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_escrows(db, skip=skip, limit=limit)

@app.get("/escrows/{escrow_id}", response_model=schemas.Escrow)
def read_escrow(escrow_id: int, db: Session = Depends(get_db)):
    db_escrow = crud.get_escrow(db, escrow_id)
    if not db_escrow:
        raise HTTPException(status_code=404, detail="Escrow not found")
    return db_escrow
# === APPROVALS ===

@app.post("/approvals/", response_model=schemas.Approval)
def create_approval(approval: schemas.ApprovalCreate, db: Session = Depends(get_db)):
    return crud.create_approval(db, approval)

@app.post("/approvals/approve")
def approve_escrow(escrow_id: int, approver_id: int, db: Session = Depends(get_db)):
    try:
        approval = crud.approve_escrow(db, escrow_id, approver_id)
        return {"message": "Approved successfully", "approval": approval}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/escrows/{escrow_id}/approvals", response_model=list[schemas.Approval])
def get_approvals(escrow_id: int, db: Session = Depends(get_db)):
    return crud.get_approvals_for_escrow(db, escrow_id)

@app.post("/payment/callback")
def payment_callback(data: dict):
    print("Received callback:", data)
    # Simulate confirming payment
    return {"status": "received"}

from app.utils.payment import initiate_stk_push

@app.post("/pay/test")
def pay_test(phone_number: str = "254708374149", amount: int = 10):
    res = initiate_stk_push(phone_number, amount)
    return res
