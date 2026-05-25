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

UPDATE_PROFILE_SCHEMA = {
    "type": "object",
    "required": ["login", "id"],
    "properties": {
        "login": {"type": "string"},
        "id": {"type": "number"},
        "bio": {"type": ["string", "null"]},
        "location": {"type": ["string", "null"]},
        "type": {"type": "string"}
    },
    "additionalProperties": True
}

CREATE_REPO_SCHEMA = {

    "type": "object",

    "required": [
        "id",
        "name",
        "full_name",
        "private",
        "owner",
        "html_url",
        "description",
        "url",
        "has_issues",
        "visibility",
        "created_at",
        "default_branch"
    ],

    "properties": {

        "id":             {"type": "integer"},
        "name":           {"type": "string"},
        "full_name":      {"type": "string"},        # "matsan201/mi-repo-de-prueba"
        "private":        {"type": "boolean"},
        "description":    {"type": ["string", "null"]},
        "html_url":       {"type": "string"},
        "url":            {"type": "string"},
        "has_issues":     {"type": "boolean"},
        "visibility":     {"type": "string", "enum": ["public", "private", "internal"]},
        "created_at":     {"type": "string"},
        "default_branch": {"type": "string"},
        "fork":           {"type": "boolean"},

        "owner": {
            "type": "object",
            "required": ["login", "id"],
            "properties": {
                "login": {"type": "string"},
                "id":    {"type": "integer"}
            }
        }
    },

    "additionalProperties": True
}

UPDATE_REPO_SCHEMA = {
    "type": "object",
    "required": ["id", "name", "full_name", "private", "description", "visibility"],
    "properties": {
        "id":          {"type": "integer"},
        "name":        {"type": "string"},
        "full_name":   {"type": "string"},
        "private":     {"type": "boolean"},
        "description": {"type": ["string", "null"]},
        "visibility":  {"type": "string", "enum": ["public", "private", "internal"]},
        "html_url":    {"type": "string"},
        "updated_at":  {"type": "string"},
    },
    "additionalProperties": True
}

ERROR_REPO_SCHEMA = {
    "type": "object",
    "required": ["message", "errors"],
    "properties": {
        "message": {"type": "string"},
        "errors": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "resource": {"type": "string"},
                    "code":     {"type": "string"},
                    "field":    {"type": "string"},
                    "message":  {"type": "string"}
                }
            }
        }
    },
    "additionalProperties": True
}

ERROR_VALIDATION_ISSUE_SCHEMA = {
    "type": "object",
    "required": ["message"],
    "properties": {
        "message": {"type": "string"},
        "errors": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "field": {"type": "string"},
                    "code": {"type": "string"},
                    "resource": {"type": "string"},
                    "message": {"type": "string"}
                }
            }
        }
    },
    "additionalProperties": True
}
UPDATE_ISSUE_SCHEMA = {
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
NOT_FOUND_ISSUE_SCHEMA = {
    "type": "object",
    "required": ["message"],
    "properties": {
        "message": {"type": "string"},
        "documentation_url": {"type": "string"}
    },
    "additionalProperties": True
}
