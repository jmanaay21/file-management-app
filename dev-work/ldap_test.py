# import ldap
# import sys
# import LDAP_ADMIN_DN

# #Ldap_conn = ldap.initialize(ldap_host)

# def try_ldap_bind(ldap_host, admin_pass):
#     try:
#         ldap_conn = ldap3.initialize(ldap_host)
#         print("Connection initialized")
#     except ldap.SERVER_DOWN:
#         print("Cant contact LDAP server")
#         exit(4)
#     try:
#         ldap_conn.simple_bind_s(LDAP_ADMIN_DN,admin_pass)
#     except (ldap.INVALID_CREDENTAILS):
#         print("This passwords is incorrect.")
#         sys.exit(3)
#     print("Authentication successful")

