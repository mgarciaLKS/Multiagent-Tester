import os
import sys
sys.path.insert(0, '/home/mgarcia/Desktop/Otros/IA/CURSO UPV MCP/testing-multiagent/sample_project')
sys.path.insert(0, '/home/mgarcia/Desktop/Otros/IA/CURSO UPV MCP/testing-multiagent')

import pytest
from sample_project.database import Database
from sample_project.services import TaskService


@pytest.fixture
def db():
    """Provide a fresh in-memory Database per test."""
    return Database()


@pytest.fixture
def task_service(db):
    """TaskService wired to the fresh Database."""
    return TaskService(db)


def test_create_and_complete_task_flow(task_service, db):
    """Create a task, verify it appears in pending, complete it, ensure it moves to completed with timestamp."""
    # Create
    task = task_service.create_task('Buy milk', '2 liters of milk')
    assert task.id == 1
    # Appears in pending
    pending = task_service.get_pending_tasks()
    assert len(pending) == 1 and pending[0].id == task.id and pending[0].completed is False

    # Complete via service
    assert task_service.complete_task(task.id) is True

    # Verify state and timestamp persisted in DB
    t_db = db.get_task(task.id)
    assert t_db.completed is True
    assert t_db.completed_at is not None

    # Now shows in completed and not in pending
    completed = task_service.get_completed_tasks()
    assert len(completed) == 1 and completed[0].id == task.id
    assert task_service.get_pending_tasks() == []


def test_delete_task_flow(task_service, db):
    """Create multiple tasks, delete one, and verify it is removed from DB and service filters."""
    t1 = task_service.create_task('Task 1', 'a')
    t2 = task_service.create_task('Task 2', 'b')
    t3 = task_service.create_task('Task 3', 'c')

    assert [t.id for t in db.get_all_tasks()] == [1, 2, 3]

    # Delete the middle task
    assert task_service.delete_task(t2.id) is True
    assert [t.id for t in db.get_all_tasks()] == [1, 3]

    # Ensure filters reflect deletion
    assert {t.id for t in task_service.get_pending_tasks()} == {1, 3}
    # Complete one of the remaining and validate filters
    task_service.complete_task(t3.id)
    assert {t.id for t in task_service.get_completed_tasks()} == {3}
    assert {t.id for t in task_service.get_pending_tasks()} == {1}


def test_filter_pending_and_completed_across_multiple_tasks(task_service):
    """Create mixed tasks, complete a subset, and assert filtering correctness."""
    tasks = [
        task_service.create_task('A', 'a'),  # id 1
        task_service.create_task('B', 'b'),  # id 2
        task_service.create_task('C', 'c'),  # id 3
        task_service.create_task('D', 'd'),  # id 4
    ]
    # Complete 2 and 4
    assert task_service.complete_task(2) is True
    assert task_service.complete_task(4) is True

    pending = task_service.get_pending_tasks()
    completed = task_service.get_completed_tasks()

    assert {t.id for t in pending} == {1, 3}
    assert {t.id for t in completed} == {2, 4}


def test_create_task_validation_errors(task_service, db):
    """Creating with empty or overly long title raises and does not persist tasks."""
    # Empty title
    with pytest.raises(ValueError):
        task_service.create_task('   ', 'x')
    # Too long title
    with pytest.raises(ValueError):
        task_service.create_task('x' * 101, 'y')

    # Ensure DB still empty
    assert db.get_all_tasks() == []
