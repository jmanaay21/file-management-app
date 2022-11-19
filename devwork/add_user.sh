#!/bin/bash

ldapadd -x -D cn=admin,dc=fileserver,dc=net -W -f user_add.ldif