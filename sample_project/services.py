"""
Service layer for TODO application - Business logic
"""
from typing import List, Optional
from .database import Database
from .models import Task, User


class TaskService:
    """Business logic for task management"""
    
    def __init__(self, database: Database):
        self.db = database
    
    def create_task(self, title: str, description: str) -> Task:
        """Create a new task with validation"""
        if not title or not title.strip():
            raise ValueError("Task title cannot be empty")
        
        if len(title) > 100:
            raise ValueError("Task title too long (max 100 characters)")
        
        return self.db.add_task(title.strip(), description.strip())
    
    def complete_task(self, task_id: int) -> bool:
        """Mark a task as completed"""
        task = self.db.get_task(task_id)
        if not task:
            return False
        
        task.mark_completed()
        return True
    
    def get_pending_tasks(self) -> List[Task]:
        """Get all incomplete tasks"""
        return [task for task in self.db.get_all_tasks() if not task.completed]
    
    def get_completed_tasks(self) -> List[Task]:
        """Get all completed tasks"""
        return [task for task in self.db.get_all_tasks() if task.completed]
    
    def delete_task(self, task_id: int) -> bool:
        """Delete a task"""
        return self.db.delete_task(task_id)


class UserService:
    """Business logic for user management"""
    
    def __init__(self, database: Database):
        self.db = database
    
    def register_user(self, username: str, email: str) -> User:
        """Register a new user with validation"""
        if not username or not username.strip():
            raise ValueError("Username cannot be empty")
        
        if len(username) < 3:
            raise ValueError("Username too short (min 3 characters)")
        
        # Check if username already exists
        if self.db.get_user_by_username(username):
            raise ValueError(f"Username '{username}' already exists")
        
        user = self.db.add_user(username, email)
        
        if not user.validate_email():
            raise ValueError("Invalid email format")
        
        return user
    
    def deactivate_user(self, user_id: int) -> bool:
        """Deactivate a user"""
        user = self.db.get_user(user_id)
        if not user:
            return False
        
        user.is_active = False
        return True
