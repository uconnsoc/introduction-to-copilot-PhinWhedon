"""Pytest configuration and shared fixtures."""

import pytest
from fastapi.testclient import TestClient
import sys
from pathlib import Path

# Add src directory to path so we can import app
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from app import app, activities as original_activities


@pytest.fixture
def client():
    """Provide a TestClient for making requests to the app."""
    return TestClient(app)


@pytest.fixture
def reset_activities():
    """Reset activities to initial state before each test."""
    # Store original state
    initial_state = {
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
        },
        "Gym Class": {
            "description": "Physical education and sports activities",
            "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
            "max_participants": 30,
            "participants": ["john@mergington.edu", "olivia@mergington.edu"]
        },
        "Basketball": {
            "description": "Competitive basketball team and games",
            "schedule": "Mondays and Thursdays, 4:00 PM - 5:30 PM",
            "max_participants": 15,
            "participants": []
        },
        "Tennis Club": {
            "description": "Learn tennis skills and compete in matches",
            "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
            "max_participants": 10,
            "participants": []
        },
        "Drama Club": {
            "description": "Perform in school plays and theatrical productions",
            "schedule": "Tuesdays, 3:30 PM - 5:00 PM",
            "max_participants": 20,
            "participants": []
        },
        "Photography Club": {
            "description": "Learn photography techniques and exhibit your work",
            "schedule": "Thursdays, 4:00 PM - 5:00 PM",
            "max_participants": 15,
            "participants": []
        },
        "Debate Team": {
            "description": "Develop debate skills and compete in tournaments",
            "schedule": "Mondays and Wednesdays, 4:00 PM - 5:30 PM",
            "max_participants": 12,
            "participants": []
        },
        "Science Club": {
            "description": "Explore scientific concepts through experiments and projects",
            "schedule": "Fridays, 3:30 PM - 4:30 PM",
            "max_participants": 18,
            "participants": []
        }
    }
    
    # Clear and populate activities dict
    original_activities.clear()
    original_activities.update(initial_state)
    
    yield
    
    # Reset again after test
    original_activities.clear()
    original_activities.update(initial_state)
