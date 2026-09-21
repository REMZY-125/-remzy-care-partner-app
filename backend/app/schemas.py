"""
Pydantic schemas for Remzy Care Partner API.
Request and response formats for all endpoints.
"""

from pydantic import BaseModel, EmailStr, Field
from datetime import date, datetime
from typing import Optional, List


# ============================================================
# AUTH SCHEMAS
# ============================================================

class LoginRequest(BaseModel):
    """Login request — phone and password."""
    phone: str = Field(..., min_length=10, max_length=15)
    password: str = Field(..., min_length=4, max_length=100)


class TokenResponse(BaseModel):
    """Login response — JWT token and basic user info."""
    access_token: str
    token_type: str = "bearer"
    care_partner_id: int
    full_name: str


class UserProfileResponse(BaseModel):
    """User profile information."""
    id: int
    full_name: str
    phone: str
    email: Optional[str] = None
    care_point_id: Optional[int] = None
    is_active: bool

    class Config:
        from_attributes = True


class ProfileUpdateRequest(BaseModel):
    """Request to update user profile."""
    full_name: Optional[str] = Field(None, min_length=2, max_length=100)
    email: Optional[EmailStr] = None


# ============================================================
# ATTENDANCE SCHEMAS
# ============================================================

class AttendanceResponse(BaseModel):
    """Single attendance record."""
    id: int
    care_partner_id: int
    date: date
    check_in: Optional[datetime] = None
    check_out: Optional[datetime] = None
    status: str
    notes: Optional[str] = None

    class Config:
        from_attributes = True


class CheckInResponse(BaseModel):
    """Response after successful check-in."""
    message: str
    attendance: AttendanceResponse


class CheckOutResponse(BaseModel):
    """Response after successful check-out."""
    message: str
    attendance: AttendanceResponse


class AttendanceHistoryResponse(BaseModel):
    """Paged attendance history."""
    total: int
    records: List[AttendanceResponse]


# ============================================================
# LEAVE SCHEMAS
# ============================================================

class LeaveApplyRequest(BaseModel):
    """Request to apply for leave."""
    leave_type: str = Field(..., min_length=3, max_length=50)
    start_date: date
    end_date: date
    reason: Optional[str] = Field(None, max_length=500)


class LeaveResponse(BaseModel):
    """Single leave record."""
    id: int
    care_partner_id: int
    leave_type: str
    start_date: date
    end_date: date
    reason: Optional[str] = None
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


class LeaveHistoryResponse(BaseModel):
    """Paged leave history."""
    total: int
    records: List[LeaveResponse]


# ============================================================
# WORKDAY SCHEMAS
# ============================================================

class AssignmentItem(BaseModel):
    """Single assignment in today's workday."""
    id: int
    client_name: str
    client_address: Optional[str] = None
    shift_start: Optional[datetime] = None
    shift_end: Optional[datetime] = None
    task_description: Optional[str] = None
    status: str


class WorkdayResponse(BaseModel):
    """Today's workday summary."""
    date: date
    care_partner_name: str
    total_assignments: int
    completed_assignments: int
    attendance_status: str
    check_in_time: Optional[datetime] = None
    check_out_time: Optional[datetime] = None
    assignments: List[AssignmentItem]