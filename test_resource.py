import pytest
from fastapi.testclient import TestClient
from User_Resource_Access_Manager import app

client = TestClient(app)

# Add parametrized test cases for authentication and accessing resource
@pytest.mark.parametrize("username, password, expected_status_code", [
    ("user1", "password1", 200),      # Valid credentials for user1 (admin)
    ("user2", "password2", 403),      # Valid credentials for user2 (user) but resource is not accessed.
    ("user3", "password", 401), # Nonexistent user
    ("user1", "wrongpassword", 401)   # Wrong password
])
def test_authentication(username, password, expected_status_code):
    response = client.get("/resource", auth=(username, password))
    assert response.status_code == expected_status_code

