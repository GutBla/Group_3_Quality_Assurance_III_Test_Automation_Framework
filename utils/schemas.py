LABEL_SCHEMA = {
    "type": "object",
    "required": ["id", "name", "color", "url", "default"],
    "properties": {
        "id": {"type": "number"},
        "name": {"type": "string"},
        "color": {"type": "string"},
        "url": {"type": "string"},
        "default": {"type": "boolean"},
        "description": {"type": ["string", "null"]}
    },
    "additionalProperties": True
}

LABEL_ERROR_SCHEMA = {
    "type": "object",
    "required": ["message", "documentation_url"],
    "properties": {
        "message": {"type": "string"},
        "documentation_url": {"type": "string"}
    },
    "additionalProperties": True
}

ASSIGN_LABELS_SCHEMA = {
    "type": "array",
    "items": {
        "type": "object",
        "required": ["id", "name", "color", "url"],
        "properties": {
            "id": {"type": "number"},
            "name": {"type": "string"},
            "color": {"type": "string"},
            "url": {"type": "string"}
        }
    }
}

CREATE_ISSUE_SCHEMA = {

    "type": "object",

    "required": [
        "id",
        "number",
        "title",
        "body",
        "state",
        "url",
        "repository_url",
        "created_at",
        "updated_at"
    ],

    "properties": {

        "id": {"type": "number"},
        "number": {"type": "number"},
        "title": {"type": "string"},
        "body": {"type": "string"},
        "state": {"type": "string"},
        "url": {"type": "string"},
        "repository_url": {"type": "string"},
        "created_at": {"type": "string"},
        "updated_at": {"type": "string"},

        "labels": {"type": "array"},
        "assignees": {"type": "array"},
        "user": {"type": "object"}
    },

    "additionalProperties": True
}