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