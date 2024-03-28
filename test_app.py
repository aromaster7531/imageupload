from app import app, S3_ACCESS_KEY, S3_SECRET_KEY

import pytest


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


def test_index(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Upload Image' in response.data

def test_s3_credentials():
    print("S3_ACCESS_KEY:", S3_ACCESS_KEY)
    print("S3_SECRET_KEY:", S3_SECRET_KEY)

def test_upload_file(client):
    data = {'file': (open('test.jpg', 'rb'), 'test.jpg')}
    response = client.post('/upload', data=data, content_type='multipart/form-data')
    assert response.status_code == 200
    assert b'File uploaded successfully!' in response.data
