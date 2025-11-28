import json
import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_update_status_get_not_allowed(client):
    url = "/api/update-status/"
    response = client.get(url)
    assert response.status_code == 405
    assert response.json() == {"error": "Only POST allowed"}


@pytest.mark.django_db
def test_update_status_missing_status(client):
    url = "/api/update-status/"
    response = client.post(
        url,
        data=json.dumps({}),
        content_type="application/json"
    )
    assert response.status_code == 400
    assert response.json() == {"error": "Status is required"}


@pytest.mark.django_db
def test_update_status_success(client):
    url = "/api/update-status/"
    response = client.post(
        url,
        data=json.dumps({"status": "completed"}),
        content_type="application/json"
    )
    assert response.status_code == 200
    assert response.json() == {
        "message": "Status updated successfully",
        "new_status": "completed"
    }
