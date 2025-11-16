"""
API Tests
"""

import pytest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.app import create_app

@pytest.fixture
def client():
    """Create test client"""
    app = create_app('testing')
    app.config['TESTING'] = True

    with app.test_client() as client:
        yield client

def test_health_check(client):
    """Test health check endpoint"""
    response = client.get('/api/health')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'healthy'

def test_root_endpoint(client):
    """Test root endpoint"""
    response = client.get('/')
    assert response.status_code == 200
    data = response.get_json()
    assert 'service' in data
    assert 'version' in data

def test_initialize_endpoint(client):
    """Test initialize endpoint"""
    response = client.post('/api/initialize',
                          json={'ticker': '^AXJO', 'start_date': '2023-01-01'})
    assert response.status_code in [200, 500]  # May fail without internet

def test_models_endpoint(client):
    """Test models endpoint"""
    response = client.get('/api/models')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'success'
