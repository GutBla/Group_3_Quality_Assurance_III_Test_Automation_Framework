import pytest
import os
from unittest.mock import MagicMock, patch
from services.request_manager import RequestManager

def test_request_manager_singleton():
    rm1 = RequestManager()
    rm2 = RequestManager()
    assert rm1 is rm2

def test_log_response_non_json():
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.side_effect = ValueError("No es JSON")
    
    rm = RequestManager()
    rm._log_response(mock_response)

def test_initialize_missing_token():
    with patch.dict(os.environ, {}, clear=True):
        RequestManager._instance = None 
        with pytest.raises(EnvironmentError, match="ACCESS_TOKEN no está configurado."):
            RequestManager()

def test_request_manager_methods():
    rm = RequestManager()
    rm.session = MagicMock() 
 
    rm.patch("http://test.url", json={"test": "data"})
    rm.session.patch.assert_called()
    
    rm.head("http://test.url")
    rm.session.head.assert_called()