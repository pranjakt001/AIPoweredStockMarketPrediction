"""
Error handling utilities
"""

from flask import jsonify
import logging
from functools import wraps

logger = logging.getLogger(__name__)

class APIError(Exception):
    """Base API Exception"""
    status_code = 500

    def __init__(self, message, status_code=None, payload=None):
        super().__init__()
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['status'] = 'error'
        rv['message'] = self.message
        return rv

class ValidationError(APIError):
    """Validation error"""
    status_code = 400

class NotFoundError(APIError):
    """Resource not found error"""
    status_code = 404

class ServerError(APIError):
    """Internal server error"""
    status_code = 500

def handle_api_error(error):
    """Handle API errors"""
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

def handle_generic_error(error):
    """Handle generic errors"""
    logger.error(f"Unhandled error: {str(error)}")
    response = jsonify({
        'status': 'error',
        'message': 'Internal server error'
    })
    response.status_code = 500
    return response

def safe_api_call(f):
    """Decorator for safe API calls with error handling"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except APIError as e:
            logger.error(f"API Error in {f.__name__}: {e.message}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error in {f.__name__}: {str(e)}")
            raise ServerError(f"An unexpected error occurred: {str(e)}")
    return decorated_function
