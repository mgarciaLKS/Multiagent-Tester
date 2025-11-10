import os
import sys
sys.path.insert(0, '/home/mgarcia/Desktop/Otros/IA/CURSO UPV MCP/testing-multiagent/sample_project')
sys.path.insert(0, '/home/mgarcia/Desktop/Otros/IA/CURSO UPV MCP/testing-multiagent')

import pytest
from sample_project.database import Database
from sample_project.services import TaskService, UserService
from sample_project.api import TodoAPI


@pytest.fixture
def api_stack():
    """Construct a fresh full stack (API -> Services -> Database) for each test.
    We override the TodoAPI's internal db and services so all layers share the same Database instance.
    """
    db = Database()
    task_service = TaskService(db)
    user_service = UserService(db)
    api = TodoAPI()
    # Wire API to our shared instances to ensure consistent state across calls
    api.db = db
    api.task_service = task_service
    api.user_service = user_service
    return api, db, task_service, user_service


def test_api_task_lifecycle_end_to_end(api_stack):
    """End-to-end: create task via API, list, complete, and verify completed state.
    Validates data flows API -> Service -> Database and back.
    """
    api, db, *_ = api_stack

    # Create task
    create_resp = api.create_task({'title': 'Buy milk', 'description': '2 liters'})
    assert create_resp['success'] is True
    task_payload = create_resp['task']
    assert task_payload['id'] == 1
    assert task_payload['title'] == 'Buy milk'
    assert 'created_at' in task_payload

    # List all tasks
    list_resp = api.get_tasks()
    assert list_resp['success'] is True
    assert list_resp['count'] == 1
    assert list_resp['tasks'][0]['completed'] is False

    # Complete the task
    complete_resp = api.complete_task(task_payload['id'])
    assert complete_resp['success'] is True

    # List completed via filter and verify
    completed_resp = api.get_tasks({'status': 'completed'})
    assert completed_resp['success'] is True
    assert completed_resp['count'] == 1
    assert completed_resp['tasks'][0]['id'] == task_payload['id']
    assert completed_resp['tasks'][0]['title'] == 'Buy milk'
    # Verify underlying DB shows completion timestamp set
    t = db.get_task(task_payload['id'])
    assert t.completed is True and t.completed_at is not None


def test_api_user_registration_and_deactivation(api_stack):
    """Register user through API, then deactivate through the service (API lacks endpoint).
    Confirms user state change persists in the shared Database and is observable across layers.
    """
    api, db, _, user_service = api_stack

    reg = api.register_user({'username': 'alice', 'email': 'alice@example.com'})
    assert reg['success'] is True
    user_payload = reg['user']
    assert user_payload['username'] == 'alice'
    uid = user_payload['id']
    assert db.get_user(uid) is not None and db.get_user(uid).is_active is True

    # Deactivate via service (no API endpoint provided in implementation)
    ok = user_service.deactivate_user(uid)
    assert ok is True
    assert db.get_user(uid).is_active is False


def test_api_error_handling_for_nonexistent_resources(api_stack):
    """Attempt to act on non-existent task/user and verify API/service responses.
    Ensures error propagation and response shaping are correct.
    """
    api, _, _, user_service = api_stack

    # Non-existent task completion
    comp = api.complete_task(9999)
    assert comp['success'] is False
    assert 'error' in comp and 'not found' in comp['error'].lower()

    # Non-existent task deletion
    dele = api.delete_task(9999)
    assert dele['success'] is False
    assert 'error' in dele and 'not found' in dele['error'].lower()

    # Non-existent user deactivation via service
    assert user_service.deactivate_user(9999) is False


def test_api_create_task_validation_errors_bubble_to_api(api_stack):
    """Invalid task titles should produce API error responses from service-raised ValueErrors."""
    api, *_ = api_stack

    r1 = api.create_task({'title': '   ', 'description': 'x'})
    assert r1['success'] is False
    assert 'cannot be empty' in r1['error'].lower()

    r2 = api.create_task({'title': 'x' * 101, 'description': 'y'})
    assert r2['success'] is False
    assert 'too long' in r2['error'].lower()


def test_api_get_tasks_filters_status(api_stack):
    """Verify API filtering for pending and completed tasks uses Services and Database correctly."""
    api, *_ = api_stack

    api.create_task({'title': 'Task A', 'description': 'a'})
    api.create_task({'title': 'Task B', 'description': 'b'})

    # Complete second task
    api.complete_task(2)

    all_resp = api.get_tasks()
    assert all_resp['success'] is True and all_resp['count'] == 2

    pending_resp = api.get_tasks({'status': 'pending'})
    assert pending_resp['success'] is True and pending_resp['count'] == 1
    assert pending_resp['tasks'][0]['id'] == 1

    completed_resp = api.get_tasks({'status': 'completed'})
    assert completed_resp['success'] is True and completed_resp['count'] == 1
    assert completed_resp['tasks'][0]['id'] == 2
