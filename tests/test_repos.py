from src.users.repos.repos_users import UserDBRepository
from src.users.repos.repos_roles import RoleDBRepository
from src.users.schemas import UserCreate, RoleCreate, UserUpdate


def test_create_user(db_session):
    role_repo = RoleDBRepository(db_session)
    role = RoleCreate(name="admin")
    db_role = role_repo.create_role(role)
    user_repo = UserDBRepository(db_session)
    user = UserCreate(name="Test User", email="test@example.com", password="password", role_id=1)
    db_user = user_repo.create_user(user)
    assert db_user.id is not None
    assert db_user.name == "Test User"
    assert db_user.email == "test@example.com"


def test_get_users(db_session):
    role_repo = RoleDBRepository(db_session)
    role = RoleCreate(name="admin")
    db_role = role_repo.create_role(role)
    user_repo = UserDBRepository(db_session)
    user = UserCreate(name="Test User", email="test@example.com", password="password", role_id=1)
    user_repo.create_user(user)
    users = user_repo.get_users()
    assert len(users) == 1


def test_get_user(db_session):
    role_repo = RoleDBRepository(db_session)
    role = RoleCreate(name="admin")
    db_role = role_repo.create_role(role)
    user_repo = UserDBRepository(db_session)
    user = UserCreate(name="Test User", email="test_get_user@example.com", password="password", role_id=1)
    db_user = user_repo.create_user(user)
    db_user = user_repo.get_user(db_user.id)
    assert db_user is not None
    assert db_user.email == "test_get_user@example.com"


def test_update_user(db_session):
    role_repo = RoleDBRepository(db_session)
    role = RoleCreate(name="admin")
    db_role = role_repo.create_role(role)
    user_repo = UserDBRepository(db_session)
    user = UserCreate(name="Test User", email="test_edit@example.com", password="password", role_id=1)
    db_user = user_repo.create_user(user)
    user = UserUpdate(id=db_user.id, name="Edited User")
    db_user = user_repo.update_user(user)
    assert db_user is not None
    assert db_user.name == "Edited User"


def test_delete_user(db_session):
    role_repo = RoleDBRepository(db_session)
    role = RoleCreate(name="admin")
    db_role = role_repo.create_role(role)
    user_repo = UserDBRepository(db_session)
    user = UserCreate(name="Test User", email="test_deleted@example.com", password="password", role_id=1)
    db_user = user_repo.create_user(user)
    user_repo.delete_user(db_user.id)
    users = user_repo.get_users()
    assert len(users) == 0


def test_get_user_by_email(db_session):
    role_repo = RoleDBRepository(db_session)
    role = RoleCreate(name="admin")
    db_role = role_repo.create_role(role)
    user_repo = UserDBRepository(db_session)
    user = UserCreate(name="Test User", email="test@example.com", password="password", role_id=1)
    user_repo.create_user(user)
    db_user = user_repo.get_user_by_email("test@example.com")
    assert db_user is not None
    assert db_user.email == "test@example.com"
