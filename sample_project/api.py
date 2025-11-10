"""
API layer for TODO application
"""
from typing import Dict, List, Any
from .services import TaskService, UserService
from .database import Database


class TodoAPI:
    """RESTful API interface for TODO application"""
    
    def __init__(self):
        self.db = Database()
        self.task_service = TaskService(self.db)
        self.user_service = UserService(self.db)
    
    def create_task(self, data: Dict[str, str]) -> Dict[str, Any]:
        """Create a new task via API"""
        try:
            title = data.get('title', '')
            description = data.get('description', '')
            
            task = self.task_service.create_task(title, description)
            
            return {
                'success': True,
                'task': {
                    'id': task.id,
                    'title': task.title,
                    'description': task.description,
                    'completed': task.completed,
                    'created_at': task.created_at.isoformat()
                }
            }
        except ValueError as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_tasks(self, filters: Dict[str, Any] = None) -> Dict[str, Any]:
        """Get tasks with optional filters"""
        filters = filters or {}
        
        if filters.get('status') == 'completed':
            tasks = self.task_service.get_completed_tasks()
        elif filters.get('status') == 'pending':
            tasks = self.task_service.get_pending_tasks()
        else:
            tasks = self.db.get_all_tasks()
        
        return {
            'success': True,
            'tasks': [
                {
                    'id': task.id,
                    'title': task.title,
                    'description': task.description,
                    'completed': task.completed
                }
                for task in tasks
            ],
            'count': len(tasks)
        }
    
    def complete_task(self, task_id: int) -> Dict[str, Any]:
        """Mark a task as completed"""
        success = self.task_service.complete_task(task_id)
        
        if success:
            return {'success': True, 'message': 'Task completed'}
        else:
            return {'success': False, 'error': 'Task not found'}
    
    def delete_task(self, task_id: int) -> Dict[str, Any]:
        """Delete a task"""
        success = self.task_service.delete_task(task_id)
        
        if success:
            return {'success': True, 'message': 'Task deleted'}
        else:
            return {'success': False, 'error': 'Task not found'}
    
    def register_user(self, data: Dict[str, str]) -> Dict[str, Any]:
        """Register a new user"""
        try:
            username = data.get('username', '')
            email = data.get('email', '')
            
            user = self.user_service.register_user(username, email)
            
            return {
                'success': True,
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'is_active': user.is_active
                }
            }
        except ValueError as e:
            return {
                'success': False,
                'error': str(e)
            }
