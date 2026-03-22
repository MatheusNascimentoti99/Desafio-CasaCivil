import pytest
from app.auth import create_access_token, decode_access_token

@pytest.fixture(autouse=True)
def created_token():
    user_id = "test-user-id"
    token = create_access_token(data={"sub": user_id})
    return token

def test_token_generation_and_verification(created_token):
    assert created_token is not None, "Token should be generated successfully"
    assert isinstance(created_token, str), "Generated token should be a string"
    

def test_decode_access_token(created_token):

    assert created_token is not None, "Token should be generated successfully"

    # Decode the token and extract the user ID
    token_data = decode_access_token(created_token)
    assert token_data is not None, "Token should be decoded successfully"
    assert token_data.sub == "test-user-id", "Decoded token subject should match the original user ID"