
import os
import sys
# Import path fix provided by supervisor
sys.path.insert(0, '/home/mgarcia/Desktop/Otros/IA/CURSO UPV MCP/testing-multiagent/sample_project')
# Additional parent path to import the package (required for relative imports in modules)
sys.path.insert(0, '/home/mgarcia/Desktop/Otros/IA/CURSO UPV MCP/testing-multiagent')

import pytest

from sample_project.database import Database
from sample_project.models import Task, User


def test_database_initial_state_empty():
    """Database starts with empty users and tasks lists"""
    # Arrange
    db = Database()

    # Assert
    assert db.tasks == []
    assert db.users == []


def test_add_get_and_list_tasks_crud_basic():
    """Add a task, retrieve by id, and list all tasks returns it"""
    db = Database()

    # Act
    task = db.add_task('Title', 'Desc')

    # Assert creation
    assert isinstance(task, Task)
    assert task.id == 1
    assert task.title == 'Title'

    # Retrieve by id
    fetched = db.get_task(task.id)
    assert fetched is task

    # List all tasks returns a copy containing the task
    tasks = db.get_all_tasks()
    assert task in tasks
    assert tasks is not db.tasks  # should be a shallow copy


def test_get_all_tasks_returns_copy_not_affecting_internal_store():
    """Modifying returned tasks list should not change internal storage"""
    db = Database()
    t1 = db.add_task('T1', 'D1')
    t2 = db.add_task('T2', 'D2')

    tasks = db.get_all_tasks()
    tasks.clear()

    # Internal store remains intact
    assert len(db.tasks) == 2
    assert db.tasks[0] == t1 and db.tasks[1] == t2


def test_delete_task_success_and_failure():
    """Delete an existing task returns True; non-existent returns False"""
    db = Database()
    task = db.add_task('Title', 'Desc')

    assert db.delete_task(task.id) is True
    # Already deleted
    assert db.delete_task(task.id) is False
    # Non-existent id
    assert db.delete_task(9999) is False


def test_get_task_nonexistent_returns_none():
    """Getting non-existent task id returns None"""
    db = Database()
    assert db.get_task(42) is None


def test_add_user_and_get_by_id_and_username_and_unique_ids():
    """Add users, retrieve by id/username, and verify unique/incrementing ids"""
    db = Database()

    u1 = db.add_user('alice', 'alice@example.com')
    u2 = db.add_user('bob', 'bob@example.com')

    assert isinstance(u1, User)
    assert isinstance(u2, User)
    assert u1.id == 1
    assert u2.id == 2

    # Get by id
    assert db.get_user(u1.id) is u1
    assert db.get_user(u2.id) is u2
    assert db.get_user(9999) is None

    # Get by username
    assert db.get_user_by_username('alice') is u1
    assert db.get_user_by_username('missing') is None


def test_update_and_delete_user_methods_missing_are_skipped():
    """If update_user/delete_user/list_users not implemented, skip with reason"""
    db = Database()

    # update_user
    if not hasattr(db, 'update_user'):
        pytest.skip('Database.update_user not implemented in this version')
    # delete_user
    if not hasattr(db, 'delete_user'):
        pytest.skip('Database.delete_user not implemented in this version')
    # list_users
    if not hasattr(db, 'get_all_users') and not hasattr(db, 'list_users'):
        pytest.skip('Database.list/get_all users not implemented in this version')

    # The rest of this test will not execute due to skip above in this project
