import datetime

PUBLIC_USERNAME = "octocat"
FOLLOW_USERNAME = "octocat"

DISPOSABLE_EMAIL = "andrea.qa.test@test.com"

INVALID_AUTH_HEADERS = {
    "Authorization": "Bearer token_invalido_123456789"
}

UPDATE_PROFILE_PAYLOAD = {
    "bio": "Nueva API",
    "location": "Bolivia",
}

UPDATE_EDITABLE_FIELDS_PAYLOAD = {
    "company": "QA Testing Team",
    "location": "Cochabamba, Bolivia",
    "hireable": True,
}

def get_update_profile_payload():
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    return {
        "bio": f"API Testing Professional - {timestamp}",
        "location": "Cochabamba, Bolivia",
    }


def get_invalid_update_payload(original_login, original_id, new_bio="Nueva API QA"):
    return {
        "login": f"intento_{original_login}",
        "id": original_id + 9999,
        "bio": new_bio,
    }


def get_update_editable_payload():
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    return {
        "company": f"QA Automation Hub - {timestamp}",
        "location": "Mendoza, Argentina",
        "hireable": True,
    }