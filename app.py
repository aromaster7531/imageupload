from flask import Flask, request, jsonify, render_template
import boto3
import os

app = Flask(__name__)

S3_BUCKET_NAME = 'imagebucketfile'
S3_REGION = 'us-east-1'
S3_ACCESS_KEY = os.environ.get('AWS_ACCESS_KEY_ID')
S3_SECRET_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'File is empty'})

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'Invalid Filename'})

    try:
        s3_client = boto3.client('s3', region_name=S3_REGION,
                                 aws_access_key_id=S3_ACCESS_KEY,
                                 aws_secret_access_key=S3_SECRET_KEY)
        
        s3_client.upload_fileobj(file, S3_BUCKET_NAME, file.filename)

        return jsonify({'message': 'File uploaded to the S3 Bucket'})
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)

