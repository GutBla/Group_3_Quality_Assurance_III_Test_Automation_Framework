import pytest

from data.label_data import (ASSIGN_LABELS_PAYLOAD, CREATE_LABEL_PAYLOAD,
                             CREATE_LABEL_PAYLOAD_NO_NAME, LABEL_UPDATED_NAME,
                             UPDATE_LABEL_PAYLOAD)
from utils.schema_validator import validate_schema
from utils.schemas import (ASSIGN_LABELS_SCHEMA, LABEL_ERROR_SCHEMA,
                           LABEL_SCHEMA, LIST_LABELS_SCHEMA)


@pytest.mark.functional
@pytest.mark.smoke
def test_should_create_label_successfully(labels_api):
    """HLTC-06: Crear una etiqueta con nombre y color válidos"""

    # Arrange
    labels_api.delete_label(CREATE_LABEL_PAYLOAD["name"])
    payload = CREATE_LABEL_PAYLOAD

    # Act
    response = labels_api.create_label(payload)
    body = response.json()

    # Assert 1 — Status Code
    assert response.status_code == 201

    # Assert 2 — Response Body
    assert body["name"] == payload["name"]
    assert body["color"] == payload["color"]
    assert body["default"] is False

    # Assert 3 — Schema Validation (soft assertion)
    assert validate_schema(body, LABEL_SCHEMA)

    # Assert 4 — Data Integrity via GET
    get_response = labels_api.get_label(payload["name"])
    get_body = get_response.json()

    assert get_response.status_code == 200
    assert get_body["name"] == payload["name"]
    assert get_body["color"] == payload["color"]

    # Cleanup
    labels_api.delete_label(payload["name"])


@pytest.mark.negative
@pytest.mark.regression
def test_should_fail_to_create_label_without_name(labels_api):
    """HLTC-07: Validar error al crear etiqueta sin nombre"""

    # Arrange
    payload = CREATE_LABEL_PAYLOAD_NO_NAME

    # Act
    response = labels_api.create_label(payload)
    body = response.json()

    # Assert 1 — Status Code
    assert response.status_code == 422

    # Assert 2 — Response Body
    assert "message" in body
    assert body["message"] != ""

    # Assert 3 — Schema Validation (soft assertion)
    assert validate_schema(body, LABEL_ERROR_SCHEMA)

    # Assert 4 — Data Integrity (no label was created)
    assert "id" not in body
    assert "name" not in body


@pytest.mark.functional
@pytest.mark.regression
def test_should_update_label_successfully(label, labels_api):
    """HLTC-08: Actualizar nombre y color de una etiqueta existente"""

    # Arrange
    original_name = label
    payload = UPDATE_LABEL_PAYLOAD
    labels_api.delete_label(payload["new_name"])

    # Act
    response = labels_api.update_label(original_name, payload)
    body = response.json()

    # Assert 1 — Status Code
    assert response.status_code == 200

    # Assert 2 — Response Body
    assert body["name"] == payload["new_name"]
    assert body["color"] == payload["color"]

    # Assert 3 — Schema Validation (soft assertion)
    assert validate_schema(body, LABEL_SCHEMA)

    # Assert 4 — Data Integrity via GET
    get_response = labels_api.get_label(payload["new_name"])
    get_body = get_response.json()

    assert get_response.status_code == 200
    assert get_body["name"] == payload["new_name"]
    assert get_body["color"] == payload["color"]

    # Cleanup — fixture teardown deletes original_name which no longer exists
    # after rename, so we clean up the renamed label here
    labels_api.delete_label(payload["new_name"])


@pytest.mark.acceptance
@pytest.mark.regression
def test_should_assign_label_to_issue(label, labels_api, issue):
    """HLTC-10: Asignar etiqueta existente a un issue"""

    # Arrange — use the unique label name from fixture directly to avoid
    # race conditions with the static updated-label-sergio name
    label_name = label

    # Act
    response = labels_api.add_labels_to_issue(issue, [label_name])
    body = response.json()

    # Assert 1 — Status Code
    assert response.status_code == 200

    # Assert 2 — Response Body
    label_names = [lbl["name"] for lbl in body]
    assert label_name in label_names

    # Assert 3 — Schema Validation (soft assertion)
    assert validate_schema(body, ASSIGN_LABELS_SCHEMA)

    # Assert 4 — Data Integrity via GET issue
    get_response = labels_api.get_issue(issue)
    get_body = get_response.json()

    assert get_response.status_code == 200
    issue_label_names = [lbl["name"] for lbl in get_body["labels"]]
    assert label_name in issue_label_names


@pytest.mark.functional
@pytest.mark.smoke
def test_should_get_existing_label_successfully(label, labels_api):
    """HLTC-06 integrity: Obtener una etiqueta existente por nombre"""

    # Arrange
    label_name = label
    expected_color = CREATE_LABEL_PAYLOAD["color"]

    # Act
    response = labels_api.get_label(label_name)
    body = response.json()

    # Assert 1 — Status Code
    assert response.status_code == 200

    # Assert 2 — Response Body
    assert body["name"] == label_name
    assert body["color"] == expected_color

    # Assert 3 — Schema Validation (soft assertion)
    assert validate_schema(body, LABEL_SCHEMA)

    # Assert 4 — Data Integrity
    assert body["default"] is False
    assert "description" in body

    # Assert 5 — Default Values
    assert isinstance(body["id"], int)
    assert body["id"] > 0


