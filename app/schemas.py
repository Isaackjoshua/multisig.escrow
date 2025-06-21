# app/schemas.py

from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

# Shared schema for User
class UserBase(BaseModel):
    name: str
    phone: str

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int

    class Config:
        orm_mode = True


# Shared schema for Escrow
class EscrowBase(BaseModel):
    amount: float
    description: Optional[str] = None
    buyer_id: int
    seller_id: int

class EscrowCreate(EscrowBase):
    pass

class Escrow(EscrowBase):
    id: int
    status: str
    created_at: datetime

    class Config:
        orm_mode = True


# Shared schema for Approval
class ApprovalBase(BaseModel):
    escrow_id: int
    approver_id: int

class ApprovalCreate(ApprovalBase):
    pass

class Approval(ApprovalBase):
    id: int
    has_approved: bool

    class Config:
        orm_mode = True
