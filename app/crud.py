# app/crud.py

from sqlalchemy.orm import Session
from app import models, schemas

# ========== USER ==========

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(name=user.name, phone=user.phone)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_users(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.User).offset(skip).limit(limit).all()

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

# ========== ESCROW ==========

def create_escrow(db: Session, escrow: schemas.EscrowCreate):
    db_escrow = models.EscrowTransaction(
        amount=escrow.amount,
        description=escrow.description,
        buyer_id=escrow.buyer_id,
        seller_id=escrow.seller_id
    )
    db.add(db_escrow)
    db.commit()
    db.refresh(db_escrow)
    return db_escrow

def get_escrow(db: Session, escrow_id: int):
    return db.query(models.EscrowTransaction).filter(models.EscrowTransaction.id == escrow_id).first()

def get_escrows(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.EscrowTransaction).offset(skip).limit(limit).all()

# ========== APPROVAL ==========

def create_approval(db: Session, approval: schemas.ApprovalCreate):
    existing = db.query(models.EscrowApproval).filter_by(
        escrow_id=approval.escrow_id,
        approver_id=approval.approver_id
    ).first()

    if existing:
        return existing  # prevent duplicate approval records

    db_approval = models.EscrowApproval(
        escrow_id=approval.escrow_id,
        approver_id=approval.approver_id
    )
    db.add(db_approval)
    db.commit()
    db.refresh(db_approval)
    return db_approval

def approve_escrow(db: Session, escrow_id: int, approver_id: int):
    approval = db.query(models.EscrowApproval).filter_by(
        escrow_id=escrow_id,
        approver_id=approver_id
    ).first()

    if not approval:
        raise ValueError("Approval record not found.")

    if approval.has_approved:
        return approval  # already approved

    approval.has_approved = True
    db.commit()
    db.refresh(approval)

    # Check if enough approvals exist
    total_approvals = db.query(models.EscrowApproval).filter_by(escrow_id=escrow_id).count()
    approved_count = db.query(models.EscrowApproval).filter_by(escrow_id=escrow_id, has_approved=True).count()

    if total_approvals > 0 and approved_count >= 2:  # Minimum 2 out of 3
        escrow = db.query(models.EscrowTransaction).filter_by(id=escrow_id).first()
        if escrow and escrow.status != "released":
            escrow.status = "released"
            db.commit()

    return approval

def get_approvals_for_escrow(db: Session, escrow_id: int):
    return db.query(models.EscrowApproval).filter_by(escrow_id=escrow_id).all()
