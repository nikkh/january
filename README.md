# WIP Templates - Test Harness

This page enables you to discretly deploy ARM templates for the infrastruture - useful to deploy templates with a single click while developing them.

Deploy VNet needs to be run first - this will create your NSGs, VNet and Subnets and NSGs will be assigned to the Kafka and Spark Subnets.  Others may be run in any order.

[Deploy Vnet](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fnikkh%2Fjanuary%2Fmaster%2Fcreate_vnet.json)

[Deploy Firewall](.)

[Deploy Bastion](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fnikkh%2Fjanuary%2Fmaster%2Fcreate_bastion.json)

[Deploy Kafka](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fnikkh%2Fjanuary%2Fmaster%2Fcreate_kafka_cluster.json)

[Deploy Spark](.)

and run last....

[Configure Firewall](.)

