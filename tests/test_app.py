import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from app import app, activities


initial_state = {
    name: {**activity, "participants": list(activity["participants"])}
    for name, activity in activities.items()
}


@pytest.fixture(autouse=True)
def reset_activities():
    activities.clear()
    activities.update(
        {
            name: {**activity, "participants": list(activity["participants"])}
            for name, activity in initial_state.items()
        }
    )
    yield


def test_unregister_participant_removes_email_from_activity():
    client = TestClient(app)

    response = client.delete(
        "/activities/Chess Club/participants/michael@mergington.edu"
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Removed michael@mergington.edu from Chess Club"
    assert "michael@mergington.edu" not in activities["Chess Club"]["participants"]
    assert "daniel@mergington.edu" in activities["Chess Club"]["participants"]


def test_unregister_participant_returns_404_when_not_found():
    client = TestClient(app)

    response = client.delete(
        "/activities/Chess Club/participants/unknown@mergington.edu"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found"
