import pytest
import uuid

import os

from dotenv import load_dotenv

from api.auth_api import AuthAPI

from api.notes_api import NotesAPI


load_dotenv()


def get_token():

    auth_api = AuthAPI()

    response = auth_api.login(
        os.getenv("EMAIL"),
        os.getenv("PASSWORD")
    )

    assert response.status_code == 200

    token = response.json()["data"]["token"]

    return token

@pytest.mark.api
def test_get_notes():

    token = get_token()

    notes_api = NotesAPI(token)

    response = notes_api.get_notes()

    assert response.status_code == 200

    assert isinstance(
        response.json()["data"],
        list
    )

@pytest.mark.api
def test_create_note_api():

    token = get_token()

    notes_api = NotesAPI(token)

    unique_id = str(uuid.uuid4())[:8]

    title = f"API Note {unique_id}"

    response = notes_api.create_note(
        title,
        "Created from API"
    )

    assert response.status_code == 200

    response_data = response.json()

    assert (
        response_data["data"]["title"]
        == title
    )


@pytest.mark.api
def test_delete_note_api():

    token = get_token()

    notes_api = NotesAPI(token)

    unique_id = str(uuid.uuid4())[:8]

    title = f"Delete API {unique_id}"

    create_response = notes_api.create_note(
        title,
        "Delete test"
    )

    note_id = (
        create_response.json()["data"]["id"]
    )

    delete_response = (
        notes_api.delete_note(note_id)
    )

    assert delete_response.status_code == 200

@pytest.mark.api
def test_invalid_login_api():

    auth_api = AuthAPI()

    response = auth_api.login(
        "wrong@gmail.com",
        "wrongpassword"
    )

    assert response.status_code == 401

@pytest.mark.api
def test_create_note_without_token():

    import requests

    from config.environment import config

    endpoint = f"{config.api_url}/notes"

    payload = {
        "title": "Unauthorized",
        "description": "Should fail"
    }

    response = requests.post(
        endpoint,
        json=payload
    )

    assert response.status_code in [401, 403]

@pytest.mark.api
def test_create_note_without_title_api():

    token = get_token()

    notes_api = NotesAPI(token)

    response = notes_api.create_note(
        "",
        "Missing title"
    )

    assert response.status_code == 400

@pytest.mark.api
def test_get_notes_response_time():

    token = get_token()

    notes_api = NotesAPI(token)

    response = notes_api.get_notes()

    assert response.elapsed.total_seconds() < 3