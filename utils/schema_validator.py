from jsonschema import ValidationError, validate


def validate_schema(data, schema):
    try:
        validate(instance=data, schema=schema)
        return True
    except ValidationError:
        return False