import pytest
import time
import re
from jsonschema import validate
from config.config import REPO_NAME, USERNAME
from data.pull_request_data import (INVALID_AUTH_HEADERS,
                                    get_dynamic_body_payload,
                                    get_dynamic_title_payload)
from utils.logger import logger
from utils.schemas import (PR_LABELS_SCHEMA, PR_NOT_FOUND_SCHEMA,
                           PR_VALIDATION_ERROR_SCHEMA, PULL_REQUEST_SCHEMA,
                           UNAUTHORIZED_ERROR_SCHEMA, UPDATE_PR_SCHEMA)

PR_NUMBER = 1

pytestmark = pytest.mark.xdist_group(name="serial_tests")


@pytest.mark.functional
@pytest.mark.acceptance
@pytest.mark.smoke
def test_should_update_pr_title_successfully(pr_api, pr_state):
    """HLTC-27: Actualizar título de un pull request existente"""
    payload = get_dynamic_title_payload()
    logger.info(f"Preparando actualización de título del PR {PR_NUMBER}")
    logger.info(f"Nuevo título: {payload['title']}")
    response = pr_api.update_pull_request(PR_NUMBER, payload)
    body = response.json()
    logger.info("Verificando código de estado 200")
    assert response.status_code == 200
    logger.info("Verificando que el título fue actualizado correctamente")
    assert body["title"] == payload["title"]
    logger.info("Verificando que el número del PR no cambió")
    assert body["number"] == PR_NUMBER
    logger.info("Verificando que el título no está vacío")
    assert body["title"] != ""
    logger.info("Validando schema de respuesta contra UPDATE_PR_SCHEMA")
    validate(instance=body, schema=UPDATE_PR_SCHEMA)

    time.sleep(4)
    logger.info("Ejecutando verificación de integridad vía GET")
    get_response = pr_api.get_pull_request(PR_NUMBER)
    get_body = get_response.json()
    assert get_response.status_code == 200
    assert get_body["title"] == payload["title"]
    assert get_body["number"] == PR_NUMBER


@pytest.mark.functional
@pytest.mark.regression
def test_should_update_pr_body_successfully(pr_api, pr_state):
    """HLTC-28: Actualizar cuerpo de un pull request existente"""
    payload = get_dynamic_body_payload()
    logger.info(f"Preparando actualización del cuerpo del PR {PR_NUMBER}")
    logger.info(f"Nuevo cuerpo: {payload['body']}")
    response = pr_api.update_pull_request(PR_NUMBER, payload)
    body = response.json()
    logger.info("Verificando código de estado 200")
    assert response.status_code == 200
    logger.info("Verificando que el cuerpo fue actualizado correctamente")
    assert body["body"] == payload["body"]
    logger.info("Verificando que la respuesta contiene el campo 'body'")
    assert "body" in body
    logger.info("Verificando que el número del PR es correcto")
    assert body["number"] == PR_NUMBER
    logger.info("Verificando que el cuerpo no está vacío")
    assert body["body"] != ""
    logger.info("Validando schema de respuesta contra UPDATE_PR_SCHEMA")
    validate(instance=body, schema=UPDATE_PR_SCHEMA)

    time.sleep(4)
    logger.info("Ejecutando verificación de integridad vía GET")
    get_response = pr_api.get_pull_request(PR_NUMBER)
    get_body = get_response.json()
    assert get_response.status_code == 200
    assert get_body["body"] == payload["body"]


@pytest.mark.functional
@pytest.mark.regression
def test_should_add_label_to_pr_successfully(pr_api, pr_temp_label):
    """HLTC-29: Asignar etiqueta existente a un pull request"""
    label_name = pr_temp_label
    logger.info(f"Agregando etiqueta '{label_name}' al PR {PR_NUMBER}")
    response = pr_api.add_labels(PR_NUMBER, [label_name])
    body = response.json()
    logger.info("Verificando código de estado 200 o 201")
    assert response.status_code in [200, 201]
    logger.info("Verificando que la etiqueta fue agregada correctamente")
    label_names = [lbl["name"] for lbl in body]
    assert label_name in label_names
    logger.info("Verificando que la respuesta es un array")
    assert isinstance(body, list)
    logger.info("Verificando que cada etiqueta contiene el campo 'name'")
    for lbl in body:
        assert "name" in lbl
    logger.info("Verificando que al menos una etiqueta está presente")
    assert len(body) > 0
    logger.info("Validando schema de respuesta contra PR_LABELS_SCHEMA")
    validate(instance=body, schema=PR_LABELS_SCHEMA)

    time.sleep(4)
    logger.info("Ejecutando verificación de integridad vía GET labels")
    get_response = pr_api.get_labels(PR_NUMBER)
    get_body = get_response.json()
    assert get_response.status_code == 200
    get_label_names = [lbl["name"] for lbl in get_body]
    assert label_name in get_label_names


