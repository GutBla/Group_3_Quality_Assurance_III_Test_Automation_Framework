from jsonschema import validate

from data.label_data import (
    CREATE_LABEL_PAYLOAD,
    CREATE_LABEL_PAYLOAD_NO_NAME,
    UPDATE_LABEL_PAYLOAD,
    LABEL_UPDATED_NAME,
    ASSIGN_LABELS_PAYLOAD,
)
from utils.schemas import LABEL_SCHEMA, LABEL_ERROR_SCHEMA, ASSIGN_LABELS_SCHEMA


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

    # Assert 3 — Schema Validation
    validate(instance=body, schema=LABEL_SCHEMA)

    # Assert 4 — Data Integrity via GET
    get_response = labels_api.get_label(payload["name"])
    get_body = get_response.json()

    assert get_response.status_code == 200
    assert get_body["name"] == payload["name"]
    assert get_body["color"] == payload["color"]

    # Cleanup
    labels_api.delete_label(payload["name"])


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

    # Assert 3 — Schema Validation
    validate(instance=body, schema=LABEL_ERROR_SCHEMA)

    # Assert 4 — Data Integrity (no label was created)
    assert "id" not in body
    assert "name" not in body


def test_should_update_label_successfully(label, labels_api):
    """HLTC-08: Actualizar nombre y color de una etiqueta existente"""

    # Arrange
    original_name = label
    payload = UPDATE_LABEL_PAYLOAD

    # Act
    response = labels_api.update_label(original_name, payload)
    body = response.json()

    # Assert 1 — Status Code
    assert response.status_code == 200

    # Assert 2 — Response Body
    assert body["name"] == payload["new_name"]
    assert body["color"] == payload["color"]

    # Assert 3 — Schema Validation
    validate(instance=body, schema=LABEL_SCHEMA)

    # Assert 4 — Data Integrity via GET
    get_response = labels_api.get_label(payload["new_name"])
    get_body = get_response.json()

    assert get_response.status_code == 200
    assert get_body["name"] == payload["new_name"]
    assert get_body["color"] == payload["color"]


def test_should_assign_label_to_issue(label, labels_api, issue):
    """HLTC-10: Asignar etiqueta existente a un issue"""

    # Arrange — update the label first so its name matches ASSIGN_LABELS_PAYLOAD
    from data.label_data import UPDATE_LABEL_PAYLOAD
    labels_api.update_label(label, UPDATE_LABEL_PAYLOAD)

    # Act
    response = labels_api.add_labels_to_issue(issue, ASSIGN_LABELS_PAYLOAD)
    body = response.json()

    # Assert 1 — Status Code
    assert response.status_code == 200

    # Assert 2 — Response Body
    label_names = [lbl["name"] for lbl in body]
    assert LABEL_UPDATED_NAME in label_names

    # Assert 3 — Schema Validation
    validate(instance=body, schema=ASSIGN_LABELS_SCHEMA)

    # Assert 4 — Data Integrity via GET issue
    get_response = labels_api.get_issue(issue)
    get_body = get_response.json()

    assert get_response.status_code == 200
    issue_label_names = [lbl["name"] for lbl in get_body["labels"]]
    assert LABEL_UPDATED_NAME in issue_label_names


def test_should_get_existing_label_successfully(label, labels_api):
    """HLTC-06 integrity: Obtener una etiqueta existente por nombre"""

    # Arrange
    label_name = label

    # Act
    response = labels_api.get_label(label_name)
    body = response.json()

    # Assert 1 — Status Code
    assert response.status_code == 200

    # Assert 2 — Response Body
    assert body["name"] == label_name
    assert body["color"] == CREATE_LABEL_PAYLOAD["color"]

    # Assert 3 — Schema Validation
    validate(instance=body, schema=LABEL_SCHEMA)

    # Assert 4 — Data Integrity
    assert body["default"] is False
    assert "description" in body

    # Assert 5 — Default Values
    assert isinstance(body["id"], int)
    assert body["id"] > 0


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
