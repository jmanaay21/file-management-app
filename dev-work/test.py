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

from mysql.connector import Error, connect


def main():
    """Main function to run"""
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

                # Get user info to prepare to uplaod data into server
                user_args = int(input("\nWhat would you like to do?\n"
                + "1 for upload, 2 for download, 3 for delete: "))

                # Choose action for database
                database_action(user_args)

    except Error as e:
        print(e)


def file_info():
    """Get user info and store it for mysql use"""
    file_name = input("\nInsert file name: ")
    file_ext = input("Insert file extension: ")
    file_ext = "." + file_ext
    file_path = input("Insert file path to encode and upload:\n")

    print('\nHere is your file staged to upload:')
    print(f'file: {file_name}{file_ext}\n'
        + f'file path: {file_path}')

# Function to decide whether to upload or delete from database
def database_action(user_args):
    """Case function decides to up, down or delete, 
    once case is decided, user access should be checked"""
    match user_args:
        case 1:
            print('option 1, upload:')
            file_info()
            
        case 2:
            return 'option 2, download:'

        case 3:
            return 'option 3, delete:'


# Refactor this to input path file to upload
def decodedData(b64EncodedData):
    """Decode encoded data when received"""
    decodedBytes = base64.b64decode(b64EncodedData)
    print(decodedBytes)
    with open("exampleSaveData.md", "w") as file:
        file.write(decodedBytes.decode("UTF-8"))


def encodeFile(file_path):
    """Encode file before sending it off to server"""
    data = open(file_path, "r").read()
    with open(file_path, "r") as file:
        encoded = base64.b64encode(bytes(file.read(), "UTF-8"))
        print(data)
        print(encoded)
        decodedData(encoded)

if __name__ == '__main__':
    main()
