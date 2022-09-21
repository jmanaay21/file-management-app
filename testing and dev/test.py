from flask import Flask
import json
import base64



app = Flask(__name__)

@app.route('/files')
def listFiles():
    return json.dumps('{“Files”:[“File1”: “Something.docx”,“File2”: “SomethingElse.xlsx]}')

@app.route('/upload', methods=['POST'])
def uploadFile():
    """
    Determine what to do with the payload
    Determine how to save a file
    Determine the format of the post function
    They are passing the data, parse through data
    """
    return 'File successfully loaded'

@app.route('/download')
def downloadFile():
    """
    Really only need file name as key, client will decode
    Decide what object format is gonna look like
    Need byte representation of the file
    """
    return 'To Do: return object representing as file'

@app.route('/delete', method=['DELETE'])
def deleteFile():
    """
    
    """
    return ''

def encodeFile(pathToFile):
    data = open(pathToFile, 'r').read()
    encoded = base64.b64encode(data)
    print(data)
    print(encoded)
    decodeFile(encoded)

def decodeFile(b64data):
    decoded = base64.b64decode(b64data)
    f = open('exampleSaveData.md', 'w')
    f.write(decoded)
    f.close()
    print(decoded)

@app.route('/testingcoding')
def testingCode():
    tempfilepath = '/home/parallels/Documents/file-management-app/README.md'
    encodeFile(tempfilepath)
    return 'finished'