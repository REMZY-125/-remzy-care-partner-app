"""
Database models for Remzy Care Partner API.
All SQLAlchemy models in one file.
"""

from sqlalchemy import (
    Column, Integer, String, Boolean, DateTime, Date, Text
)
from sqlalchemy.sql import func
from app.database import Base


class CarePartner(Base):
    """Care Partner (staff member)."""
    __tablename__ = "care_partners"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(100), nullable=False)
    phone = Column(String(15), unique=True, nullable=False, index=True)
    email = Column(String(100), nullable=True)
    password_hash = Column(String(255), nullable=False)
    care_point_id = Column(Integer, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())


class Attendance(Base):
    """Daily attendance record."""
    __tablename__ = "attendance"

    id = Column(Integer, primary_key=True, index=True)
    care_partner_id = Column(Integer, nullable=False, index=True)
    date = Column(Date, nullable=False, index=True)
    check_in = Column(DateTime, nullable=True)
    check_out = Column(DateTime, nullable=True)
    status = Column(String(20), default="present")
    notes = Column(String(500), nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())


class Leave(Base):
    """Leave application by a care partner."""
    __tablename__ = "leaves"

    id = Column(Integer, primary_key=True, index=True)
    care_partner_id = Column(Integer, nullable=False, index=True)
    leave_type = Column(String(50), nullable=False)
    start_date = Column(Date, nullable=False, index=True)
    end_date = Column(Date, nullable=False, index=True)
    reason = Column(Text, nullable=True)
    status = Column(String(20), default="pending")
    approved_by = Column(Integer, nullable=True)
    approved_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())


class Client(Base):
    """Client / patient receiving care."""
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(100), nullable=False)
    phone = Column(String(15), nullable=True, index=True)
    email = Column(String(100), nullable=True)
    address = Column(Text, nullable=True)
    city = Column(String(50), nullable=True)
    pincode = Column(String(10), nullable=True)
    care_type = Column(String(50), nullable=True)
    medical_notes = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())


class Assignment(Base):
    """Task assigned to a care partner."""
    __tablename__ = "assignments"

    id = Column(Integer, primary_key=True, index=True)
    care_partner_id = Column(Integer, nullable=False, index=True)
    client_id = Column(Integer, nullable=False, index=True)
    assignment_date = Column(Date, nullable=False, index=True)
    shift_start = Column(DateTime, nullable=True)
    shift_end = Column(DateTime, nullable=True)
    task_description = Column(Text, nullable=True)
    status = Column(String(20), default="assigned")
    completed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())