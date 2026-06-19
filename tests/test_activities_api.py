def test_get_activities_returns_expected_structure(client):
    # Arrange
    endpoint = "/activities"

    # Act
    response = client.get(endpoint)

    # Assert
    payload = response.json()
    assert response.status_code == 200
    assert "Chess Club" in payload
    assert "participants" in payload["Chess Club"]
    assert isinstance(payload["Chess Club"]["participants"], list)


def test_signup_adds_participant_to_activity(client):
    # Arrange
    activity_name = "Chess Club"
    new_email = "new.student@mergington.edu"
    endpoint = f"/activities/{activity_name}/signup"

    # Act
    response = client.post(endpoint, params={"email": new_email})

    # Assert
    payload = response.json()
    assert response.status_code == 200
    assert payload["message"] == f"Signed up {new_email} for {activity_name}"

    activity_response = client.get("/activities")
    participants = activity_response.json()[activity_name]["participants"]
    assert new_email in participants


def test_signup_with_unknown_activity_returns_404(client):
    # Arrange
    endpoint = "/activities/Unknown Club/signup"

    # Act
    response = client.post(endpoint, params={"email": "student@mergington.edu"})

    # Assert
    payload = response.json()
    assert response.status_code == 404
    assert payload["detail"] == "Activity not found"


def test_signup_with_duplicate_email_returns_400(client):
    # Arrange
    activity_name = "Chess Club"
    existing_email = "michael@mergington.edu"
    endpoint = f"/activities/{activity_name}/signup"

    # Act
    response = client.post(endpoint, params={"email": existing_email})

    # Assert
    payload = response.json()
    assert response.status_code == 400
    assert payload["detail"] == "Student already signed up for this activity"


def test_unregister_removes_participant_from_activity(client):
    # Arrange
    activity_name = "Music Band"
    existing_email = "ava@mergington.edu"
    endpoint = f"/activities/{activity_name}/participants/{existing_email}"

    # Act
    response = client.delete(endpoint)

    # Assert
    payload = response.json()
    assert response.status_code == 200
    assert payload["message"] == f"Removed {existing_email} from {activity_name}"

    activity_response = client.get("/activities")
    participants = activity_response.json()[activity_name]["participants"]
    assert existing_email not in participants


def test_unregister_with_unknown_activity_returns_404(client):
    # Arrange
    endpoint = "/activities/Unknown Club/participants/student@mergington.edu"

    # Act
    response = client.delete(endpoint)

    # Assert
    payload = response.json()
    assert response.status_code == 404
    assert payload["detail"] == "Activity not found"


def test_unregister_non_participant_returns_404(client):
    # Arrange
    activity_name = "Science Club"
    missing_email = "not.enrolled@mergington.edu"
    endpoint = f"/activities/{activity_name}/participants/{missing_email}"

    # Act
    response = client.delete(endpoint)

    # Assert
    payload = response.json()
    assert response.status_code == 404
    assert payload["detail"] == "Participant not found in this activity"
