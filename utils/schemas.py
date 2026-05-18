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