"""
Will implement this version of ldap, will cut down on unecessary
code and contain the users attributes (uidNumber, gidNumber)
"""
import ldap
from getpass import getpass


ldapconn = ldap.initialize('ldap://localhost')

ID = ""

cn = input("Enter Username:  ")
user = f'uid={cn},ou=People,dc=fileserver,dc=net'
userpass = getpass("Enter Password:  ")

# Making vars for search_s function
baseDN = "dc=fileserver,dc=net"
search_scope = ldap.SCOPE_SUBTREE

ldapconn.simple_bind_s(user, userpass)
usercn = f"uid={cn}"
searchFilter = "uid=10000"
retrieve_attributes = 0

UID = ldapconn.search_s(baseDN, search_scope, usercn, ['gidNumber'])
UID = str(UID)

print(UID)

for n in UID:
    if n.isdecimal():
        ID = ID + n
print(ID)

"""
search up search_s function on python-ldap
"""