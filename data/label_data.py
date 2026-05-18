LABEL_NAME = "test-label-sergio"
LABEL_UPDATED_NAME = "updated-label-sergio"

CREATE_LABEL_PAYLOAD = {
    "name": LABEL_NAME,
    "color": "e11d48",
    "description": "Label created via Pytest API test"
}

UPDATE_LABEL_PAYLOAD = {
    "new_name": LABEL_UPDATED_NAME,
    "color": "00ff88",
    "description": "Updated via PATCH in Pytest"
}

CREATE_LABEL_PAYLOAD_NO_NAME = {
    "color": "ff0000",
    "description": "Label without name - should fail"
}

ASSIGN_LABELS_PAYLOAD = [LABEL_UPDATED_NAME]
