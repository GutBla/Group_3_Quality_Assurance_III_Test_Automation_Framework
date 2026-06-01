import pytest
from jsonschema import validate

from data.user_data import (DISPOSABLE_EMAIL, FOLLOW_USERNAME,
                            INVALID_AUTH_HEADERS, PUBLIC_USERNAME,
                            get_invalid_update_payload,
                            get_update_editable_payload,
                            get_update_profile_payload)
from utils.logger import logger
from utils.schemas import (AUTH_USER_SCHEMA, EMAIL_ERROR_SCHEMA,
                           PUBLIC_USER_SCHEMA, UNAUTHORIZED_ERROR_SCHEMA,
                           UPDATE_PROFILE_SCHEMA)

# HLTC-16 — Obtener usuario autenticado

@pytest.mark.functional
@pytest.mark.acceptance
@pytest.mark.smoke
def test_hltc16_get_authenticated_user(github_user_api):
    
    logger.info("Ejecutando GET /user para el usuario autenticado")
    response = github_user_api.get_authenticated_user()
    body = response.json()

    logger.info("Verificando código de estado 200")
    assert response.status_code == 200

    logger.info("Verificando campos obligatorios en la respuesta")
    assert "login" in body
    assert "id" in body
    assert "email" in body

    logger.info("Verificando integridad de datos")
    assert body["login"] is not None
    assert body["login"] != ""
    assert isinstance(body["id"], int)

    logger.info("Validando schema contra AUTH_USER_SCHEMA")
    validate(instance=body, schema=AUTH_USER_SCHEMA)


# HLTC-17 — Acceso no autorizado (token inválido)

@pytest.mark.negative
@pytest.mark.smoke
def test_hltc17_unauthorized_access_rejected(github_user_api):
    
    logger.info("Ejecutando GET /user con token inválido")
    response = github_user_api.get_authenticated_user(
        headers=INVALID_AUTH_HEADERS
    )
    body = response.json()

    logger.info("Verificando código de estado 401 o 403")
    assert response.status_code in [401, 403]

    logger.info("Verificando que la respuesta contiene campo 'message'")
    assert "message" in body

    logger.info("Verificando que el mensaje no está vacío")
    assert body["message"] != ""

    logger.info("Verificando que el mensaje indica credenciales inválidas")
    assert "bad credentials" in body["message"].lower()

    logger.info("Validando schema contra UNAUTHORIZED_ERROR_SCHEMA")
    validate(instance=body, schema=UNAUTHORIZED_ERROR_SCHEMA)


# HLTC-18 — Actualizar perfil (bio y location)


@pytest.mark.functional
@pytest.mark.acceptance
@pytest.mark.smoke
def test_hltc18_update_profile(github_user_api, profile_restore):
    
    payload = get_update_profile_payload()

    logger.info(f"Actualizando perfil con bio='{payload['bio']}'")
    response = github_user_api.update_profile(payload)
    body = response.json() if response.status_code == 200 else None

    logger.info("Verificando código de estado 200 o 204")
    assert response.status_code in [200, 204]

    if response.status_code == 200:
        logger.info("Verificando que bio fue actualizado correctamente")
        assert body["bio"] == payload["bio"]

        logger.info("Verificando que location fue actualizado correctamente")
        assert body["location"] == payload["location"]

        logger.info("Verificando que los campos bio y location existen")
        assert "bio" in body
        assert "location" in body

        logger.info("Verificando que bio no está vacío")
        assert body["bio"] != ""

        logger.info("Validando schema contra UPDATE_PROFILE_SCHEMA")
        validate(instance=body, schema=UPDATE_PROFILE_SCHEMA)

        logger.info("Ejecutando verificación de integridad vía GET")
        get_response = github_user_api.get_authenticated_user()
        get_body = get_response.json()
        assert get_body["bio"] == payload["bio"]
        assert get_body["location"] == payload["location"]


# HLTC-19 — Actualizar perfil con campos protegidos (debe ignorarlos)


