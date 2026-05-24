from services.github_user_api import GitHubUserAPI


def test_should_get_existing_github_user_successfully():

    # Arrange
    username = "octocat"
    client = GitHubUserAPI()

    # Act
    response = client.get_user(username)
    body = response.json()

    # Assert 1
    assert response.status_code == 200

    # Assert 2
    assert body["login"] == username

    # Assert 3
    assert "id" in body

    # Assert 4
    assert body["type"] == "User"
