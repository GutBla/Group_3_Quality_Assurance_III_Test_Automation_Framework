import time

def get_update_profile_payload():
    return {
        "bio": f"QA Automation Engineer - {int(time.time())}",
        "location": "Cochambamba, Bolivia"
    }

def get_invalid_update_payload(original_login, original_id):
    return {
        "login": f"invalid_{original_login}",
        "id": original_id + 99999,
        "bio": f"Testing protected fields - {int(time.time())}"
    }

PUBLIC_USERNAME = "octocat"