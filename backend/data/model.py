"""
Data models for the Agentic University Admission System.
These models define the structure of data stored in the Supabase database.
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import List, Optional, Dict, Union


class ApplicationStatus(str, Enum):
    SUBMITTED = "submitted"
    UNDER_REVIEW = "under_review"
    DOCUMENTS_VERIFIED = "documents_verified"
    SHORTLISTED = "shortlisted"
    REJECTED = "rejected"
    ADMITTED = "admitted"
    FEE_SLIP_SENT = "fee_slip_sent"


class LoanStatus(str, Enum):
    REQUESTED = "requested"
    UNDER_PROCESS = "under_process"
    APPROVED = "approved"
    REJECTED = "rejected"
    DISBURSED = "disbursed"


@dataclass
class Document:
    """Represents a submitted document."""
    name: str
    type: str  # e.g., ID, transcript, recommendation_letter
    uploaded_date: datetime = field(default_factory=datetime.now)
    is_valid: bool = False
    remarks: Optional[str] = None


@dataclass
class Application:
    """Represents a student application."""
    id: Optional[str] = None
    student_id: str = ""
    submission_date: datetime = field(default_factory=datetime.now)
    status: ApplicationStatus = ApplicationStatus.SUBMITTED
    documents: List[Document] = field(default_factory=list)
    eligible: bool = False
    shortlisted_by: Optional[str] = None
    updated_on: datetime = field(default_factory=datetime.now)


@dataclass
class Student:
    """Represents a student."""
    id: Optional[str] = None
    name: str = ""
    email: str = ""
    phone: str = ""
    applications: List[str] = field(default_factory=list)  # List of Application IDs
    communication_history: List[str] = field(default_factory=list)  # Log IDs


@dataclass
class CommunicationLog:
    """Tracks communication with students."""
    id: Optional[str] = None
    student_id: str = ""
    message: str = ""
    sent_by: str = ""  # Agent or system
    timestamp: datetime = field(default_factory=datetime.now)
    medium: str = "email"  # email, sms, portal
    response_required: bool = False
    response_received: bool = False


@dataclass
class LoanRequest:
    """Represents a student loan request."""
    id: Optional[str] = None
    student_id: str = ""
    amount_requested: float = 0.0
    purpose: str = ""
    status: LoanStatus = LoanStatus.REQUESTED
    evaluation_notes: Optional[str] = None
    evaluated_by: Optional[str] = None
    decision_date: Optional[datetime] = None


@dataclass
class FeeSlip:
    """Represents a generated fee slip."""
    id: Optional[str] = None
    student_id: str = ""
    application_id: str = ""
    amount: float = 0.0
    generated_date: datetime = field(default_factory=datetime.now)
    due_date: Optional[datetime] = None
    is_paid: bool = False


@dataclass
class Agent:
    """Generic agent model."""
    id: Optional[str] = None
    name: str = ""
    role: str = ""  # admission_officer, document_checker, shortlisting_agent, student_counsellor, loan_agent
    active: bool = True
    assigned_tasks: List[str] = field(default_factory=list)


@dataclass
class AdmissionProcessStatus:
    """Tracks progress of the admission process for dashboard or bot queries."""
    total_applications: int = 0
    verified_documents: int = 0
    shortlisted_candidates: int = 0
    admitted_students: int = 0
    fee_slips_sent: int = 0
    loans_processed: int = 0
    last_updated: datetime = field(default_factory=datetime.now)
