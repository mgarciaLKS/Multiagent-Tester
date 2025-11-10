"""
Data models for the TODO application
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Task:
    """Represents a task in the TODO list"""
    id: int
    title: str
    description: str
    completed: bool = False
    created_at: datetime = None
    completed_at: Optional[datetime] = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()
    
    def mark_completed(self):
        """Mark task as completed"""
        self.completed = True
        self.completed_at = datetime.now()
    
    def mark_incomplete(self):
        """Mark task as incomplete"""
        self.completed = False
        self.completed_at = None


@dataclass
class User:
    """Represents a user"""
    id: int
    username: str
    email: str
    is_active: bool = True
    
    def validate_email(self) -> bool:
        """Simple email validation"""
        return '@' in self.email and '.' in self.email.split('@')[1]
