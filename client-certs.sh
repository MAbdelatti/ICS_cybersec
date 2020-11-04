#!/bin/bash
set -x
#doesn't currently work using varaibles
cacert = 'server-certs/mqtt-ca.crt'
cakey = 'server-certs/mqtt-ca.key'

dir="client-certs"
echo "Creating Client Key"
openssl genrsa -out mqtt-client.key 2048
echo "##########################################"
echo "Creating certificate request"
openssl req -new -out mqtt-client.csr -key mqtt-client.key
echo "##########################################"
echo "Signing client certificate with CA key"
echo "The CA key File must be in the server-certs folder"
openssl x509 -req -in mqtt-client.csr -CA server-certs/mqtt-ca.crt -CAkey server-certs/mqtt-ca.key -CAcreateserial -out mqtt-client.crt -days 3650

if [ -d $dir ];then
 echo "directory Exists"
else
 mkdir $dir
fi

mv mqtt-client.* $dir