@pytest.mark.functional
@pytest.mark.acceptance
@pytest.mark.smoke
def test_should_close_pr_successfully(pr_api, pr_state):
    """HLTC-30: Cambiar estado de pull request a cerrado"""
    if pr_state["state"] == "closed":
        pytest.skip("El PR ya está cerrado — este test requiere un PR abierto.")
    logger.info(f"Cerrando PR {PR_NUMBER}")
    response = pr_api.close_pull_request(PR_NUMBER)
    body = response.json()
    logger.info("Verificando código de estado 200")
    assert response.status_code == 200
    logger.info("Verificando que el estado cambió a 'closed'")
    assert body["state"] == "closed"
    logger.info("Verificando que la respuesta contiene campo 'merged'")
    assert "merged" in body
    logger.info("Verificando que la respuesta contiene campo 'state'")
    assert "state" in body
    logger.info("Verificando que el número del PR no cambió")
    assert body["number"] == PR_NUMBER
    logger.info("Validando schema de respuesta contra UPDATE_PR_SCHEMA")
    validate(instance=body, schema=UPDATE_PR_SCHEMA)

    time.sleep(4)
    logger.info("Ejecutando verificación de integridad vía GET")
    get_response = pr_api.get_pull_request(PR_NUMBER)
    get_body = get_response.json()
    assert get_response.status_code == 200
    assert get_body["state"] == "closed"


@pytest.mark.negative
@pytest.mark.regression
def test_should_fail_to_add_empty_label_list(pr_api):
    """HLTC-31: Agregar lista vacía de etiquetas a un pull request debe fallar"""
    logger.info(f"Intentando agregar lista de etiquetas vacía al PR {PR_NUMBER}")
    response = pr_api.add_labels(PR_NUMBER, [])
    body = response.json()
    logger.info("Verificando código de estado 422")
    assert response.status_code == 422
    logger.info("Verificando que la respuesta contiene campo 'message'")
    assert "message" in body
    logger.info("Verificando que el mensaje de error no está vacío")
    assert body["message"] != ""
    logger.info("Verificando que la respuesta contiene 'documentation_url'")
    assert "documentation_url" in body
    msg_lower = body["message"].lower()
    assert any(
        keyword in msg_lower
        for keyword in ["validation", "invalid", "no subschema"]
    ), f"Mensaje de error inesperado: {body['message']}"
    logger.info("Validando schema de respuesta contra PR_VALIDATION_ERROR_SCHEMA")
    validate(instance=body, schema=PR_VALIDATION_ERROR_SCHEMA)


@pytest.mark.functional
@pytest.mark.smoke
def test_should_get_pull_request_successfully(pr_api):
    """Obtener un pull request por número debe retornar 200 y los datos correctos"""
    logger.info(f"Obteniendo PR {PR_NUMBER}")
    response = pr_api.get_pull_request(PR_NUMBER)
    body = response.json()
    logger.info("Verificando código de estado 200")
    assert response.status_code == 200
    logger.info("Verificando campos obligatorios en la respuesta")
    assert "number" in body
    assert "title" in body
    assert "state" in body
    logger.info("Verificando que el número del PR coincide")
    assert body["number"] == PR_NUMBER
    logger.info("Verificando que el título no está vacío")
    assert body["title"] is not None
    assert body["title"] != ""
    logger.info("Verificando que el estado es 'open' o 'closed'")
    assert body["state"] in ["open", "closed"]
    logger.info("Validando schema de respuesta contra PULL_REQUEST_SCHEMA")
    validate(instance=body, schema=PULL_REQUEST_SCHEMA)


