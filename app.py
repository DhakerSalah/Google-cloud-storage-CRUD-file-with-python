from flask import Flask, send_file, request
from google.cloud import storage
from google.auth import default
import os

app = Flask(__name__)
storage_client = storage.Client.from_service_account_json(os.path.abspath("file.json"))
my_bucket = 'bucketName'
bucket = storage_client.bucket(my_bucket)

@app.route('/list')
def get_list():
    arrayFiles = [] 
    # blobs = bucket.list_blobs(prefix='folderName/') if your file exist in folder
    blobs = bucket.list_blobs()
    for blob in blobs:
        # if not blob.name.endswith('/'):   #for getting only files in this folder without "folderName/"
            print(blob.name)
            arrayFiles.append(blob.name)
    return arrayFiles

@app.route('/getFile/<name>')
def get_file(name):
    # blob = bucket.blob("desktop/" + name) # if your file exist in folder
    blob = bucket.blob(name)
    if blob.exists():
        blobName = blob.name
        # file_split = blobName.split("/")[1] # folder/file.txt => file.txt
        print(blobName)
    else:
        blobName = "File does not exist"
    return blobName

@app.route('/getContent/<name>')
def get_file_content(name):
    # blob = bucket.blob("desktop/" + name) # if your file exist in folder
    blob = bucket.blob(name)
    if blob.exists():
        content = blob.download_as_text()
        print(content)
    else:
        content = "File does not exist"
    return content

@app.route('/post', methods=['POST'])
def upload_file():
    try:
        uploaded_file = request.files.get('myfile')
        filename = uploaded_file.filename
        blob = bucket.blob(filename) # post file with his name
        blob.upload_from_string(uploaded_file.read())
        return filename
    except Exception as e:
        return str(e)

@app.route('/delete/<name>', methods=['delete'])
def delete_file(name):
    try:
        blob = bucket.blob(name)
        if blob.exists():
            blob.delete()
            message = "Successfully file deleted"
        else:
            message = "File does not exist"
        return message
    except Exception as e:
        return str(e)

if __name__ == '__main__':
    app.run(debug = True, port = 6000)