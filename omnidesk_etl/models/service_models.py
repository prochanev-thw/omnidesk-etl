from dataclasses import dataclass
from typing import List, Optional, Union
from datetime import datetime
from .base_model import BaseModel


@dataclass
class CaseCreating(BaseModel):

    user_email: str
    user_full_name: str = "User's full name"
    subject: str = "I need help"
    content: str = "I need help"
    language_id: int = 2
    lables: List[int] = None


@dataclass
class Label(BaseModel):
    label_id: int
    label_title: str


@dataclass
class LabelCase(BaseModel):
    case_id: int
    label_id: int


@dataclass
class CaseExtracting(BaseModel):
    case_id: int
    case_number: str
    subject: str
    user_id: int
    staff_id: int
    group_id: int
    status: str
    priority: str
    channel: str
    recipient: str
    cc_emails: str
    bcc_emails: str
    deleted: bool
    spam: bool
    created_at: datetime
    updated_at: datetime
    language_id: int
    raiting: str = None
    raiting_comment: str = None
    rated_staff_id: int = None
    closing_speed: Optional[Union[int, str]] = None
    labels: List[int] = None

    def __post_init__(self):
        self.created_at = self.created_at.date()
        self.updated_at = self.updated_at.date()
        if self.closing_speed == "-":
            self.closing_speed = None

    @property
    def labels_objects(self):

        if self.labels:
            return [
                LabelCase(self.case_id, label_id)
                for label_id in self.labels
            ]
