"""
This is a py file that will contain the functions used for security
meaning LDAP implementation, encoding, decoding, hashing, etc.

Make class to contain functions for encoding and storing commands
to be executed on main.py
"""
import base64

class Secure:
    """Classification for incuding sercurity functions"""
    # def __init__(self):

    def decodedData(self, b64EncodedData):
        """Decode encoded data when received"""
        decodedBytes = base64.b64decode(b64EncodedData)
        print(decodedBytes)
        with open("exampleSaveData.md", "w") as file:
            file.write(decodedBytes.decode("UTF-8"))


    def encodeFile(self, pathToFile):
        """Encode file before sending it off to server"""
        data = open(pathToFile, "r").read()
        with open(pathToFile, "r") as file:
            encoded = base64.b64encode(bytes(file.read(), "UTF-8"))
            print(data)
            print(encoded)
            # decodedData(encoded) Make this function call work


    # Press the green button in the gutter to run the script.
    if __name__ == '__main__':
        tempFilePath = "/home/parallels/Documents/file-management-app/README.md"
        encodeFile(tempFilePath)

    # def decodeFile(b64data):
    #     decoded = base64.b64decode(b64data)
    #     f = open('exampleSaveData.md', 'w')
    #     f.write(decoded)
    #     f.close()
    #     print(decoded)

    # def encodeFile(pathToFile):
    #     data = open(pathToFile, 'r').read()
    #     encoded = base64.b64encode(data)
    #     print(data)
    #     print(encoded)
    #     decodeFile(encoded)

    # if __name__ == "__main__":
    #     tempfilepath = '/home/parallels/Documents/file-management-app/README.md'
    #     encodeFile(tempfilepath)
