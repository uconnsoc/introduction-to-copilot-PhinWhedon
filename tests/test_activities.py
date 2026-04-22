"""Tests for the Activities API endpoints using AAA (Arrange-Act-Assert) pattern."""

import pytest


class TestGetActivities:
    """Tests for GET /activities endpoint."""

    def test_get_activities_returns_all_activities(self, client, reset_activities):
        """Test that GET /activities returns all activities with correct data."""
        # Arrange
        expected_activities = [
            "Chess Club",
            "Programming Class",
            "Gym Class",
            "Basketball",
            "Tennis Club",
            "Drama Club",
            "Photography Club",
            "Debate Team",
            "Science Club"
        ]

        # Act
        response = client.get("/activities")
        data = response.json()

        # Assert
        assert response.status_code == 200
        assert isinstance(data, dict)
        assert set(data.keys()) == set(expected_activities)
        
        # Verify structure of an activity
        chess_club = data["Chess Club"]
        assert "description" in chess_club
        assert "schedule" in chess_club
        assert "max_participants" in chess_club
        assert "participants" in chess_club
        assert isinstance(chess_club["participants"], list)

    def test_get_activities_contains_participant_data(self, client, reset_activities):
        """Test that activities show current participant data."""
        # Arrange
        expected_chess_participants = ["michael@mergington.edu", "daniel@mergington.edu"]

        # Act
        response = client.get("/activities")
        data = response.json()

        # Assert
        assert response.status_code == 200
        assert data["Chess Club"]["participants"] == expected_chess_participants


class TestSignupForActivity:
    """Tests for POST /activities/{activity_name}/signup endpoint."""

    def test_signup_new_student_successful(self, client, reset_activities):
        """Test that a new student can successfully sign up for an activity."""
        # Arrange
        activity_name = "Basketball"
        student_email = "newstudent@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup?email={student_email}"
        )
        data = response.json()

        # Assert
        assert response.status_code == 200
        assert "Signed up" in data["message"]
        assert student_email in data["message"]
        assert activity_name in data["message"]

    def test_signup_adds_participant_to_activity(self, client, reset_activities):
        """Test that signup actually adds the participant to the activity."""
        # Arrange
        activity_name = "Basketball"
        student_email = "newstudent@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup?email={student_email}"
        )
        
        # Get updated activities
        activities_response = client.get("/activities")
        activities_data = activities_response.json()

        # Assert
        assert response.status_code == 200
        assert student_email in activities_data[activity_name]["participants"]

    def test_signup_duplicate_student_prevented(self, client, reset_activities):
        """Test that a student cannot sign up twice for the same activity."""
        # Arrange
        activity_name = "Chess Club"
        student_email = "michael@mergington.edu"  # Already signed up

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup?email={student_email}"
        )
        data = response.json()

        # Assert
        assert response.status_code == 400
        assert "already signed up" in data["detail"]

    def test_signup_to_nonexistent_activity_returns_404(self, client, reset_activities):
        """Test that signing up for a non-existent activity returns 404."""
        # Arrange
        activity_name = "Nonexistent Activity"
        student_email = "student@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup?email={student_email}"
        )
        data = response.json()

        # Assert
        assert response.status_code == 404
        assert "not found" in data["detail"]

    def test_signup_with_url_encoded_activity_name(self, client, reset_activities):
        """Test that signup works with URL-encoded activity names."""
        # Arrange
        activity_name = "Programming Class"
        student_email = "newstudent@mergington.edu"
        encoded_name = "Programming%20Class"

        # Act
        response = client.post(
            f"/activities/{encoded_name}/signup?email={student_email}"
        )

        # Assert
        assert response.status_code == 200
        
        # Verify student was added
        activities_response = client.get("/activities")
        activities_data = activities_response.json()
        assert student_email in activities_data[activity_name]["participants"]


class TestUnregisterFromActivity:
    """Tests for DELETE /activities/{activity_name}/unregister endpoint."""

    def test_unregister_existing_participant_successful(self, client, reset_activities):
        """Test that an existing participant can successfully unregister."""
        # Arrange
        activity_name = "Chess Club"
        student_email = "michael@mergington.edu"

        # Act
        response = client.delete(
            f"/activities/{activity_name}/unregister?email={student_email}"
        )
        data = response.json()

        # Assert
        assert response.status_code == 200
        assert "Unregistered" in data["message"]
        assert student_email in data["message"]

    def test_unregister_removes_participant_from_activity(self, client, reset_activities):
        """Test that unregister actually removes the participant from the activity."""
        # Arrange
        activity_name = "Chess Club"
        student_email = "michael@mergington.edu"

        # Act
        response = client.delete(
            f"/activities/{activity_name}/unregister?email={student_email}"
        )
        
        # Get updated activities
        activities_response = client.get("/activities")
        activities_data = activities_response.json()

        # Assert
        assert response.status_code == 200
        assert student_email not in activities_data[activity_name]["participants"]

    def test_unregister_nonexistent_participant_returns_400(self, client, reset_activities):
        """Test that unregistering a non-existent participant returns 400."""
        # Arrange
        activity_name = "Chess Club"
        student_email = "nonexistent@mergington.edu"

        # Act
        response = client.delete(
            f"/activities/{activity_name}/unregister?email={student_email}"
        )
        data = response.json()

        # Assert
        assert response.status_code == 400
        assert "not registered" in data["detail"]

    def test_unregister_from_nonexistent_activity_returns_404(self, client, reset_activities):
        """Test that unregistering from a non-existent activity returns 404."""
        # Arrange
        activity_name = "Nonexistent Activity"
        student_email = "student@mergington.edu"

        # Act
        response = client.delete(
            f"/activities/{activity_name}/unregister?email={student_email}"
        )
        data = response.json()

        # Assert
        assert response.status_code == 404
        assert "not found" in data["detail"]

    def test_unregister_with_url_encoded_activity_name(self, client, reset_activities):
        """Test that unregister works with URL-encoded activity names."""
        # Arrange
        activity_name = "Programming Class"
        student_email = "emma@mergington.edu"
        encoded_name = "Programming%20Class"

        # Act
        response = client.delete(
            f"/activities/{encoded_name}/unregister?email={student_email}"
        )

        # Assert
        assert response.status_code == 200
        
        # Verify student was removed
        activities_response = client.get("/activities")
        activities_data = activities_response.json()
        assert student_email not in activities_data[activity_name]["participants"]
