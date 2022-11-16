import ldap
from getpass import getpass
import sys


#Stuff needed in beginning of the code
LDAP_SERVER = 'ldap://localhost'
BASE_DN = 'dc=fileserver,dc=net'  # base dn to search in

#login for username and password, to be passed into the ldapConnection function
LDAP_LOGIN = input('Enter your ldap login: ')
LDAP_PASSWORD = getpass('Enter your ldap password: ')

def ldapConnection(LDAP_LOGIN, LDAP_PASSWORD):
    connect = ldap.initialize(LDAP_SERVER)
    if connect:  #connects to server
        print("Connection initialized")
    else: 
        ldap.SERVER_DOWN
        print("Can't connect to LDAP server")
        exit(4)
    
    y = connect.simple_bind_s(LDAP_LOGIN, LDAP_PASSWORD)    #login for user
    print(y)
    exit()
    if (ldap.INVALID_CREDENTAILS):
        print("Invalid login and/or password")
        exit(3)
    ATTRIBUTES_TO_SEARCH = ['memberOf']
    OBJECT_TO_SEARCH = 'userPrincipalName=user@example.com'
    connect.set_option(ldap.OPT_REFERRALS, 0)  # to search the object and all its descendants
    result = connect.search_s(BASE_DN, ldap.SCOPE_SUBTREE, OBJECT_TO_SEARCH, ATTRIBUTES_TO_SEARCH)  #searches through ldap
    return result   #This needs to return a group id so we can use it for authorization in the code

ldapConnection(LDAP_LOGIN, LDAP_PASSWORD)
