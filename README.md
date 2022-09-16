# file-management-app

### Secure File Management Application Information and Parameters

This project requires the design and development of a file management 
application that allows the secure sharing and management of files. 
The application operates in a client-server architecture where common tasks
include uploading, downloading, and deleting clients’ files from and to the
server. Clients first need to be created and managed through an LDAP
(Lightweight Directory Access Protocol) server. Clients need to be authenticated
to access the server. Access control (authorization) mechanisms should be
enforced to affect what clients can do on the server. All network communication
(and its protocols) between all hosts (clients, servers) should be encrypted.
An auxiliary auditing functionality should keep track of what clients do on the
server.

### Requirements
App (file management):
- functionality (up, down, delete, view)
- authentication (LDAP)	
- authorization (access control)
- logging/auditability

Must run and be developed in LinuxOS

### Approach
- MySQL approach for data storage/file manipulation
- Use LDAP as an Authentication and Authorization system


### Resources

- [Manage and use LDAP](https://www.digitalocean.com/community/tutorials/how-to-manage-and-use-ldap-servers-with-openldap-utilities)

- [MySQL Community version](https://www.mysql.com/products/community/#:~:text=MySQL%20Community%20Edition%20is%20the,community%20of%20open%20source%20developers.)

- [MySQL Manual + Guide](https://dev.mysql.com/doc/refman/8.0/en/)

- [Connecting MySQL to Visual Studio](https://dev.mysql.com/doc/visual-studio/en/)

- [MySQL to Python](https://dev.mysql.com/doc/connector-python/en/)