from app import app

import pytest


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


def test_index(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Upload Image' in response.data


def test_upload_file(client):
    data = {'file': (open('test.jpg', 'rb'), 'test.jpg')}
    response = client.post('/upload', data=data, content_type='multipart/form-data')
    assert response.status_code == 200
    assert b'File uploaded successfully!' in response.data
