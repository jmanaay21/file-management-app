import ldap
import sys


l = ldap.initialize('ldap://localhost')
binddn = "cn=Andy,ou=People,dc=fileserver,dc=net"
pw = "password"
basedn = "ou=People,dc=filserver,dc=net"
searchFilter = "(&(gidNumber=5000)(objectClass=posixAccount))"
searchAttribute = ["",""]
#this will scope the entire subtree under UserUnits
searchScope = ldap.SCOPE_SUBTREE
#Bind to the server
try:
    l.protocol_version = ldap.VERSION3
    l.simple_bind_s(binddn, pw) 
except ldap.INVALID_CREDENTIALS:
    print("Your username or password is incorrect.")
    sys.exit(0)
except ldap.LDAPError as e:
    if type(e.message) == dict and e.message.has_key('desc'):
        print(e.message['desc'])
    else: 
        print(e)
    sys.exit(0)
try:    
    ldap_result_id = l.search(basedn, searchScope, searchFilter, searchAttribute)
    result_set = []
    while 1:
        result_type, result_data = l.result(ldap_result_id, 0)
        if (result_data == []):
            break
        else:
            ## if you are expecting multiple results you can append them
            ## otherwise you can just wait until the initial result and break out
            if result_type == ldap.RES_SEARCH_ENTRY:
                result_set.append(result_data)
    print(result_set)
except ldap.LDAPError as e:
    print(e)
l.unbind_s()
