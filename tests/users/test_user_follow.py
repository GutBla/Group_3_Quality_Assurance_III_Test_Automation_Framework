import pytest
from data.user_data import FOLLOW_USERNAME
from utils.logger import logger


@pytest.mark.functional
@pytest.mark.acceptance
@pytest.mark.smoke
@pytest.mark.xdist_group("follow")
def test_should_follow_user_successfully(github_user_api):
    """HLTC-22: Seguir a un usuario autenticado"""
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


@pytest.mark.functional
@pytest.mark.regression
@pytest.mark.xdist_group("follow")
def test_should_check_following_user_successfully(github_user_api):
    """HLTC-23: Verificar si el usuario autenticado sigue a otro"""
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


@pytest.mark.functional
@pytest.mark.acceptance
@pytest.mark.smoke
@pytest.mark.xdist_group("follow")
def test_should_unfollow_user_successfully(github_user_api):
    """HLTC-24: Dejar de seguir a un usuario"""
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
