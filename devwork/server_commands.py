import shutil
import logging
from cryptography.fernet import Fernet

logging.basicConfig(
    level=logging.INFO,
    format="{asctime} {levelname:<8} {message}",
    style='{',
    filename='%slog' % __file__[-2],
    filemode='a'
)
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

    contents = open(stage_file, 'r').read()
    
    upload_command = f"INSERT INTO file_store (filename, extension, filecontent) "\
        f"VALUES (\'{file_name}\', \'{file_ext}\', \'{contents}\');"
    
    logging.info(f"File {file_name} uploaded")

    return upload_command

def download():
    fileid = input("\nIn localhost/list_files.php there is the current database shown.\nWhich file in the table would you like to download? (Use fileid): ")
    download_command = f"SELECT filename, extension, filecontent from file_store where fileid={fileid};"
    return download_command

def delete():
    """
    List table for users to see, ask for which row they would want to delete
    Ask if they are sure again, return the command to delete into main
    """
    fileid = input("\nIn localhost/list_files.php there is the current database shown.\nWhich file in the table would you like to delete?(Use fileid): ") 
    delete_command = f"DELETE FROM file_store WHERE fileid={fileid};"
    return delete_command

def create_file(file_contents):
    file_contents_split = str(file_contents).split(", ")
    file_name = file_contents_split[0]
    file_ext = file_contents_split[1]
    file_content = file_contents_split[2]

    # Format strings to stage for file making
    file_name = file_name.replace("[(", "")
    file_name = file_name.replace("'", "")

    file_ext = file_ext.replace("'", "")

    file_content = file_content[:-3]
    file_content = file_content[2:]

    stage_file = f"{file_name}.{file_ext}"
    # Creating file
    new_file = open(f"{file_name}.{file_ext}", "w")
    new_file.write(file_content)
    new_file.close()
    logging.info(f"File {file_name} created")

    # Actually using key to decrypt file
    with open('filekey.key', 'rb') as filekey:
        key = filekey.read()

    fernet = Fernet(key)

    with open(stage_file, 'rb') as enc_file:
        encrypted = enc_file.read()

    decrypted = fernet.decrypt(encrypted)

    with open(stage_file, 'wb') as dec_file:
        dec_file.write(decrypted)
