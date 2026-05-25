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

LIST_LABELS_SCHEMA = {
    "type": "array",
    "items": LABEL_SCHEMA
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
        "id": {"type": "integer"},
        "name": {"type": "string"},
        "full_name": {"type": "string"},
        "private": {"type": "boolean"},
        "description": {"type": ["string", "null"]},
        "html_url": {"type": "string"},
        "url": {"type": "string"},
        "has_issues": {"type": "boolean"},
        "visibility": {"type": "string", "enum": ["public", "private", "internal"]},
        "created_at": {"type": "string"},
        "default_branch": {"type": "string"},
        "fork": {"type": "boolean"},
        "owner": {
            "type": "object",
            "required": ["login", "id"],
            "properties": {
                "login": {"type": "string"},
                "id": {"type": "integer"}
            }
        }
    },
    "additionalProperties": True
}

LIST_REPOS_SCHEMA = {
    "type": "array",
    "items": {
        "type": "object",
        "required": ["id", "name", "full_name", "private", "owner"],
        "properties": {
            "id": {"type": "integer"},
            "name": {"type": "string"},
            "full_name": {"type": "string"},
            "private": {"type": "boolean"},
            "owner": {"type": "object"},
        }
    }
}

CONTRIBUTORS_SCHEMA = {
    "type": "array",
    "items": {
        "type": "object",
        "required": ["login", "id", "contributions"],
        "properties": {
            "login": {"type": "string"},
            "id": {"type": "integer"},
            "contributions": {"type": "integer"},
        }
    }
}

AUTH_USER_SCHEMA = {
    "type": "object",
    "required": ["login", "id"],
    "properties": {
        "login": {"type": "string"},
        "id": {"type": "number"},
        "email": {"type": ["string", "null"]},
        "name": {"type": ["string", "null"]},
        "bio": {"type": ["string", "null"]},
        "location": {"type": ["string", "null"]}
    },
    "additionalProperties": True
}

UPDATE_REPO_SCHEMA = {
    "type": "object",
    "required": ["id", "name", "full_name", "private", "description", "visibility"],
    "properties": {
        "id": {"type": "integer"},
        "name": {"type": "string"},
        "full_name": {"type": "string"},
        "private": {"type": "boolean"},
        "description": {"type": ["string", "null"]},
        "visibility": {"type": "string", "enum": ["public", "private", "internal"]},
        "html_url": {"type": "string"},
        "updated_at": {"type": "string"},
    },
    "additionalProperties": True
}

PUBLIC_USER_SCHEMA = {
    "type": "object",
    "required": ["login", "id"],
    "properties": {
        "login": {"type": "string"},
        "id": {"type": "number"},
        "type": {"type": "string"}
    }
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
                    "code": {"type": "string"},
                    "field": {"type": "string"},
                    "message": {"type": "string"}
                }
            }
        }
    },
    "additionalProperties": True
}

EMAIL_ERROR_SCHEMA = {
    "type": "object",
    "required": ["message", "documentation_url", "status"],
    "properties": {
        "message": {"type": "string"},
        "documentation_url": {"type": "string"},
        "status": {"type": "string"}
    }
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

UNAUTHORIZED_ERROR_SCHEMA = {
    "type": "object",
    "properties": {
        "message": {"type": "string"},
        "documentation_url": {"type": "string"}
    },
    "required": ["message"],
    "additionalProperties": True
}

ERROR_VALIDATION_SCHEMA = {
    "type": "object",
    "properties": {
        "message": {"type": "string"},
        "errors": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "resource": {"type": "string"},
                    "code": {"type": "string"},
                    "field": {"type": "string"},
                    "message": {"type": "string"}
                },
                "required": ["resource", "code", "field"]
            }
        },
        "documentation_url": {"type": "string"}
    },
    "required": ["message", "errors"],
    "additionalProperties": True
}

ERROR_NOT_FOUND_SCHEMA = {
    "type": "object",
    "properties": {
        "message": {"type": "string"},
        "documentation_url": {"type": "string"},
        "status": {"type": "string"}
    },
    "required": ["message", "documentation_url"],
    "additionalProperties": True
}

CREATE_COMMENT_SCHEMA = {
    "type": "object",
    "properties": {
        "id": {"type": "integer"},
        "node_id": {"type": "string"},
        "url": {"type": "string"},
        "html_url": {"type": "string"},
        "body": {"type": "string"},
        "user": {"type": "object"},
        "created_at": {"type": "string"},
        "updated_at": {"type": "string"}
    },
    "required": ["id", "body", "user", "created_at"],
    "additionalProperties": True
}

PULL_REQUEST_SCHEMA = {
    "type": "object",
    "required": ["id", "number", "title", "state", "url", "html_url"],
    "properties": {
        "id": {"type": "integer"},
        "number": {"type": "integer"},
        "title": {"type": "string"},
        "body": {"type": ["string", "null"]},
        "state": {"type": "string", "enum": ["open", "closed"]},
        "url": {"type": "string"},
        "html_url": {"type": "string"},
        "merged": {"type": ["boolean", "null"]},
        "draft": {"type": "boolean"},
        "created_at": {"type": "string"},
        "updated_at": {"type": "string"},
        "head": {"type": "object"},
        "base": {"type": "object"},
        "user": {"type": "object"},
    },
    "additionalProperties": True,
}

UPDATE_PR_SCHEMA = {
    "type": "object",
    "required": ["id", "number", "title", "state"],
    "properties": {
        "id": {"type": "integer"},
        "number": {"type": "integer"},
        "title": {"type": "string"},
        "body": {"type": ["string", "null"]},
        "state": {"type": "string", "enum": ["open", "closed"]},
        "merged": {"type": ["boolean", "null"]},
        "updated_at": {"type": "string"},
    },
    "additionalProperties": True,
}

PR_LABELS_SCHEMA = {
    "type": "array",
    "items": {
        "type": "object",
        "required": ["id", "name", "color"],
        "properties": {
            "id": {"type": "integer"},
            "name": {"type": "string"},
            "color": {"type": "string"},
            "url": {"type": "string"},
            "default": {"type": "boolean"},
        },
    },
}

PR_NOT_FOUND_SCHEMA = {
    "type": "object",
    "required": ["message"],
    "properties": {
        "message": {"type": "string"},
        "documentation_url": {"type": "string"},
    },
    "additionalProperties": True,
}

PR_VALIDATION_ERROR_SCHEMA = {
    "type": "object",
    "required": ["message"],
    "properties": {
        "message": {"type": "string"},
        "documentation_url": {"type": "string"},
    },
    "additionalProperties": True,
}
