"""
TODO Application - Simple task management system

This is a sample project for testing purposes.
It includes:
- Data models (Task, User)
- Database layer (in-memory storage)
- Service layer (business logic)
- API layer (REST-like interface)
"""

from .models import Task, User
from .database import Database
from .services import TaskService, UserService
from .api import TodoAPI

__version__ = "0.1.0"
__all__ = ['Task', 'User', 'Database', 'TaskService', 'UserService', 'TodoAPI']
