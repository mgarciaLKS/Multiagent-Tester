"""
Database layer for TODO application
"""
from typing import List, Optional
from .models import Task, User


class Database:
    """Simple in-memory database"""
    
    def __init__(self):
        self.tasks: List[Task] = []
        self.users: List[User] = []
        self._next_task_id = 1
        self._next_user_id = 1
    
    def add_task(self, title: str, description: str) -> Task:
        """Add a new task"""
        task = Task(
            id=self._next_task_id,
            title=title,
            description=description
        )
        self.tasks.append(task)
        self._next_task_id += 1
        return task
    
    def get_task(self, task_id: int) -> Optional[Task]:
        """Get task by ID"""
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None
    
    def get_all_tasks(self) -> List[Task]:
        """Get all tasks"""
        return self.tasks.copy()
    
    def delete_task(self, task_id: int) -> bool:
        """Delete a task"""
        task = self.get_task(task_id)
        if task:
            self.tasks.remove(task)
            return True
        return False
    
    def add_user(self, username: str, email: str) -> User:
        """Add a new user"""
        user = User(
            id=self._next_user_id,
            username=username,
            email=email
        )
        self.users.append(user)
        self._next_user_id += 1
        return user
    
    def get_user(self, user_id: int) -> Optional[User]:
        """Get user by ID"""
        for user in self.users:
            if user.id == user_id:
                return user
        return None
    
    def get_user_by_username(self, username: str) -> Optional[User]:
        """Get user by username"""
        for user in self.users:
            if user.username == username:
                return user
        return None
