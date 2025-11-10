import os
import sys
sys.path.insert(0, '/home/mgarcia/Desktop/Otros/IA/CURSO UPV MCP/testing-multiagent/sample_project')
sys.path.insert(0, '/home/mgarcia/Desktop/Otros/IA/CURSO UPV MCP/testing-multiagent')

import pytest
from sample_project.database import Database
from sample_project.services import UserService


@pytest.fixture
def db():
    return Database()


@pytest.fixture
def user_service(db):
    return UserService(db)


def test_register_user_success_and_duplicate_username_blocked(user_service, db):
    """Register a user; attempting duplicate username raises ValueError and does not create a second user."""
    u = user_service.register_user('alice', 'alice@example.com')
    assert u.id == 1
    # Persisted in DB
    assert db.get_user(1) is not None
    # Duplicate attempt
    with pytest.raises(ValueError):
        user_service.register_user('alice', 'alice@other.com')
    # Still only one user in DB
    # Database doesn't expose list_users; we can check by querying by ids and username
    assert db.get_user(2) is None
    assert db.get_user_by_username('alice').id == 1


def test_register_user_invalid_email_raises_and_user_is_still_persisted_current_impl(user_service, db):
    """Current implementation adds user then validates email, so invalid email raises AFTER persistence.
    This test documents the behavior: user remains in DB despite error.
    """
    with pytest.raises(ValueError):
        user_service.register_user('bob', 'invalid-email')
    # User persisted with id 1 due to current implementation order
    u = db.get_user(1)
    assert u is not None
    assert u.username == 'bob'


def test_deactivate_user_flow_persists(user_service, db):
    """Register a user, deactivate via service, verify is_active becomes False and persists."""
    u = user_service.register_user('carol', 'carol@example.com')
    assert db.get_user(u.id).is_active is True

    ok = user_service.deactivate_user(u.id)
    assert ok is True
    assert db.get_user(u.id).is_active is False


def test_user_ids_increment(user_service, db):
    u1 = user_service.register_user('dave', 'dave@example.com')
    u2 = user_service.register_user('erin', 'erin@example.com')
    assert u1.id == 1
    assert u2.id == 2
