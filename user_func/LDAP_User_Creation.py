#User creation code, may have to be in bash to run on command line

#User input for file
print("Welcome to user creation")

user = input("Enter the user ID (name): ")
sn = input("Enter the last name: ")
groupID = input("Enter the group ID number: ")
password = input("Enter a password: ")

uid = user

fileCreate = f"dn: uid={user},ou=People,dc=fileserver,dc=net\n" \
    "objectClass: inetOrgPerson\n" \
    "objectClass: posixAccount\n" \
    "objectClass: shadowAccount\n" \
    f"uid: {uid}\n" \
    f"sn: {sn}\n" \
    f"cn: {user} {sn}\n" \
    f"displayName: {user} {sn}\n" \
    f"gidNumber: {groupID}\n" \
    f"userPassword: {password}\n" \
    f"gecos: {user} {sn}\n" \
    "loginShell: /bin/bash\n" \
    f"homeDirectory: /home/{user}"

def filemaker(fileCreate):
    new_file = open("user_add.ldif", "w")
    new_file.write(fileCreate)
    new_file.close()

filemaker(fileCreate)

