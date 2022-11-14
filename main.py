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
import shutil
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
                cursor.execute(f"DESCRIBE file_store")
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
                        print('\nOption 1, upload:')

                        # Set upload value up temporarily to allow file transfer
                        cursor.execute("SET GLOBAL max_allowed_packet=1073741824;")
                        cursor.execute(upload())

                        cursor.execute("SELECT * FROM TABLE file_store")

                    case 2:
                        print('\n\nOption 2, download:\n')

                        cursor.execute(download())


                    case 3:
                        return 'option 3, delete:'
                            # Choose action for database

                cursor.close()
    except Error as e:
        print(e)

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

    # Copy file into current directory
    shutil.copy(file_path, f"./{file_name}.{file_ext}")

    stage_file = f'./{file_name}.{file_ext}'

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
    with open(f'{stage_file}', 'rb') as file:
        original = file.read()

    # Encrypting the actual file
    enc_data = fernet.encrypt(original)

    # Opening file in write mode and encrypting data
    with open(f'{stage_file}', 'wb') as encrypted_file:
        encrypted_file.write(enc_data)

    upload_command = f"INSERT INTO file_store (filename, extension, filecontent) "\
        f"VALUES (\'{file_name}\', \'{file_ext}\', LOAD_FILE(\'{stage_file}\'));"

    print(upload_command)
    return upload_command

def download():
    print()
    return "(Download command from my sql)"


if __name__ == '__main__':
    main()