@pytest.mark.functional
@pytest.mark.regression
def test_should_delete_label_successfully(label, labels_api):
    """HLTC-09: Eliminar una etiqueta existente del repositorio"""

    # Arrange
    label_name = label

    # Act
    response = labels_api.delete_label(label_name)

    # Assert 1 — Status Code
    assert response.status_code == 204

    # Assert 2 — Response Body vacío
    assert response.text == ""

    # Assert 3 — Data Integrity via GET (debe retornar 404)
    get_response = labels_api.get_label(label_name)
    assert get_response.status_code == 404

    # Assert 4 — Error body confirma que la etiqueta no existe
    get_body = get_response.json()
    assert "message" in get_body
    assert get_body["message"] == "Not Found"


# ── Activity 3: Additional tests ─────────────────────────────────────────────

@pytest.mark.negative
@pytest.mark.regression
def test_should_fail_to_get_nonexistent_label(labels_api):
    """HLTC-11: GET sobre etiqueta inexistente devuelve 404"""

    # Arrange
    nonexistent_name = "nonexistent-label-sergio-xyz"
    labels_api.delete_label(nonexistent_name)

    # Act
    response = labels_api.get_label(nonexistent_name)
    body = response.json()

    # Assert 1 — Status Code
    assert response.status_code == 404

    # Assert 2 — Error message
    assert "message" in body
    assert body["message"] == "Not Found"

    # Assert 3 — Schema Validation (soft assertion)
    assert validate_schema(body, LABEL_ERROR_SCHEMA)

    # Assert 4 — No resource data in body
    assert "id" not in body
    assert "color" not in body


@pytest.mark.functional
@pytest.mark.smoke
def test_should_list_all_labels_from_repository(label, labels_api):
    """HLTC-12: Listar todas las etiquetas del repositorio"""

    # Act
    response = labels_api.list_labels()
    body = response.json()

    # Assert 1 — Status Code
    assert response.status_code == 200

    # Assert 2 — Response is a list
    assert isinstance(body, list)

    # Assert 3 — Schema Validation (soft assertion)
    assert validate_schema(body, LIST_LABELS_SCHEMA)

    # Assert 4 — The label created by the fixture is present
    label_names = [lbl["name"] for lbl in body]
    assert label in label_names


@pytest.mark.negative
@pytest.mark.regression
def test_should_fail_to_create_duplicate_label(label, labels_api):
    """HLTC-13: Crear etiqueta con nombre duplicado devuelve 422"""

    # Arrange — label fixture already created this label
    duplicate_payload = {
        "name": label,
        "color": "cc0000",
        "description": "Intento de etiqueta duplicada",
    }

    # Act
    response = labels_api.create_label(duplicate_payload)
    body = response.json()

    # Assert 1 — Status Code
    assert response.status_code == 422

    # Assert 2 — Error message present
    assert "message" in body
    assert body["message"] != ""

    # Assert 3 — No resource data returned
    assert "id" not in body


@pytest.mark.negative
@pytest.mark.regression
def test_should_fail_to_update_nonexistent_label(labels_api):
    """HLTC-14: PATCH sobre etiqueta inexistente devuelve 404"""

    # Arrange
    nonexistent_name = "nonexistent-label-sergio-xyz"
    labels_api.delete_label(nonexistent_name)
    payload = {"new_name": "renamed-label", "color": "aabbcc"}

    # Act
    response = labels_api.update_label(nonexistent_name, payload)
    body = response.json()

    # Assert 1 — Status Code
    assert response.status_code == 404

    # Assert 2 — Error message
    assert "message" in body
    assert body["message"] == "Not Found"

    # Assert 3 — Schema Validation (soft assertion)
    assert validate_schema(body, LABEL_ERROR_SCHEMA)

    # Assert 4 — No resource data in body
    assert "id" not in body
    assert "color" not in body


@pytest.mark.negative
@pytest.mark.regression
def test_should_fail_to_create_label_with_invalid_color(labels_api):
    """HLTC-15: Crear etiqueta con formato de color inválido devuelve 422"""

    # Arrange
    invalid_color_payload = {
        "name": "label-invalid-color-sergio",
        "color": "ZZZZZZ",
        "description": "Label con color inválido",
    }
    labels_api.delete_label(invalid_color_payload["name"])

    # Act
    response = labels_api.create_label(invalid_color_payload)
    body = response.json()

    # Assert 1 — Status Code
    assert response.status_code == 422

    # Assert 2 — Error message present
    assert "message" in body
    assert body["message"] != ""

    # Assert 3 — No resource was created
    assert "id" not in body
