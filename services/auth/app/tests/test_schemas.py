import pytest

from app.schemas import UserCreate, UserResponse

def test_user_create_schema():
    user_data = UserCreate(email="alice@example.com", password="secret123", full_name="Alice")
    assert user_data.email == "alice@example.com"
    assert user_data.password == "secret123"
    assert user_data.full_name == "Alice"
    
def test_user_create_schema_invalid_email():
    with pytest.raises(ValueError):
        UserCreate(email="invalid-email", password="secret123", full_name="Alice")
        
def test_user_create_schema_empty_password():
    with pytest.raises(TypeError):
        UserCreate(email="alice@example.com", password="", full_name="Alice").validate()

def test_user_create_schema_missing_fields():
    with pytest.raises(ValueError):
        UserCreate(email="alice@example.com", password="secret123")
        
def test_user_create_schema_empty_full_name():
    with pytest.raises(TypeError):
        UserCreate(email="alice@example.com", password="secret123", full_name="").validate()
        
def test_response_model():
    from datetime import datetime
    from uuid import uuid4
    
    user_response = UserResponse(
        id=uuid4(),
        email="alice@example.com",
        full_name="Alice",
        created_at=datetime.now()
    )
    
    assert user_response.email == "alice@example.com"
    assert user_response.full_name == "Alice"
    assert user_response.is_active == True, "User should be active by default"
    assert isinstance(user_response.created_at, datetime), "created_at should be a datetime instance"

def test_token_data_model():
    from app.schemas import TokenData
    
    token_data = TokenData(sub="user123")
    assert token_data.sub == "user123", "TokenData should store the subject correctly"
    
    token_data_empty = TokenData()
    assert token_data_empty.sub is None, "TokenData sub should be None by default"