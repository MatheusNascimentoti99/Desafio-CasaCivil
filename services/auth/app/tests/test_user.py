import pytest

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from app.database import Base
from app.dto.user import UserCreate
from app.services.user import create_user, get_user_by_email, get_users
from app.auth import verify_password


TEST_DB_URL = "sqlite+aiosqlite:///:memory:"


@pytest.fixture(scope="module")
async def engine():
    engine = create_async_engine(TEST_DB_URL, echo=False)
    # create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    await engine.dispose()


@pytest.fixture()
async def db(engine):
    async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        yield session

@pytest.fixture(autouse=True)
def user_data():
    return UserCreate(email="alice@example.com", password="secret123", full_name="Alice")

# @pytest.fixture(autouse=True)
# async def clean_user(db: AsyncSession, user_data):
#     # Clean up any existing user with the same email
#     existing_user = await get_user_by_email(db, user_data.email)
#     if existing_user:
#         await db.delete(existing_user)
#         await db.commit()

@pytest.mark.asyncio
async def test_create(db: AsyncSession, user_data: UserCreate):
    # Create user
    user = await create_user(db, user_data)

    assert user.email == user_data.email, "Email should match"
    assert user.full_name == user_data.full_name, "Full name should match"
    
@pytest.mark.asyncio
async def test_hash_password(db: AsyncSession, user_data: UserCreate):
    # Create user
    user = await create_user(db, user_data)
    assert user.hashed_password != user_data.password, "Hashed password should be different from plain text password"
    assert verify_password(user_data.password, user.hashed_password), "Password should be hashed correctly and verify successfully"

@pytest.mark.asyncio
async def test_fetch_user(db: AsyncSession, user_data: UserCreate):
    # Create user
    user = await create_user(db, user_data)

    # Fetch by email
    fetched = await get_user_by_email(db, user_data.email)
    assert fetched is not None, "Fetched user should not be None"
    assert fetched.email == user.email, "Fetched email should match created user's email"


@pytest.mark.asyncio
async def test_get_users(db: AsyncSession):
    # Ensure at least one user exists from previous test, create another
    user_in = UserCreate(email="bob@example.com", password="pass456", full_name="Bob")
    await create_user(db, user_in)

    users = await get_users(db, skip=0, limit=10)
    assert isinstance(users, list)
    # there should be at least 2 users (alice and bob)
    assert len(users) >= 2
