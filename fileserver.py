"""
Main program in which we will run build from
"""
import ldap
import logging
from getpass import getpass
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
        logging.info(f"User {cn} has logged into the server")
    except:
        logging.warning(f"User {cn} failed authentication")
        print("\nError authenticating user, please try again.\n")

    usercn = f"uid={cn}"

    # Look up user gid/uid number (This will be for method access control)
    UID = ldapconn.search_s(baseDN, search_scope, usercn, ['gidNumber'])
    UID = str(UID)

    for n in UID:
        if n.isdecimal():
            ID = ID + n
    if is_authenticated: 
        logging.info(f"{cn} has logged in with GID {ID}")
        print(f"Welcome {cn}, you are groupID number {ID}.\n")
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
        # Use mysql pasword if autheticated
        with open('filekey.key', 'rb') as filekey:
            key = filekey.read()
        fernet = Fernet(key)

        with open('mysqlpass.txt', 'rb') as enc_file:
            encrypted = enc_file.read()
        sqlpass = fernet.decrypt(encrypted)
        sqlpass = str(sqlpass)
        sqlpass = sqlpass[2:-1]
        sqlpass = sqlpass + '@'

        try:
            with connect(
                # Setting up connection to server database
                host="localhost",
                user=("root"),
                password=(sqlpass),
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
                                print(f"\nFile successfully uploaded to server.\n")
                                logging.info('File has been uploaded to database')

                            else:
                                logging.warning("Unauthorized upload attempt")
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

                                print("\nFile successfully downloaded, check current directory.\n")
                                logging.info('File has been downloaded from database')

                            else:
                                logging.warning("Unuthorized download attempt")
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

                                print("\nFile successfully deleted, check localhost/list_files.php for list of file in database\n")
                                logging.info('File has been deleted from database')
                            else:
                                logging.warning("Unauthorized delete attempt")
                                print("\nYou are not authorized to delete.\n")
                                exit()

                    cursor.close()
        except Error as e:
            print(e)
            logging.error(f'{e}')
    else:
        print("\nUser not authenticated, please try again.\n")
        logging.warning('Unauthenticated access attempt')


if __name__ == "__main__":
    logging.info('Application sesstion initialized')
    server_use()
    logging.info('Application session ended')