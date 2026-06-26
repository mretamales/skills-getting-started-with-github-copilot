from fastapi.testclient import TestClient

from src import app as app_module

client = TestClient(app_module.app)


def test_root_redirects_to_static_index():
    # Arrange
    expected_location = "/static/index.html"

    # Act
    response = client.get("/")

    # Assert
    assert response.status_code == 200
    assert response.url.path == expected_location


def test_get_activities_returns_all_activities():
    # Arrange
    activity_name = "Chess Club"

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    assert activity_name in response.json()
    assert response.json()[activity_name]["description"] == "Learn strategies and compete in chess tournaments"


def test_signup_for_activity_success():
    # Arrange
    activity_name = "Chess Club"
    new_participant = "newstudent@mergington.edu"
    assert new_participant not in app_module.activities[activity_name]["participants"]

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": new_participant})

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {new_participant} for {activity_name}"
    assert new_participant in app_module.activities[activity_name]["participants"]


def test_signup_for_nonexistent_activity_returns_404():
    # Arrange
    activity_name = "Nonexistent Club"
    new_participant = "newstudent@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": new_participant})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_duplicate_signup_returns_400():
    # Arrange
    activity_name = "Chess Club"
    existing_participant = app_module.activities[activity_name]["participants"][0]

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": existing_participant})

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student is already signed up for this activity"


def test_unregister_from_activity_success():
    # Arrange
    activity_name = "Chess Club"
    participant = app_module.activities[activity_name]["participants"][0]
    assert participant in app_module.activities[activity_name]["participants"]

    # Act
    response = client.delete(f"/activities/{activity_name}/participants", params={"email": participant})

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Unregistered {participant} from {activity_name}"
    assert participant not in app_module.activities[activity_name]["participants"]


def test_unregister_missing_participant_returns_404():
    # Arrange
    activity_name = "Chess Club"
    missing_participant = "missing@mergington.edu"
    assert missing_participant not in app_module.activities[activity_name]["participants"]

    # Act
    response = client.delete(f"/activities/{activity_name}/participants", params={"email": missing_participant})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found in this activity"
