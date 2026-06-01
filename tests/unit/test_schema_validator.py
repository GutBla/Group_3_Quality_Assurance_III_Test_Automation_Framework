import pytest

from utils import schemas
from utils.schema_validator import validate_schema

test_data_map = [
    (schemas.LABEL_SCHEMA, {
        "id": 1, "name": "bug", "color": "f00", "url": "x", "default": True}), (schemas.LABEL_ERROR_SCHEMA, {
            "message": "error", "documentation_url": "url"}), (schemas.ASSIGN_LABELS_SCHEMA, [
                {
                    "id": 1, "name": "bug", "color": "f00", "url": "x"}]), (schemas.CREATE_ISSUE_SCHEMA, {
                        "id": 1, "number": 1, "title": "t", "body": "b", "state": "open", "url": "x", "repository_url": "x", "created_at": "x", "updated_at": "x"}), (schemas.UPDATE_PROFILE_SCHEMA, {
                            "login": "user", "id": 1}), (schemas.CREATE_REPO_SCHEMA, {
                                "id": 1, "name": "n", "full_name": "f", "private": True, "owner": {
                                    "login": "o", "id": 1}, "html_url": "x", "description": "d", "url": "x", "has_issues": True, "visibility": "public", "created_at": "x", "default_branch": "m"}), (schemas.AUTH_USER_SCHEMA, {
                                        "login": "u", "id": 1}), (schemas.UPDATE_REPO_SCHEMA, {
                                            "id": 1, "name": "n", "full_name": "f", "private": True, "description": "d", "visibility": "public"}), (schemas.PUBLIC_USER_SCHEMA, {
                                                "login": "u", "id": 1, "type": "User"}), (schemas.ERROR_REPO_SCHEMA, {
                                                    "message": "m", "errors": []}), (schemas.EMAIL_ERROR_SCHEMA, {
                                                        "message": "m", "documentation_url": "u", "status": "s"}), (schemas.ERROR_VALIDATION_ISSUE_SCHEMA, {
                                                            "message": "m"}), (schemas.UPDATE_ISSUE_SCHEMA, {
                                                                "id": 1, "number": 1, "title": "t", "body": "b", "state": "open", "url": "x", "repository_url": "x", "created_at": "x", "updated_at": "x"}), (schemas.NOT_FOUND_ISSUE_SCHEMA, {
                                                                    "message": "m"}), (schemas.UNAUTHORIZED_ERROR_SCHEMA, {
                                                                        "message": "m"}), (schemas.ERROR_VALIDATION_SCHEMA, {
                                                                            "message": "m", "errors": []}), (schemas.ERROR_NOT_FOUND_SCHEMA, {
                                                                                "message": "m", "documentation_url": "u"}), (schemas.CREATE_COMMENT_SCHEMA, {
                                                                                    "id": 1, "body": "b", "user": {}, "created_at": "x"})]


@pytest.mark.parametrize("schema, data", test_data_map)
def test_all_schemas_validation(schema, data):
    assert validate_schema(data, schema) is True


def test_schema_validation_failure():
    invalid_data = {"message": "error"}
    assert validate_schema(invalid_data, schemas.LABEL_ERROR_SCHEMA) is False