@pytest.mark.functional
@pytest.mark.regression
def test_hltc19_update_profile_protected_fields_ignored(
    github_user_api, profile_restore
):
    
    original = github_user_api.get_authenticated_user().json()
    original_login = original["login"]
    original_id = original["id"]

    import datetime
    new_bio = f"QA Integrity Check {datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"
    payload = get_invalid_update_payload(original_login, original_id, new_bio=new_bio)

    logger.info(
        f"Enviando payload con campos protegidos: login='{payload['login']}', "
        f"id={payload['id']}, bio='{payload['bio']}'"
    )
    response = github_user_api.update_profile(payload)
    body = response.json()

    logger.info("Verificando código de estado 200")
    assert response.status_code == 200

    logger.info("Verificando que 'login' NO fue modificado")
    assert body["login"] == original_login

    logger.info("Verificando que 'id' NO fue modificado")
    assert body["id"] == original_id

    logger.info("Verificando que 'bio' SÍ fue actualizado")
    assert body["bio"] == new_bio

    logger.info("Verificando que la respuesta contiene login e id")
    assert "login" in body
    assert "id" in body

    logger.info("Validando schema contra UPDATE_PROFILE_SCHEMA")
    validate(instance=body, schema=UPDATE_PROFILE_SCHEMA)


# HLTC-20 — Obtener perfil público de un usuario

@pytest.mark.functional
@pytest.mark.acceptance
@pytest.mark.smoke
def test_hltc20_get_public_user(github_user_api):
    
    username = PUBLIC_USERNAME

    logger.info(f"Ejecutando GET /users/{username}")
    response = github_user_api.get_user(username)
    body = response.json()

    logger.info("Verificando código de estado 200")
    assert response.status_code == 200

    logger.info("Verificando campos públicos en la respuesta")
    assert "login" in body
    assert "id" in body

    logger.info("Verificando que el login coincide con el usuario solicitado")
    assert body["login"].lower() == username.lower()

    logger.info("Verificando que id es un número")
    assert isinstance(body["id"], int)

    logger.info("Validando schema contra PUBLIC_USER_SCHEMA")
    validate(instance=body, schema=PUBLIC_USER_SCHEMA)


# HLTC-21 — Actualizar campos editables: company, location, hireable

@pytest.mark.functional
@pytest.mark.regression
def test_hltc21_update_editable_fields(github_user_api, profile_restore):
    
    payload = get_update_editable_payload()

    logger.info(
        f"Actualizando campos editables: company='{payload['company']}', "
        f"location='{payload['location']}', hireable={payload['hireable']}"
    )
    response = github_user_api.update_profile(payload)
    body = response.json()

    logger.info("Verificando código de estado 200")
    assert response.status_code == 200

    logger.info("Verificando que 'company' fue actualizado correctamente")
    assert body["company"] == payload["company"]

    logger.info("Verificando que 'location' fue actualizado correctamente")
    assert body["location"] == payload["location"]

    logger.info("Verificando que 'hireable' fue establecido en True")
    assert body["hireable"] is True

    logger.info("Verificando que los campos company, location, hireable existen")
    assert "company" in body
    assert "location" in body
    assert "hireable" in body

    logger.info("Validando schema contra UPDATE_PROFILE_SCHEMA")
    validate(instance=body, schema=UPDATE_PROFILE_SCHEMA)

    logger.info("Ejecutando verificación de integridad vía GET")
    get_response = github_user_api.get_authenticated_user()
    get_body = get_response.json()
    assert get_body["company"] == payload["company"]
    assert get_body["location"] == payload["location"]
    assert get_body["hireable"] is True


# HLTC-22 — Seguir a un usuario

@pytest.mark.functional
@pytest.mark.acceptance
@pytest.mark.smoke
def test_hltc22_follow_user(github_user_api):
    
    target = FOLLOW_USERNAME

    logger.info(f"Siguiendo al usuario '{target}'")
    response = github_user_api.follow_user(target)

    logger.info("Verificando código de estado 204 No Content")
    assert response.status_code == 204

    logger.info("Verificando que el cuerpo de la respuesta está vacío")
    assert response.text == ""

    logger.info("Verificando que la respuesta no contiene mensaje de error")
    assert "error" not in response.text.lower()

    logger.info("Ejecutando verificación de integridad vía HEAD")
    check_response = github_user_api.check_following(target)
    assert check_response.status_code == 204

    logger.info(f"Teardown: dejando de seguir a '{target}'")
    github_user_api.unfollow_user(target)


# HLTC-23 — Verificar si el usuario sigue a otro

