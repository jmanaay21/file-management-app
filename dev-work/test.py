"""
This test is just an internal example of how each
function would be laid out and work within the server
as well as how the encoding and decoding might be laid out

TO DO:
- Move encode and decode to seperate file
    (maybe even a seperate class)
- Add different users/ access control (LDAP)
- Implement encode and decode functions to
    add to file tables from python
- Create strinf builder for a sql command
    so user doesn't have direct access to
    inserting mysql commands

STRUCTURE
Upload:
- Take parameters
- Read and encode file
- Encrypt file contents
- Make sql command to store info in server
- Execute command
"""
import base64
from getpass import getpass
from cryptography.fernet import Fernet
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

                # Case function decides to up, down or delete,
                # once case is decided, user access should be checked
                match user_args:
                    case 1:
                        print('option 1, upload:')
                        
                        cursor.execute(upload())

                        cursor.execute("SELECT * FROM TABLE file_store")

                    case 2:
                        return 'option 2, download:'

                    case 3:
                        return 'option 3, delete:'
                            # Choose action for database

                cursor.close()
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

    encodeFile(file_path)

    return file_name, file_ext, file_path

# Refactor this to input path file to upload
def decodedData(b64EncodedData):
    """Decode encoded data when received"""
    decodedBytes = base64.b64decode(b64EncodedData)
    print(decodedBytes)
    with open("exampleSaveData.md", "w") as file:
        file.write(decodedBytes.decode("UTF-8"))


def encodeFile(encData):
    """Encode file before sending it off to server"""
    data = open(encData, "r").read()
    with open(encData, "r") as file:
        encoded = base64.b64encode(bytes(file.read(), "UTF-8"))
        print(data)
        print(encoded)
        decodedData(encoded)

        return encoded

# how-to-encrypt-and-decrypt-strings-in-python

def upload():
    """
    Get user info and store it for mysql use and
    create mysql string for uploading to server
    """
    file_name = input("\nInsert file name: ")
    file_ext = input("Insert file extension: ")
    # file_ext = "." + file_ext
    file_path = input("Insert file path to encode and upload:\n")

    print('\nHere is your file staged to upload:')
    print(f'file: {file_name}.{file_ext}\n'
    + f'file path: {file_path}\n\n')

    data = open(file_path, "r", encoding="utf8").read()

    # Key generation and keep in file
    key = Fernet.generate_key()
    with open('filekey.key', 'wb') as filekey:
        filekey.write(key)

    # Opening the key
    with open('filekey.key', 'rb') as filekey:
        key = filekey.read()

    # Using the generated key
    fernet = Fernet(key)

    # Open the original file to encrypt
    with open(f'{file_path}', 'rb') as original_file:
        original = original_file.read()

    # Encrypting the actual file
    encrypted = fernet.encrypt(original)

    # Opening file in write mode and encrypting data
    with open(f'enc_{file_name}.{file_ext}', 'wb') as encrypted_file:
        encrypted_file.write(encrypted)

    #DEBUG (Byte to String datatype change)
    encData = str(encrypted)

    # encode encData as base64
    enc_bytes = encData.encode('ascii')
    base64_bytes = base64.b64encode(enc_bytes)
    base64_encData = base64_bytes.decode('ascii')


    # Remove the '==' from the string, make sure to add back in on the download function
    size = len(base64_encData)
    staged_b64_encData = base64_encData[: size - 2]

    print(f"\n\n\nenc_Bytes: {enc_bytes}\n\nbase64_bytes: {base64_bytes}\n\nbase64_encData: {base64_encData}\n\nStaged_b64_encData: {staged_b64_encData}\n\n")

    upload_command = f"INSERT INTO file_store (filename, extension, filecontent) "\
        f"VALUES (\"{file_name}\", \"{file_ext}\", \"{encrypted}\");"

    return upload_command



if __name__ == '__main__':
    main()
