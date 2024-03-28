from flask import Flask, request, jsonify, render_template, session, redirect, url_for

import boto3
import os


S3_BUCKET_NAME = 'imagebucketfile'
S3_REGION = 'us-east-1'
S3_ACCESS_KEY = os.environ.get('AWS_ACCESS_KEY_ID')
S3_SECRET_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Set a secret key for session management

# User database (replace with a real database in production)
users = {'user1': 'password1', 'user2': 'password2'}

@app.route('/')
def index():
    if 'username' in session:
        return render_template('index.html', username=session['username'])
    else:
        return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username] == password:
            session['username'] = username
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error='Invalid username or password')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))


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

