# dc=fileserver, dc=net
# ip = localhost (127.0.0.1)
import ldap

def _connect_to_ldap(self):
    ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_NEVER)
    connection = ldap.initialize(self.server_uri)

    if self.start_tls:
        try:
            connection.start_tls_s()
        except ldap.LDAPError:
            e = get_exception()
            self.module.fail_json(msg="Cannot start TLS.", details=str(e))

        try:
            if self.bind_dn is not None:
                connection.simple_bind_s(self.bind_dn, self.bind_pw)
            else:
                connection.sasl_interactive_bind_s('', ldap.sasl.external())
        except ldap.LDAPError:
            e = get_exception()
            self.module.fail_json(
                msg="Cannot bind to the server.", details=str(e))

        return connection

