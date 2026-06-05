import uuid


def get_unique_repo_name():
    return f"mi-repo-de-prueba-{uuid.uuid4().hex[:8]}"


def make_repo_payload(repo_name):
    return {
        "name": repo_name,
        "description": "Repositorio creado desde Postman para testing",
        "private": False,
        "has_issues": True,
    }


UPDATE_DESCRIPTION_PAYLOAD = {
    "description": "Descripción actualizada desde Postman",
    "private": False,
    "has_wiki": False,
}

UPDATE_VISIBILITY_PAYLOAD = {
    "private": True,
}
