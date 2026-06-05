import uuid
import pytest
import time
from data.issue_data import CREATE_ISSUE_PAYLOAD
from data.label_data import CREATE_LABEL_PAYLOAD, LABEL_NAME, LABEL_UPDATED_NAME
from data.pull_request_data import get_dynamic_label_name
from utils.logger import logger


_NEUTRAL_PROFILE = {
    "bio": "",
    "location": "",
    "company": "",
    "hireable": False,
}

_NEUTRAL_PR_TITLE = "PR de prueba para automatización"
_NEUTRAL_PR_BODY = "Descripción inicial del PR de prueba."

PR_NUMBER = 1


@pytest.fixture
def issue(github_api):
    response = github_api.create_issue(CREATE_ISSUE_PAYLOAD)
    issue_number = response.json()["number"]
    yield issue_number
    github_api.close_issue(issue_number)


@pytest.fixture
def closed_issue(github_api):
    response = github_api.create_issue(CREATE_ISSUE_PAYLOAD)
    issue_number = response.json()["number"]
    github_api.close_issue(issue_number)
    yield issue_number
    github_api.close_issue(issue_number)


@pytest.fixture
def label(labels_api):
    labels_api.delete_label(LABEL_NAME)
    labels_api.delete_label(LABEL_UPDATED_NAME)
    time.sleep(1)

    response = labels_api.create_label(CREATE_LABEL_PAYLOAD)
    if response.status_code != 201:
        pytest.fail(f"Fallo en creación de etiqueta: {response.text}")

    label_name = response.json().get("name")
    yield label_name

    labels_api.delete_label(LABEL_NAME)
    labels_api.delete_label(LABEL_UPDATED_NAME)


@pytest.fixture
def repository(repo_api):
    repo_name = f"mi-repo-de-prueba-{uuid.uuid4().hex[:8]}"
    repo_api.delete_repo(repo_name)
    yield repo_name
    repo_api.delete_repo(repo_name)


@pytest.fixture
def profile_restore(github_user_api):
    original = github_user_api.get_authenticated_user().json()
    original_bio = original.get("bio") or ""
    original_location = original.get("location") or ""
    original_company = original.get("company") or ""
    original_hireable = original.get("hireable") or False
    logger.info(
        f"[profile_restore] Estado original capturado: bio={original_bio!r}, "
        f"company={original_company!r}, location={original_location!r}, "
        f"hireable={original_hireable}"
    )
    logger.info("[profile_restore] Limpiando perfil estado neutral antes del test")
    github_user_api.update_profile(_NEUTRAL_PROFILE)
    yield
    restore_payload = {
        "bio": original_bio,
        "location": original_location,
        "company": original_company,
        "hireable": original_hireable,
    }
    logger.info(f"[profile_restore] Restaurando perfil a: {restore_payload}")
    github_user_api.update_profile(restore_payload)


@pytest.fixture
def pr_state(pr_api):
    response = pr_api.get_pull_request(PR_NUMBER)
    original = response.json()
    original_title = original.get("title") or _NEUTRAL_PR_TITLE
    original_body = original.get("body") or _NEUTRAL_PR_BODY
    original_state = original.get("state", "open")
    logger.info(
        f"[pr_state] Estado original capturado: "
        f"title={original_title!r}, state={original_state}"
    )
    logger.info("[pr_state] Limpiando PR a estado neutral antes del test")
    clean_payload = {"title": _NEUTRAL_PR_TITLE, "body": _NEUTRAL_PR_BODY}
    if original_state == "closed":
        pr_api.update_pull_request(PR_NUMBER, {"state": "open"})
    pr_api.update_pull_request(PR_NUMBER, clean_payload)
    yield {
        "title": original_title,
        "body": original_body,
        "state": original_state,
    }
    restore_payload = {"title": original_title, "body": original_body}
    current = pr_api.get_pull_request(PR_NUMBER).json()
    if current.get("state") == "closed" and original_state == "open":
        restore_payload["state"] = "open"
    elif original_state == "closed":
        restore_payload["state"] = "closed"
    logger.info(f"[pr_state] Restaurando PR a: {restore_payload}")
    pr_api.update_pull_request(PR_NUMBER, restore_payload)


@pytest.fixture
def pr_temp_label(pr_api):
    unique_suffix = f"{uuid.uuid4().hex[:6]}"
    label_name = f"{get_dynamic_label_name()}-{unique_suffix}"
    pr_api.create_label(label_name, color="0075ca")
    yield label_name
    current_labels_resp = pr_api.get_labels(PR_NUMBER)
    if current_labels_resp.status_code == 200:
        labels = [
            lbl["name"]
            for lbl in current_labels_resp.json()
            if lbl["name"] != label_name
        ]
        pr_api.set_labels(PR_NUMBER, labels)
    pr_api.delete_label(label_name)
