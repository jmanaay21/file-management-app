"""
Main program in which we will run build from
"""
import ldap
from getpass import getpass
import shutil
from getpass import getpass
from cryptography.fernet import Fernet
from mysql.connector import Error, connect
from devwork.server_commands import *

# Dealing with ldap first for authentification before initializing
# connection to mysql server
def user_login():
    is_authenticated = False
    ldapconn = ldap.initialize('ldap://localhost')

    ID = ""

    cn = input("Enter Username: ")
    user = f'uid={cn},ou=People,dc=fileserver,dc=net'
    userpass = getpass("Enter Password: ")

    # Making vars for search_s function
    baseDN = "dc=fileserver,dc=net"
    search_scope = ldap.SCOPE_SUBTREE

    # Determine if user is authenticated
    try:
        ldapconn.simple_bind_s(user, userpass)
        is_authenticated = True
        print(f"\nUser {cn} successfully logged in.")
    except:
        print("\nError authenticating user, please try again.\n")

    usercn = f"uid={cn}"

    # Look up user gid/uid number (This will be for method access control)
    UID = ldapconn.search_s(baseDN, search_scope, usercn, ['gidNumber'])
    UID = str(UID)

    for n in UID:
        if n.isdecimal():
            ID = ID + n
    if is_authenticated: print(f"Welcome {cn}, you are goupID number {ID}.\n")
    return ID, is_authenticated

# Once authenticated, server function will run
def server_use():
    """
    user_cred is a tuple that contains gidNum and 
    """
    user_cred = user_login()
    # Setting variables for easier readability
    is_authenticated = user_cred[1]
    user_gidnum = user_cred[0]
    
    if is_authenticated:
        try:
            with connect(
                # Setting up connection to server database
                host="localhost",
                user=("root"),
                password=("Moomoo22@"),
                database="fileserver"
            ) as connection:
                with connection.cursor(buffered=True) as cursor:
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
                            if user_gidnum == '5000':
                                print('\nOption 1, upload:')

                                # Set upload value up temporarily to allow file transfer
                                cursor.execute("SET GLOBAL max_allowed_packet=1073741824;")
                                cursor.execute(upload())
                                connection.commit()

                                cursor.execute("SELECT fileid, filename, extension FROM fileserver.file_store;")
                                connection.commit()
                                table_contents = cursor.fetchall()
                                for x in table_contents:
                                    print(x)

                            else:
                                print("\nYou are not authorized to upload.\n")
                                exit()

                        case 2:
                            if user_gidnum == '4000' or user_gidnum == '5000':
                                print('\n\nOption 2, download:\n')

                                cursor.execute("SELECT fileid, filename, extension FROM fileserver.file_store;")
                                connection.commit()
                                table_contents = cursor.fetchall()
                                for x in table_contents:
                                    print(x)

                                cursor.execute(download())
                                file_contents = cursor.fetchall()
                                create_file(file_contents)
                                connection.commit()

                            else:
                                print("\nYou are not authorized to download.\n")
                                exit()

                        case 3:
                            if user_gidnum == '5000':
                                print('\n\nOption 3, delete:\n')

                                cursor.execute("SELECT fileid, filename, extension FROM fileserver.file_store;")
                                connection.commit()
                                table_contents = cursor.fetchall()
                                for x in table_contents:
                                    print(x)
                                
                                cursor.execute(delete())
                                connection.commit()


                            else:
                                print("\nYou are not authorized to delete.\n")
                                exit()

                    cursor.close()
        except Error as e:
            print(e)
    else:
        print("\nUser not authenticated, please try again.\n")

# def upload():
#     """
#     Get user info and store it for mysql use and
#     create mysql string for uploading to server
#     """
#     file_name = input("\nInsert file name: ")
#     file_ext = input("Insert file extension: ")
#     # file_ext = "." + file_ext
#     file_path = input("Insert file path to encode and upload:\n")

#     print('\nHere is your file staged to upload:')
#     print(f'file: {file_name}.{file_ext}\n'
#     + f'file path: {file_path}\n\n')

#     # Copy file into current directory
#     shutil.copy(file_path, f"./{file_name}.{file_ext}")

#     stage_file = f'./{file_name}.{file_ext}'

#     # Opening the key
#     with open('filekey.key', 'rb') as filekey:
#         key = filekey.read()

#     # Using the generated key
#     fernet = Fernet(key)

#     # Open the original file to encrypt
#     with open(f'{stage_file}', 'rb') as file:
#         original = file.read()

#     # Encrypting the actual file
#     enc_data = fernet.encrypt(original)

#     # Opening file in write mode and encrypting data
#     with open(f'{stage_file}', 'wb') as encrypted_file:
#         encrypted_file.write(enc_data)

#     contents = open(stage_file, 'r').read()
    
#     upload_command = f"INSERT INTO file_store (filename, extension, filecontent) "\
#         f"VALUES (\'{file_name}\', \'{file_ext}\', \'{contents}\');"

#     return upload_command

# def download():
#     fileid = input("\nIn localhost/list_files.php there is the current database shown.\nWhich file in the table would you like to download? (Use fileid): ")
#     download_command = f"SELECT filename, extension, filecontent from file_store where fileid={fileid};"
#     return download_command

# def delete():
#     """
#     List table for users to see, ask for which row they would want to delete
#     Ask if they are sure again, return the command to delete into main
#     """
#     fileid = input("\nIn localhost/list_files.php there is the current database shown.\nWhich file in the table would you like to delete?(Use fileid): ") 
#     delete_command = f"DELETE FROM file_store WHERE fileid={fileid};"
#     return delete_command

# def create_file(file_contents):
#     file_contents_split = str(file_contents).split(", ")
#     file_name = file_contents_split[0]
#     file_ext = file_contents_split[1]
#     file_content = file_contents_split[2]

#     # Format strings to stage for file making
#     file_name = file_name.replace("[(", "")
#     file_name = file_name.replace("'", "")

#     file_ext = file_ext.replace("'", "")

#     file_content = file_content[:-3]
#     file_content = file_content[2:]

#     stage_file = f"{file_name}.{file_ext}"
#     print(f"\nFile name: {file_name}\nFile ext: {file_ext}\nFile content: {file_content}")
#     # Creating file
#     new_file = open(f"{file_name}.{file_ext}", "w")
#     new_file.write(file_content)
#     new_file.close()

#     # Actually using key to decrypt file
#     with open('filekey.key', 'rb') as filekey:
#         key = filekey.read()

#     fernet = Fernet(key)

#     with open(stage_file, 'rb') as enc_file:
#         encrypted = enc_file.read()

#     decrypted = fernet.decrypt(encrypted)

#     with open(stage_file, 'wb') as dec_file:
#         dec_file.write(decrypted)


if __name__ == "__main__":
    server_use()