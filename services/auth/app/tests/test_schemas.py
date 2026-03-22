import pytest
from datetime import datetime
from uuid import uuid4
from pydantic import ValidationError

from app.schemas import UserCreate, UserResponse, TokenData


class TestUserCreate:
    """Testes para o schema UserCreate."""

    def test_user_create_schema(self):
        """Testa criação válida de usuário."""
        user_data = UserCreate(
            email="alice@example.com",
            password="secret123",
            full_name="Alice"
        )
        assert user_data.email == "alice@example.com"
        assert user_data.password == "secret123"
        assert user_data.full_name == "Alice"

    def test_user_create_schema_invalid_email(self):
        """Testa que email inválido é rejeitado."""
        with pytest.raises(ValidationError):
            UserCreate(
                email="invalid-email",
                password="secret123",
                full_name="Alice"
            )

    def test_user_create_schema_empty_password(self):
        with pytest.raises(ValidationError):
            UserCreate(
                email="alice@example.com",
                password="",
                full_name="Alice"
            )
        

    def test_user_create_schema_missing_fields(self):
        """Testa que campos obrigatórios são validados."""
        with pytest.raises(ValidationError):
            UserCreate(
                email="alice@example.com",
                password="secret123"
            )

    def test_user_create_schema_empty_full_name(self):
        with pytest.raises(ValidationError):
            UserCreate(
                email="alice@example.com",
                password="secret123",
                full_name=""
            )


class TestUserResponse:
    """Testes para o schema UserResponse."""

    def test_response_model(self):
        """Testa criação válida de resposta de usuário."""
        user_response = UserResponse(
            id=uuid4(),
            email="alice@example.com",
            full_name="Alice",
            created_at=datetime.now()
        )
        assert user_response.email == "alice@example.com"
        assert user_response.full_name == "Alice"
        assert user_response.is_active is True
        assert isinstance(user_response.created_at, datetime)

    def test_response_model_all_fields(self):
        """Testa que todos os campos são incluídos na resposta."""
        user_id = uuid4()
        now = datetime.now()
        user_response = UserResponse(
            id=user_id,
            email="bob@example.com",
            full_name="Bob",
            created_at=now,
            is_active=False
        )
        assert user_response.id == user_id
        assert user_response.email == "bob@example.com"
        assert user_response.full_name == "Bob"
        assert user_response.created_at == now
        assert user_response.is_active is False


class TestTokenData:
    """Testes para o schema TokenData."""

    def test_token_data_model(self):
        token_data = TokenData(sub="user123")
        assert token_data.sub == "user123"

    def test_token_data_model_default_sub(self):
        """Testa que sub tem valor padrão None."""
        token_data = TokenData()
        assert token_data.sub is None

