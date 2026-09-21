"""
API routes for Remzy Care Partner API.
All endpoints in one file.
"""

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import CarePartner
from app.schemas import (
    LoginRequest, TokenResponse,
    UserProfileResponse, ProfileUpdateRequest,
    AttendanceResponse, CheckInResponse, CheckOutResponse,
    AttendanceHistoryResponse,
    LeaveApplyRequest, LeaveResponse, LeaveHistoryResponse,
    WorkdayResponse,
)
from app import services
from app.utils.security import verify_password, create_access_token
from app.utils.deps import get_current_user


# ============================================================
# AUTH ROUTER
# ============================================================

auth_router = APIRouter(prefix="/auth", tags=["Auth"])


@auth_router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    """Authenticate user and return JWT token."""
    user = db.query(CarePartner).filter(
        CarePartner.phone == payload.phone
    ).first()

    if not user or not verify_password(payload.password, user.password_hash):
        from fastapi import HTTPException
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid phone number or password."
        )

    if not user.is_active:
        from fastapi import HTTPException
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is inactive."
        )

    token = create_access_token({"sub": str(user.id), "name": user.full_name})

    return TokenResponse(
        access_token=token,
        care_partner_id=user.id,
        full_name=user.full_name,
    )


@auth_router.get("/me", response_model=UserProfileResponse)
def get_me(current_user: CarePartner = Depends(get_current_user)):
    """Get current user's profile."""
    return UserProfileResponse.model_validate(current_user)


@auth_router.put("/profile", response_model=UserProfileResponse)
def update_profile(
    payload: ProfileUpdateRequest,
    current_user: CarePartner = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Update current user's profile."""
    if payload.full_name is not None:
        current_user.full_name = payload.full_name
    if payload.email is not None:
        current_user.email = payload.email

    try:
        db.commit()
        db.refresh(current_user)
    except Exception as e:
        db.rollback()
        from fastapi import HTTPException
        raise HTTPException(status_code=500, detail=str(e))

    return UserProfileResponse.model_validate(current_user)


# ============================================================
# ATTENDANCE ROUTER
# ============================================================

attendance_router = APIRouter(prefix="/attendance", tags=["Attendance"])


@attendance_router.post("/check-in", response_model=CheckInResponse)
def check_in(
    current_user: CarePartner = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Mark check-in for today."""
    record = services.check_in(db, current_user.id)
    return CheckInResponse(
        message="Check-in successful.",
        attendance=AttendanceResponse.model_validate(record)
    )


@attendance_router.post("/check-out", response_model=CheckOutResponse)
def check_out(
    current_user: CarePartner = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Mark check-out for today."""
    record = services.check_out(db, current_user.id)
    return CheckOutResponse(
        message="Check-out successful.",
        attendance=AttendanceResponse.model_validate(record)
    )


@attendance_router.get("/history", response_model=AttendanceHistoryResponse)
def attendance_history(
    limit: int = 30,
    offset: int = 0,
    current_user: CarePartner = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get attendance history."""
    records = services.get_attendance_history(
        db, current_user.id, limit=limit, offset=offset
    )
    total = services.get_attendance_count(db, current_user.id)
    return AttendanceHistoryResponse(
        total=total,
        records=[AttendanceResponse.model_validate(r) for r in records]
    )
    

# ============================================================
# LEAVE ROUTER
# ============================================================

leave_router = APIRouter(prefix="/leave", tags=["Leave"])


@leave_router.post("/apply", response_model=LeaveResponse, status_code=201)
def apply_leave(
    payload: LeaveApplyRequest,
    current_user: CarePartner = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Submit a leave application."""
    leave = services.apply_leave(db, current_user.id, payload)
    return LeaveResponse.model_validate(leave)


@leave_router.get("/history", response_model=LeaveHistoryResponse)
def leave_history(
    limit: int = 30,
    offset: int = 0,
    current_user: CarePartner = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get leave history."""
    records = services.get_leave_history(
        db, current_user.id, limit=limit, offset=offset
    )
    total = services.get_leave_count(db, current_user.id)
    return LeaveHistoryResponse(
        total=total,
        records=[LeaveResponse.model_validate(r) for r in records]
    )


# ============================================================
# WORKDAY ROUTER
# ============================================================

workday_router = APIRouter(prefix="/workday", tags=["Workday"])


@workday_router.get("/today", response_model=WorkdayResponse)
def workday_today(
    current_user: CarePartner = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get today's workday summary."""
    return services.get_today_workday(db, current_user.id)


# ============================================================
# EXPORT ALL ROUTERS
# ============================================================

__all__ = [
    "auth_router",
    "attendance_router",
    "leave_router",
    "workday_router",
]