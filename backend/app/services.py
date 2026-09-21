"""
Business logic for Remzy Care Partner API.
All services in one file.
"""

from datetime import date, datetime
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models import CarePartner, Attendance, Leave, Client, Assignment
from app.schemas import LeaveApplyRequest


# ============================================================
# ATTENDANCE SERVICE
# ============================================================

def get_today_attendance(db: Session, care_partner_id: int) -> Attendance:
    """Get today's attendance record for a care partner."""
    today = date.today()
    return db.query(Attendance).filter(
        Attendance.care_partner_id == care_partner_id,
        Attendance.date == today
    ).first()


def check_in(db: Session, care_partner_id: int) -> Attendance:
    """Mark check-in for today."""
    today = date.today()
    now = datetime.now()

    record = get_today_attendance(db, care_partner_id)

    if record and record.check_in:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You have already checked in today."
        )

    if not record:
        record = Attendance(
            care_partner_id=care_partner_id,
            date=today,
            check_in=now,
            status="present"
        )
        db.add(record)
    else:
        record.check_in = now
        record.status = "present"

    try:
        db.commit()
        db.refresh(record)
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to check in: {str(e)}"
        )

    return record


def check_out(db: Session, care_partner_id: int) -> Attendance:
    """Mark check-out for today."""
    now = datetime.now()
    record = get_today_attendance(db, care_partner_id)

    if not record or not record.check_in:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You must check in first before checking out."
        )

    if record.check_out:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You have already checked out today."
        )

    record.check_out = now

    try:
        db.commit()
        db.refresh(record)
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to check out: {str(e)}"
        )

    return record


def get_attendance_history(
    db: Session, care_partner_id: int, limit: int = 30, offset: int = 0
) -> list:
    """Get attendance history for a care partner."""
    if limit > 100:
        limit = 100
    if limit < 1:
        limit = 30
    if offset < 0:
        offset = 0

    return db.query(Attendance).filter(
        Attendance.care_partner_id == care_partner_id
    ).order_by(
        Attendance.date.desc()
    ).limit(limit).offset(offset).all()


def get_attendance_count(db: Session, care_partner_id: int) -> int:
    """Get total count of attendance records."""
    return db.query(Attendance).filter(
        Attendance.care_partner_id == care_partner_id
    ).count()


# ============================================================
# LEAVE SERVICE
# ============================================================

VALID_LEAVE_TYPES = ["sick", "casual", "emergency", "vacation", "personal"]


def apply_leave(
    db: Session, care_partner_id: int, payload: LeaveApplyRequest
) -> Leave:
    """Submit a new leave application."""
    # Validate leave type
    if payload.leave_type.lower() not in VALID_LEAVE_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid leave type. Valid types: {', '.join(VALID_LEAVE_TYPES)}"
        )

    # Validate dates
    if payload.end_date < payload.start_date:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="End date cannot be before start date."
        )

    # Check for overlapping leave
    overlapping = db.query(Leave).filter(
        Leave.care_partner_id == care_partner_id,
        Leave.status.in_(["pending", "approved"]),
        Leave.start_date <= payload.end_date,
        Leave.end_date >= payload.start_date
    ).first()

    if overlapping:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You already have a leave request for these dates."
        )

    # Create leave record
    leave = Leave(
        care_partner_id=care_partner_id,
        leave_type=payload.leave_type.lower(),
        start_date=payload.start_date,
        end_date=payload.end_date,
        reason=payload.reason,
        status="pending"
    )

    try:
        db.add(leave)
        db.commit()
        db.refresh(leave)
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to apply leave: {str(e)}"
        )

    return leave


def get_leave_history(
    db: Session, care_partner_id: int, limit: int = 30, offset: int = 0
) -> list:
    """Get leave history for a care partner."""
    if limit > 100:
        limit = 100
    if limit < 1:
        limit = 30
    if offset < 0:
        offset = 0

    return db.query(Leave).filter(
        Leave.care_partner_id == care_partner_id
    ).order_by(
        Leave.created_at.desc()
    ).limit(limit).offset(offset).all()


def get_leave_count(db: Session, care_partner_id: int) -> int:
    """Get total count of leave records."""
    return db.query(Leave).filter(
        Leave.care_partner_id == care_partner_id
    ).count()


# ============================================================
# WORKDAY SERVICE
# ============================================================

def get_today_workday(db: Session, care_partner_id: int) -> dict:
    """Get today's workday summary."""
    today = date.today()

    # Get care partner
    partner = db.query(CarePartner).filter(
        CarePartner.id == care_partner_id
    ).first()

    if not partner:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Care partner not found."
        )

    # Get today's attendance
    attendance = db.query(Attendance).filter(
        Attendance.care_partner_id == care_partner_id,
        Attendance.date == today
    ).first()

    # Get today's assignments
    assignments = db.query(Assignment).filter(
        Assignment.care_partner_id == care_partner_id,
        Assignment.assignment_date == today
    ).all()

    # Build assignment list with client info
    assignment_items = []
    for a in assignments:
        client = db.query(Client).filter(Client.id == a.client_id).first()
        assignment_items.append({
            "id": a.id,
            "client_name": client.full_name if client else "Unknown",
            "client_address": client.address if client else None,
            "shift_start": a.shift_start,
            "shift_end": a.shift_end,
            "task_description": a.task_description,
            "status": a.status
        })

    completed = sum(1 for a in assignments if a.status == "completed")

    return {
        "date": today,
        "care_partner_name": partner.full_name,
        "total_assignments": len(assignments),
        "completed_assignments": completed,
        "attendance_status": attendance.status if attendance else "not_started",
        "check_in_time": attendance.check_in if attendance else None,
        "check_out_time": attendance.check_out if attendance else None,
        "assignments": assignment_items
    }