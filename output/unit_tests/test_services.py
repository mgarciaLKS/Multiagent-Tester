
import os
import sys
# Import path fix provided by supervisor
sys.path.insert(0, '/home/mgarcia/Desktop/Otros/IA/CURSO UPV MCP/testing-multiagent/sample_project')
# Also add parent to import as package
sys.path.insert(0, '/home/mgarcia/Desktop/Otros/IA/CURSO UPV MCP/testing-multiagent')

import pytest
from unittest.mock import Mock, create_autospec

from sample_project.services import TaskService, UserService
from sample_project.models import Task, User


@pytest.fixture()
def db_mock():
    """Fixture: a mock database with required methods stubbed"""
    m = Mock()
    # Task API used by services
    m.add_task = Mock()
    m.get_task = Mock()
    m.get_all_tasks = Mock(return_value=[])
    m.delete_task = Mock(return_value=True)
    # User API used by services
    m.get_user_by_username = Mock(return_value=None)
    m.add_user = Mock()
    m.get_user = Mock(return_value=None)
    return m


# ------------------------ UserService tests ------------------------

def test_user_service_register_user_validates_and_calls_db(db_mock):
    """register_user: validates username, uniqueness, email, and returns user"""
    svc = UserService(db_mock)
    user = User(id=1, username='alice', email='alice@example.com')
    db_mock.add_user.return_value = user

    result = svc.register_user('alice', 'alice@example.com')

    db_mock.get_user_by_username.assert_called_once_with('alice')
    db_mock.add_user.assert_called_once_with('alice', 'alice@example.com')
    assert result is user


def test_user_service_register_user_rejects_empty_or_short_username(db_mock):
    """register_user: raises ValueError on empty or too-short usernames"""
    svc = UserService(db_mock)

    with pytest.raises(ValueError):
        svc.register_user('', 'a@b.com')
    with pytest.raises(ValueError):
        svc.register_user('  ', 'a@b.com')
    with pytest.raises(ValueError):
        svc.register_user('ab', 'a@b.com')


def test_user_service_register_user_rejects_duplicate_username(db_mock):
    """register_user: raises if username already exists"""
    svc = UserService(db_mock)
    db_mock.get_user_by_username.return_value = User(id=1, username='alice', email='a@b.com')

    with pytest.raises(ValueError):
        svc.register_user('alice', 'alice@example.com')


def test_user_service_register_user_invalid_email_after_creation(db_mock):
    """register_user: invalid email on created user -> raises ValueError"""
    svc = UserService(db_mock)
    # add_user returns a User with invalid email format validator
    bad = User(id=2, username='bob', email='not-an-email')
    db_mock.add_user.return_value = bad

    with pytest.raises(ValueError):
        svc.register_user('bob', 'not-an-email')


def test_user_service_deactivate_user_success_and_missing(db_mock):
    """deactivate_user: returns True when found and sets is_active False; False if missing"""
    svc = UserService(db_mock)
    user = User(id=5, username='carol', email='carol@example.com')

    # Found case
    db_mock.get_user.return_value = user
    assert svc.deactivate_user(5) is True
    assert user.is_active is False

    # Missing case
    db_mock.get_user.return_value = None
    assert svc.deactivate_user(404) is False


# ------------------------ TaskService tests ------------------------

def test_task_service_create_task_validates_and_calls_db(db_mock):
    """create_task: trims title/description, validates title and length, delegates to db"""
    svc = TaskService(db_mock)
    task = Task(id=1, title='Title', description='Desc')
    db_mock.add_task.return_value = task

    result = svc.create_task('  Title  ', '  Desc  ')

    db_mock.add_task.assert_called_once_with('Title', 'Desc')
    assert result is task


def test_task_service_create_task_rejects_empty_or_too_long_title(db_mock):
    """create_task: reject empty and too-long title"""
    svc = TaskService(db_mock)

    with pytest.raises(ValueError):
        svc.create_task('', 'd')
    with pytest.raises(ValueError):
        svc.create_task('   ', 'd')
    long_title = 'x' * 101
    with pytest.raises(ValueError):
        svc.create_task(long_title, 'd')


def test_task_service_complete_task_success_and_missing(db_mock):
    """complete_task: marks as completed if exists; returns False if missing"""
    svc = TaskService(db_mock)
    task = Task(id=10, title='T', description='D')

    # Success path
    db_mock.get_task.return_value = task
    assert svc.complete_task(10) is True
    assert task.completed is True  # mark_completed called on object

    # Missing path
    db_mock.get_task.return_value = None
    assert svc.complete_task(10) is False


def test_task_service_get_pending_and_completed_filters(db_mock):
    """get_pending_tasks/get_completed_tasks: filter based on completed flag"""
    svc = TaskService(db_mock)
    t1 = Task(id=1, title='A', description='D')
    t2 = Task(id=2, title='B', description='D'); t2.mark_completed()
    t3 = Task(id=3, title='C', description='D')

    db_mock.get_all_tasks.return_value = [t1, t2, t3]

    pending = svc.get_pending_tasks()
    completed = svc.get_completed_tasks()

    assert pending == [t1, t3]
    assert completed == [t2]


def test_task_service_delete_task_delegates_and_returns(db_mock):
    """delete_task: delegates to db.delete_task and returns its result"""
    svc = TaskService(db_mock)

    db_mock.delete_task.return_value = True
    assert svc.delete_task(1) is True
    db_mock.delete_task.assert_called_with(1)

    db_mock.delete_task.return_value = False
    assert svc.delete_task(2) is False
