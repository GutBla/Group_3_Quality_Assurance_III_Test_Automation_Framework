CREATE_ISSUE_PAYLOAD = {

    "title": "Test issue from Pytest",

    "body": "This issue was created for API testing."
}
MISSING_TITLE_ISSUE_PAYLOAD = {
    "body": "Issue sin título"
}
UPDATE_ISSUE_PAYLOAD = {
    "title": "Título del Issue Actualizado",
    "body": "Contenido del cuerpo del issue actualizado"
}
INVALID_ISSUE_NUMBER = 99999999
CLOSE_ISSUE_PAYLOAD = {
    "state": "closed"
}
INVALID_AUTH_HEADERS = {
    "Authorization": "Bearer token_falso_o_expirado_123"
}
LONG_TITLE_PAYLOAD = {
    "title": "A" * 1025,
    "body": "Probando el límite máximo de caracteres permitidos en el título."
}
NON_EXISTENT_REPO_NAME = "repositorio-fantasma-qa-999"
CREATE_COMMENT_PAYLOAD = {
    "body": (
        "Este es un comentario automatizado de prueba para "
        "verificar la integridad del endpoint de comentarios."
    )
}
