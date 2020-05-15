#!/bin/bash
set -o errexit
set -o xtrace

# Install jq
dpkg -s jq || sudo apt-get install -y jq

# Install Confluent platform (includes Kafka schema registry)
wget -qO - http://packages.confluent.io/deb/4.1/archive.key | sudo apt-key add -
sudo add-apt-repository "deb http://packages.confluent.io/deb/4.1 stable main"
sudo apt-get update
dpkg -s confluent-platform-oss-2.11 || sudo apt-get install -y confluent-platform-oss-2.11

echo "[Unit]
Description = Confluent Rest Proxy
After = network.target
StartLimitIntervalSec=0
[Service]
Type=simple
Restart=always
RestartSec=1
User=ohklvmadmin
ExecStart=/usr/bin/kafka-rest-start /etc/kafka-rest/kafka-rest.properties
[Install]
WantedBy=multi-user.target
" > /etc/systemd/system/kafka-rest.service
 
echo "
bootstrap.servers=<myproject>.cloud:9092
# Confluent Cloud Schema Registry
schema.registry.url=http://10.0.3.8:8081
basic.auth.credentials.source=USER_INFO
schema.registry.basic.auth.user.info=<schema-registry-api-key>:<schema-registry-api-secret>
" > /etc/kafka-rest/kafka-rest.properties

systemctl start kafka-rest
systemctl enable kafka-rest

echo "Installation successful."
