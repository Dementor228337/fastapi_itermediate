from sqlalchemy import select
from sqlalchemy.orm import Session
from starlette.testclient import TestClient

from src.infrastructure.database.models.user import User

def test_user_register(client: TestClient, db_session: Session):
    response = client.post("v1/api/users/register", json={
        "username": "test_user",
        "password": "secure-password",
        "email": "test@examplpe.com",
    })
    assert response.status_code == 200
    user = db_session.execute(select(User).filter(User.username == "test_user")).scalars().first()
    assert user is not None