# Sample TODO Application

A simple task management application for testing purposes.

## Structure

- `models.py` - Data models (Task, User)
- `database.py` - Database layer (in-memory storage)
- `services.py` - Business logic layer
- `api.py` - API interface layer

## Features

- Create, read, update, delete tasks
- Mark tasks as completed
- User registration and management
- Input validation

## Usage

```python
from sample_project import TodoAPI

api = TodoAPI()

# Create a task
response = api.create_task({
    'title': 'Buy groceries',
    'description': 'Milk, eggs, bread'
})

# Get all tasks
tasks = api.get_tasks()

# Complete a task
api.complete_task(task_id=1)
```

This project is designed to demonstrate unit, functional, and integration testing.
