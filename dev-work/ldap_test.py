import sys

import ldap

ldap_host = "ldap://fileserver.net"
LDAP_ADMIN_DN = input("Enter your username: ")
admin_pass = input("Enter your password: ")

def try_ldap_bind(ldap_host, admin_pass):
    try:
        ldap_conn = ldap.initialize(ldap_host)
        print("Connection initialized")
    except ldap.SERVER_DOWN:
        print("Cant contact LDAP server")
        exit(4)
    try:
        ldap_conn.simple_bind_s(LDAP_ADMIN_DN,admin_pass)
    except (ldap.INVALID_CREDENTAILS):
        print("This passwords is incorrect.")
        sys.exit(3)
    print("Authentication successful")

#def getID(user):
#    result = connect.search_s('dc=fileserver,dc=net',ldap.SCOPE_SUBTREE,'userPrincipalName='user'@fileserver.net',['memberOf'])
#    return result

