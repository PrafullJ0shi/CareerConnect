"""Tests covering the seven CareerConnect synopsis cases."""

import pytest

from app import create_app


@pytest.fixture
def client(tmp_path):
    app = create_app(
        {
            "TESTING": True,
            "SECRET_KEY": "test-secret-key",
            "DATABASE": str(tmp_path / "test.db"),
        }
    )
    with app.test_client() as test_client:
        yield test_client


def test_home_page_displays_available_job_listings(client):
    response = client.get("/")
    assert response.status_code == 200
    body = response.get_data(as_text=True)
    assert "CareerConnect" in body
    assert "Junior Python Developer" in body
    assert "Nimbus Labs" in body
    assert "QA Tester" in body


def test_keyword_search_returns_matching_jobs(client):
    response = client.get("/?q=Dehradun")
    assert response.status_code == 200
    body = response.get_data(as_text=True)
    assert "Junior Python Developer" in body
    assert "Nimbus Labs" in body
    assert "Marketing Coordinator" not in body


def test_no_match_search_displays_no_results_message(client):
    response = client.get("/?q=zzzxnotajob999")
    assert response.status_code == 200
    body = response.get_data(as_text=True)
    assert "No jobs matched" in body
    assert "Junior Python Developer" not in body


def test_job_details_page_displays_selected_job(client):
    response = client.get("/job/1")
    assert response.status_code == 200
    body = response.get_data(as_text=True)
    assert "Junior Python Developer" in body
    assert "Nimbus Labs" in body
    assert "Dehradun" in body
    assert "hiring@nimbuslabs.example" in body
    assert 'href="mailto:hiring@nimbuslabs.example"' in body


def test_invalid_job_id_returns_not_found_page(client):
    response = client.get("/job/99999")
    assert response.status_code == 404
    body = response.get_data(as_text=True)
    assert "could not be found" in body or "not found" in body.lower()


def test_job_posting_stores_and_displays_new_job(client):
    payload = {
        "title": "Quality Engineer",
        "company": "Lumen Field",
        "location": "Chennai",
        "job_type": "Full-time",
        "description": "Write test plans and verify product releases for a growing software team.",
        "email": "hiring@lumenfield.example",
    }
    response = client.post("/post", data=payload, follow_redirects=True)
    assert response.status_code == 200
    body = response.get_data(as_text=True)
    assert "posted successfully" in body
    assert "Quality Engineer" in body
    assert "Lumen Field" in body
    assert "Chennai" in body


def test_empty_form_shows_validation_message(client):
    response = client.post(
        "/post",
        data={
            "title": "",
            "company": "",
            "location": "",
            "job_type": "",
            "description": "",
            "email": "",
        },
    )
    assert response.status_code == 200
    body = response.get_data(as_text=True)
    assert "Please fill in all required fields." in body
    assert "posted successfully" not in body