@pytest.mark.functional
@pytest.mark.regression
def test_hltc23_check_following_user(github_user_api):
    
    target = FOLLOW_USERNAME

    logger.info(f"Asegurando que seguimos a '{target}' antes de verificar")
    github_user_api.follow_user(target)

    logger.info(f"Ejecutando HEAD /user/following/{target}")
    response = github_user_api.check_following(target)

    logger.info("Verificando código de estado 204 — usuario sigue al target")
    assert response.status_code == 204

    logger.info("Verificando que el cuerpo está vacío (HEAD no tiene body)")
    assert response.text == ""

    logger.info("Verificando que la respuesta no contiene 'Not Found'")
    assert "Not Found" not in response.text

    logger.info(f"Teardown: dejando de seguir a '{target}'")
    github_user_api.unfollow_user(target)


# HLTC-24 — Dejar de seguir a un usuario

@pytest.mark.functional
@pytest.mark.acceptance
@pytest.mark.smoke
def test_hltc24_unfollow_user(github_user_api):
    
    target = FOLLOW_USERNAME

    logger.info(f"Asegurando que seguimos a '{target}' antes de dejar de seguir")
    follow_resp = github_user_api.follow_user(target)
    assert follow_resp.status_code == 204

    logger.info("Verificando que efectivamente seguimos al target")
    check_resp = github_user_api.check_following(target)
    assert check_resp.status_code == 204

    logger.info(f"Ejecutando DELETE /user/following/{target}")
    unfollow_resp = github_user_api.unfollow_user(target)

    logger.info("Verificando código de estado 204 No Content")
    assert unfollow_resp.status_code == 204

    logger.info("Verificando que el cuerpo está vacío")
    assert unfollow_resp.text == ""

    logger.info("Verificando que ya no seguimos al target con HEAD — espera 404")
    not_following_resp = github_user_api.check_following(target)
    assert not_following_resp.status_code == 404


# HLTC-25 — Agregar email con dominio desechable (debe ser rechazado)

@pytest.mark.negative
@pytest.mark.regression
def test_hltc25_add_disposable_email_rejected(github_user_api):
    
    logger.info(f"Intentando agregar email desechable: {DISPOSABLE_EMAIL}")
    response = github_user_api.add_emails([DISPOSABLE_EMAIL])
    body = response.json()

    logger.info("Verificando código de estado 422 Unprocessable Entity")
    assert response.status_code == 422

    logger.info("Verificando mensaje de error de verificación de dominio")
    assert body["message"] == "Email domain could not be verified"

    logger.info("Verificando que la respuesta contiene 'documentation_url'")
    assert "documentation_url" in body

    logger.info("Verificando que 'status' indica 422")
    assert body["status"] == "422"

    logger.info("Verificando que el mensaje de error no está vacío")
    assert body["message"] != ""

    logger.info("Validando schema contra EMAIL_ERROR_SCHEMA")
    validate(instance=body, schema=EMAIL_ERROR_SCHEMA)


#  Verificar que no quedan residuos de pruebas en el perfil (Integridad)

@pytest.mark.functional
@pytest.mark.regression
def test_profile_has_no_residual_test_data(github_user_api, profile_restore):
    
    import re

    logger.info("Obteniendo estado actual del perfil para verificación de integridad")
    response = github_user_api.get_authenticated_user()
    body = response.json()

    assert response.status_code == 200

    test_patterns = [
        re.compile(r"API Testing Professional", re.IGNORECASE),
        re.compile(r"QA Integrity Check", re.IGNORECASE),
        re.compile(r"QA Automation Hub", re.IGNORECASE),
        re.compile(r"Buenos Aires, Argentina", re.IGNORECASE),
        re.compile(r"Mendoza, Argentina", re.IGNORECASE),
    ]

    residue_found = False
    residue_info = ""
    for pattern in test_patterns:
        if pattern.search(body.get("bio") or ""):
            residue_found = True
            residue_info = f"bio='{body['bio']}'"
            break
        if pattern.search(body.get("location") or ""):
            residue_found = True
            residue_info = f"location='{body['location']}'"
            break
        if pattern.search(body.get("company") or ""):
            residue_found = True
            residue_info = f"company='{body['company']}'"
            break

    logger.info("Verificando que no hay residuos de pruebas en bio/location/company")
    assert residue_found is False, (
        f"Se encontraron datos residuales de test en el perfil: {residue_info}"
    )

    logger.info("Verificando que el perfil contiene los campos obligatorios")
    assert "login" in body
    assert "id" in body
    assert "bio" in body
    assert "location" in body
    assert "company" in body