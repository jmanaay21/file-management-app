import ldap3

<<<<<<< HEAD
#Stuff needed in beginning of the code
LDAP_SERVER = 'ldap://fileserver.net'
BASE_DN = 'dc=fileserver,dc=net'  # base dn to search in

#login for username and password, to be passed into the ldapConnection function
LDAP_LOGIN = input('Enter your ldap login: ')
LDAP_PASSWORD = input('Enter your ldap password: ')

def ldapConnection(LDAP_LOGIN, LDAP_PASSWORD):
    try:
        connect = ldap.initialize(LDAP_SERVER)  #connects to server
        print("Connection initialized")
    except ldap.SERVER_DOWN:
        print("Can't connect to LDAP server")
        exit(4)
    try:
        connect.simple_bind_s(LDAP_LOGIN, LDAP_PASSWORD)    #login for user
    except (ldap.INVALID_CREDENTAILS):
        print("Invalid login and/or password")
        exit(3)
    ATTRIBUTES_TO_SEARCH = ['memberOf']
    OBJECT_TO_SEARCH = 'userPrincipalName=user@example.com'
    connect.set_option(ldap.OPT_REFERRALS, 0)  # to search the object and all its descendants
    result = connect.search_s(BASE_DN, ldap.SCOPE_SUBTREE, OBJECT_TO_SEARCH, ATTRIBUTES_TO_SEARCH)  #searches through ldap
    return result   #This needs to return a group id so we can use it for authorization in the code
=======
LDAP_SERVER = 'ldap://fileserver.net'
BASE_DN = 'dc=fileserver,dc=net'  # base dn to search in
LDAP_LOGIN = 'ldap_login'
LDAP_PASSWORD = 'ldap_password'
OBJECT_TO_SEARCH = 'userPrincipalName=user@example.com'
ATTRIBUTES_TO_SEARCH = ['memberOf']

connect = ldap3.initialize(LDAP_SERVER)
connect.set_option(ldap3.OPT_REFERRALS, 0)  # to search the object and all its descendants
connect.simple_bind_s(LDAP_LOGIN, LDAP_PASSWORD)
result = connect.search_s(BASE_DN, ldap3.SCOPE_SUBTREE, OBJECT_TO_SEARCH, ATTRIBUTES_TO_SEARCH)
>>>>>>> 5234ba0 (mild main changes to function)
