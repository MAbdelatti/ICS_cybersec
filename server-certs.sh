dir="server-certs"
echo "Creating CA key. The passkey is important so remember it"
openssl genrsa -des3 -out mqtt-ca.key 2048
echo "##########################################"
echo "Creating CA Certificate 10 years expiry"
openssl req -new -x509 -days 3650 -key mqtt-ca.key -out mqtt-ca.crt
echo "##########################################"
echo "Creating Server key"
openssl genrsa -out mqtt-server.key 2048
echo "##########################################"
echo "Creating Server certificate"
openssl req -new -out mqtt-server.csr -key mqtt-server.key
echo "##########################################"
echo "Signing Server certificate Server certificate"
echo "Common Name should be the FQDN or IP address of the server"
echo "It is what you would use to ping the server"
openssl x509 -req -in mqtt-server.csr -CA mqtt-ca.crt -CAkey mqtt-ca.key -CAcreateserial -out mqtt-server.crt -days 3650
echo "##########################################"
echo "##########################################"
echo "copying files to a subdirectory"
if [ -d $dir ]
then
 echo "directory Exists"
else
 mkdir $dir
fi
mv *.crt $dir
mv *.key $dir
mv *.csr $dir
mv *.srl $dir
echo "Modify the port number to 8883 in /etc/mosquitto/mosquitto.conf file Default Listener section."
sudo cp $dir/mqtt-server.key $dir/mqtt-server.crt /etc/mosquitto/certs/
sudo cp $dir/mqtt-ca.crt /etc/mosquitto/ca_certificates/
echo "Add the full path and file name in /etc/mosquitto/mosquitto.conf file in the following sections: cafile path/mqtt-ca.crt, certfile path/mqtt-server.crt, keyfile path/mqtt-server.key, tls_version tlsv1.3"
