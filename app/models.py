# app/models.py

from sqlalchemy import Column, Integer, String, Float, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    phone = Column(String, unique=True, nullable=False)

    # Relationships
    escrows_created = relationship("EscrowTransaction", back_populates="buyer", foreign_keys='EscrowTransaction.buyer_id')
    escrows_received = relationship("EscrowTransaction", back_populates="seller", foreign_keys='EscrowTransaction.seller_id')
    approvals = relationship("EscrowApproval", back_populates="approver")

class EscrowTransaction(Base):
    __tablename__ = "escrows"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float, nullable=False)
    description = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    buyer_id = Column(Integer, ForeignKey("users.id"))
    seller_id = Column(Integer, ForeignKey("users.id"))

    status = Column(String, default="pending")  # pending, approved, released, disputed

    # Relationships
    buyer = relationship("User", back_populates="escrows_created", foreign_keys=[buyer_id])
    seller = relationship("User", back_populates="escrows_received", foreign_keys=[seller_id])
    approvals = relationship("EscrowApproval", back_populates="escrow", cascade="all, delete")

class EscrowApproval(Base):
    __tablename__ = "approvals"

    id = Column(Integer, primary_key=True, index=True)
    escrow_id = Column(Integer, ForeignKey("escrows.id"))
    approver_id = Column(Integer, ForeignKey("users.id"))
    has_approved = Column(Boolean, default=False)

    # Relationships
    escrow = relationship("EscrowTransaction", back_populates="approvals")
    approver = relationship("User", back_populates="approvals")
