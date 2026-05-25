PUBLIC_USERNAME = "octocat"
DISPOSABLE_EMAIL = "andrea.qa.test@test.com"
FOLLOW_USERNAME = "octocat"

UPDATE_PROFILE_PAYLOAD = {
    "bio": "Nueva API",
    "location": "Bolivia"
}

def get_update_profile_payload():
    import datetime
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    return {
        "bio": f"API Testing Professional - {timestamp}",
        "location": "Cochabamba, Bolivia"
    }

def get_invalid_update_payload(original_login, original_id, new_bio="Nueva API QA"):
    return {
        "login": f"intento_{original_login}",
        "id": original_id + 9999,
        "bio": new_bio
    }