@pytest.mark.negative
@pytest.mark.smoke
def test_should_fail_to_get_pr_with_invalid_token(pr_api):
    """Obtener un pull request con token inválido debe retornar 401"""
    logger.info(f"Intentando obtener PR {PR_NUMBER} con token inválido")
    response = pr_api.client.get(
        f"{pr_api._pulls_base}/{PR_NUMBER}",
        headers=INVALID_AUTH_HEADERS,
    )
    body = response.json()
    logger.info("Verificando código de estado 401")
    assert response.status_code == 401
    logger.info("Verificando que la respuesta contiene mensaje de error")
    assert "message" in body
    logger.info("Verificando que el mensaje indica credenciales incorrectas")
    assert body["message"].lower() == "bad credentials"
    logger.info("Validando schema de respuesta contra UNAUTHORIZED_ERROR_SCHEMA")
    validate(instance=body, schema=UNAUTHORIZED_ERROR_SCHEMA)


@pytest.mark.negative
@pytest.mark.regression
def test_should_return_404_for_nonexistent_pr(pr_api):
    """Obtener un pull request inexistente debe retornar 404"""
    fake_pr_number = 99999999
    logger.info(f"Intentando obtener PR inexistente {fake_pr_number}")
    response = pr_api.get_pull_request(fake_pr_number)
    body = response.json()
    logger.info("Verificando código de estado 404")
    assert response.status_code == 404
    logger.info("Verificando que la respuesta contiene campo 'message'")
    assert "message" in body
    logger.info("Verificando que el mensaje indica 'Not Found'")
    assert "Not Found" in body["message"]
    logger.info("Validando schema de respuesta contra PR_NOT_FOUND_SCHEMA")
    validate(instance=body, schema=PR_NOT_FOUND_SCHEMA)
    logger.info("Verificando que la respuesta no contiene campo 'id'")
    assert "id" not in body


@pytest.mark.functional
@pytest.mark.regression
def test_should_list_pull_requests_successfully(pr_api):
    """Listar pull requests del repositorio debe retornar 200 y un array"""
    logger.info(f"Listando PRs del repositorio {USERNAME}/{REPO_NAME}")
    response = pr_api.list_pull_requests(state="all")
    body = response.json()
    logger.info("Verificando código de estado 200")
    assert response.status_code == 200
    logger.info("Verificando que la respuesta es un array")
    assert isinstance(body, list)
    if len(body) > 0:
        logger.info("Verificando campos básicos del primer PR en la lista")
        first_pr = body[0]
        assert "number" in first_pr
        assert "title" in first_pr
        assert "state" in first_pr
        validate(instance=first_pr, schema=PULL_REQUEST_SCHEMA)
    logger.info(f"Total de PRs encontrados: {len(body)}")


@pytest.mark.functional
@pytest.mark.regression
def test_should_have_no_residual_data_after_updates(pr_api, pr_state):
    """Verifica que no queden datos residuales de pruebas en el PR"""
    time.sleep(4)
    logger.info(f"Verificando integridad final del PR {PR_NUMBER}")
    response = pr_api.get_pull_request(PR_NUMBER)
    body = response.json()
    assert response.status_code == 200
    test_patterns = [
        re.compile(r"Título actualizado \d+"),
        re.compile(r"Cuerpo modificado \d+"),
        re.compile(r"temp-label-\d+"),
    ]
    residue = False
    for pattern in test_patterns:
        if pattern.search(body.get("title") or ""):
            residue = True
        if pattern.search(body.get("body") or ""):
            residue = True
    logger.info("Verificando que no hay residuos en título o cuerpo")
    assert residue is False, (
        f"Se encontraron datos residuales de test en el PR: "
        f"title='{body.get('title')}', body='{body.get('body')}'"
    )
    logger.info("Verificando campos básicos del PR")
    assert "number" in body
    assert "title" in body
    assert "state" in body
    logger.info(f"Estado final del PR: {body['state']}")
    if pr_state["state"]:
        assert body["state"] == pr_state["state"]
