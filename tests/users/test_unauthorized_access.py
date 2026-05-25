import pytest
from config.config import TOKEN

def test_hltc17_unauthorized_access(github_user_api):
    # Arrange
    from services.github_user_api import GitHubUserAPI
    
    original_session = github_user_api.session
    invalid_api = GitHubUserAPI()
    
    invalid_api.session.headers.update({"Authorization": "Bearer token_invalido_123"})

    # Act
    response = invalid_api.get_authenticated_user()
    body = response.json()

    # Assert
    assert response.status_code in [401, 403]
    assert "message" in body
    assert body["message"] != ""
    
    
    
    assert "bad credentials" in body["message"].lower()