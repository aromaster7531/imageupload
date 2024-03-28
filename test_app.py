from app import app, S3_ACCESS_KEY, S3_SECRET_KEY

import pytest


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_index(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Upload Image' in response.data

def test_upload_file_no_file(client):
    response = client.post('/upload')
    assert response.status_code == 200
    assert b'File is empty' in response.data

def test_upload_file_empty_filename(client):
    data = {'file': ''}
    response = client.post('/upload', data=data)
    assert response.status_code == 200
    assert b'File is empty' in response.data

