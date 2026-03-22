import pytest

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete

from app.schemas import UserCreate
from app.models import User
from app.services.user import create_user, get_user_by_email, get_users
from app.auth import verify_password

async def clear_table(session: AsyncSession, table: User) -> None:
    """Clear all users from the users table."""
    stmt = delete(table)
    await session.execute(stmt)
    await session.commit()


@pytest.fixture(autouse=True)
async def each_test(db: AsyncSession):
    """Automatically clear users table after each test."""
    yield
    await clear_table(db, User)
    
@pytest.fixture(autouse=True)
def user_data():
    return UserCreate(email="alice@example.com", password="secret123", full_name="Alice")


@pytest.mark.asyncio
async def test_create(db: AsyncSession, user_data):
    # Create user
    user = await create_user(db, user_data)

    assert user.email == user_data.email, "Email should match"
    assert user.full_name == user_data.full_name, "Full name should match"
    
@pytest.mark.asyncio
async def test_hash_password(db: AsyncSession, user_data):
    # Create user
    user = await create_user(db, user_data)
    assert user.hashed_password != user_data.password, "Hashed password should be different from plain text password"
    assert verify_password(user_data.password, user.hashed_password), "Password should be hashed correctly and verify successfully"

@pytest.mark.asyncio
async def test_fetch_user(db: AsyncSession, user_data):
    # Create user
    user = await create_user(db, user_data)

    # Fetch by email
    fetched = await get_user_by_email(db, user_data.email)
    assert fetched is not None, "Fetched user should not be None"
    assert fetched.email == user.email, "Fetched email should match created user's email"


@pytest.mark.asyncio
async def test_get_users(db: AsyncSession):
    # Create two users
    user_in1 = UserCreate(email="alice2@example.com", password="pass1234", full_name="Alice2")
    user_in2 = UserCreate(email="bob2@example.com", password="pass4567", full_name="Bob2")
    await create_user(db, user_in1)
    await create_user(db, user_in2)

    users = await get_users(db, skip=0, limit=10)
    assert isinstance(users, list)
    # there should be at least 2 users
    assert len(users) == 2


