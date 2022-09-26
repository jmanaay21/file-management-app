"""
This test is just an internal example of how each
function would be laid out and work within the server
as well as how the encoding and decoding might be laid out

TO DO:
- Move encode and decode to seperate file
    (maybe even a seperate class)
- Add different users/ access control
- Implement encode and decode functions to
    add to file tables from python script
"""
import base64
from getpass import getpass
from mysql.connector import connect, Error

try:
    with connect(
        # Setting up connection to server database
        host="localhost",
        user=input("Enter username: "),
        password=getpass("Enter password: "),
        database="fileserver"
    ) as connection:
        with connection.cursor() as cursor:
            # Moves to the fileserver table
            cursor.execute("USE fileserver")

            # Describes the contents of file_store table
            # and displays information
            cursor.execute("DESCRIBE file_store")
            myresult = cursor.fetchall()
            for x in myresult:
                print(x)
except Error as e:
    print(e)

def file_info():
    """Get user info and store it for mysql use"""
    file_name = input("Insert file name with extension (Include the dot): ")
    file_name.split('.')
    pathToFile = input("Insert file path to encode and upload:\n")


# Refactor this to input path file to upload
def decodedData(b64EncodedData):
    """Decode encoded data when received"""
    decodedBytes = base64.b64decode(b64EncodedData)
    print(decodedBytes)
    with open("exampleSaveData.md", "w") as file:
        file.write(decodedBytes.decode("UTF-8"))


def encodeFile(pathToFile):
    """Encode file before sending it off to server"""
    data = open(pathToFile, "r").read()
    with open(pathToFile, "r") as file:
        encoded = base64.b64encode(bytes(file.read(), "UTF-8"))
        print(data)
        print(encoded)
        decodedData(encoded)
