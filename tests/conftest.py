import pytest
from src.database.session import TestSessionLocal, TestEngine
from src.dependencies import get_db
from src.main import app
from fastapi.testclient import TestClient
from src.users.models import User, Role


@pytest.fixture(scope="session", autouse=True)
def test_db():
    with TestEngine.connect() as connection:
        User.metadata.create_all(bind=connection)
        Role.metadata.create_all(bind=connection)
        yield
        User.metadata.drop_all(bind=connection)
        Role.metadata.drop_all(bind=connection)


@pytest.fixture(scope="function")
def db_session(test_db):
    connection = TestEngine.connect()
    transaction = connection.begin()
    session = TestSessionLocal(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="function")
def client(db_session):
    def _get_test_db():
        yield db_session

    app.dependency_overrides[get_db] = _get_test_db
    yield TestClient(app)
    app.dependency_overrides.clear()
