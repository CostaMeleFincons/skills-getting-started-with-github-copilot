def test_root_redirects_to_static_index(client):
    # Arrange
    target_url = "/"

    # Act
    response = client.get(target_url, follow_redirects=False)

    # Assert
    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"
