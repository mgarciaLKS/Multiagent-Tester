
import os
import sys
sys.path.insert(0, '/home/mgarcia/Desktop/Otros/IA/CURSO UPV MCP/testing-multiagent/sample_project')

import pytest
from datetime import datetime, timedelta

# Import models directly (module is standalone)
import models
from models import Task, User


def test_task_creation_defaults_and_fields():
    """Task: ensure required fields set and defaults applied"""
    # Arrange
    now_before = datetime.now()

    # Act
    task = Task(id=1, title='Test', description='Desc')

    # Assert
    assert task.id == 1
    assert task.title == 'Test'
    assert task.description == 'Desc'
    assert task.completed is False
    assert isinstance(task.created_at, datetime)
    assert task.completed_at is None
    assert task.created_at >= now_before


def test_task_mark_completed_sets_state_and_timestamp(monkeypatch):
    """Task.mark_completed should set completed True and stamp completed_at"""
    task = Task(id=2, title='Do', description='X')

    # Freeze time via monkeypatch to ensure deterministic timestamp
    fixed = datetime(2022, 1, 1, 12, 0, 0)
    monkeypatch.setattr(models, 'datetime', type('DT', (), {
        'now': staticmethod(lambda: fixed),
        'fromtimestamp': datetime.fromtimestamp
    }))

    task.mark_completed()
    assert task.completed is True
    assert task.completed_at == fixed


def test_task_mark_incomplete_resets_state():
    """Task.mark_incomplete should clear completion state"""
    task = Task(id=3, title='A', description='B')
    task.mark_completed()

    task.mark_incomplete()
    assert task.completed is False
    assert task.completed_at is None


def test_task_post_init_sets_created_at_when_none(monkeypatch):
    """Task.__post_init__: created_at set when not provided"""
    fixed = datetime(2020, 5, 17, 8, 30, 0)
    monkeypatch.setattr(models, 'datetime', type('DT', (), {
        'now': staticmethod(lambda: fixed),
        'fromtimestamp': datetime.fromtimestamp
    }))

    task = Task(id=4, title='T', description='D')
    assert task.created_at == fixed


def test_user_creation_and_email_validation():
    """User: creation fields and email validation behavior"""
    user = User(id=1, username='alice', email='alice@example.com')
    assert user.id == 1
    assert user.username == 'alice'
    assert user.is_active is True
    assert user.validate_email() is True

    bad = User(id=2, username='bob', email='no-at-symbol')
    assert bad.validate_email() is False


def test_models_repr_str_equality_basic():
    """If dataclass equality present, identical instances compare equal"""
    fixed = datetime(2021, 1, 1, 0, 0, 0)
    t1 = Task(id=10, title='x', description='y', created_at=fixed, completed_at=None, completed=False)
    t2 = Task(id=10, title='x', description='y', created_at=fixed, completed_at=None, completed=False)
    t3 = Task(id=11, title='x', description='y', created_at=fixed, completed_at=None, completed=False)
    assert t1 == t2
    assert t1 != t3

    u1 = User(id=1, username='a', email='a@b.com')
    u2 = User(id=1, username='a', email='a@b.com')
    u3 = User(id=2, username='a', email='a@b.com')
    assert u1 == u2
    assert u1 != u3
