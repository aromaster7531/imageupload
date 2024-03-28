# tests/test_app.py

import os
import tempfile
import pytest
from app import app

@pytest.fixture
def client():
    # Set up a temporary file to store uploaded images
    app.config['TESTING'] = True
    app.config['UPLOAD_FOLDER'] = tempfile.mkdtemp()
    client = app.test_client()

    # Ensure the application context is pushed when testing
    with app.app_context():
        yield client

def test_upload(client):
    # Simulate a file upload request
    data = {'file': (open('test_image.jpg', 'rb'), 'test_image.jpg')}
    response = client.post('/upload', data=data, content_type='multipart/form-data')

    # Check if the response is successful (HTTP status code 200)
    assert response.status_code == 200

    # Check if the uploaded file exists in the temporary upload folder
    assert os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], 'test_image.jpg'))

    # Clean up - delete the uploaded file
    os.remove(os.path.join(app.config['UPLOAD_FOLDER'], 'test_image.jpg'))

    # You can add more assertions to validate the response content if needed
