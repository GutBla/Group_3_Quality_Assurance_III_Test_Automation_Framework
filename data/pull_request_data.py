import datetime

PR_NUMBER = 1

UPDATE_TITLE_PAYLOAD = {
    "title": f"Título actualizado {datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"
}

UPDATE_BODY_PAYLOAD = {
    "body": f"Cuerpo modificado {datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"
}

CLOSE_PR_PAYLOAD = {
    "state": "closed"
}

REOPEN_PR_PAYLOAD = {
    "state": "open"
}

ADD_LABEL_PAYLOAD = {
    "labels": ["bug"]
}

EMPTY_LABEL_PAYLOAD = {
    "labels": []
}

INVALID_AUTH_HEADERS = {
    "Authorization": "Bearer token_invalido_123456789"
}


def get_dynamic_title_payload():
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    return {"title": f"Título actualizado {timestamp}"}


def get_dynamic_body_payload():
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    return {"body": f"Cuerpo modificado {timestamp}"}


def get_dynamic_label_name():
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    return f"temp-label-{timestamp}"