import pytest
from datetime import datetime

from server.app import app
from server.models import db, Workout

@pytest.fixture
def client():
    app.config.update(
        TESTING=True,
        SQLALCHEMY_DATABASE_URI="sqlite:///:memory:",
    )

    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.session.remove()
        db.drop_all()

def test_get_workouts(client):
    response = client.get("/workouts")
    assert response.status_code == 200
    assert response.json == []

def test_get_exercises(client):
    response = client.get("/exercises")
    assert response.status_code == 200
    assert response.get_json() == []

def test_get_workout(client):
    with app.app_context():
        workout = Workout(
            name="Morning Workout",
            description="A quick morning routine",
        )
        
        db.session.add(workout)
        db.session.commit()
        Workout_id = workout.id

    response = client.get(f"/workouts/{Workout_id}")
    assert response.status_code == 200
    data = response.get_json()
    assert data["id"] == Workout_id
    assert data["name"] == "Morning Workout"
    assert data["description"] == "A quick morning routine"

def test_get_nonexistent_workout(client):
    response = client.get("/workouts/999")
    assert response.status_code == 404
    assert response.get_json() == {"error": "Workout not found."}

def test_get_nonexistent_exercise(client):
    response = client.get("/exercises/999")
    assert response.status_code == 404
    assert response.get_json() == {"error": "Exercise not found."}