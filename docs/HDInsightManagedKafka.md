## Deploy a HDInsight Managed Kafka with Confluent Schema Registry 

In this section we would deploy an HDInsight Managed Kafka  cluster with an Edge Node inside a Virtual Network and then install the Confluent Schema Registry on the Edge Node.  

- Click on the Deploy to Azure Button to start the deployment process

<a href="https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fnikkh%2Fjanuary%2Fmaster%2Fazuredeploy.json" target="_blank">
    <img src="http://azuredeploy.net/deploybutton.png"/>
</a><a href="http://armviz.io/#/?load=https://raw.githubusercontent.com/nikkh/january/master/azuredeploy.json" target="_blank">
  <img src="http://armviz.io/visualizebutton.png"/>
</a>

</br>
</br>

 - On the Custom deployment template populate the fields as described below. Leave the rest of their fields at their default entries
    -  **Resource Group** : Choose a previously created resource group from the dropdown
    - **Location** : Automatically populated based on the Resource Group location 
    - **Cluster Name** : Enter a cluster name( or one is created by default)
    - **Cluster Login Name**: Create a administrator name for the Kafka Cluster( example : admin) 
    - **Cluster Login Password**: Create a administrator login password for the username chosen above
    - **SSH User Name**: Create an SSH username for the cluster
    - **SSH Password**: Create an SSH password for the username chosen above

- Check he box titled "*I agree to the terms and conditions stated above*" and click on **Purchase**. 
    
![HDInsight Kafka Schema Registry](https://github.com/nikkh/january/blob/master/images/Pic2.png)

- Wait till the deployment completes and you get the *Your Deployment is Complete* message and then click on  **Go to resource**.

![HDInsight Kafka Schema Registry](https://github.com/nikkh/january/blob/master/images/Pic3.png)

- On the Resource group explore the various components created as part of the Deployment . Click on the HDInsight Cluster to open the cluster page. 

![HDInsight Kafka Schema Registry](https://github.com/nikkh/january/blob/master/images/Pic4.png)

- On the HDInsight cluster page click on the SSH+Cluster login blade on the left and get the hostname of the edge node that was deployed.

![HDInsight Kafka Schema Registry](https://github.com/nikkh/january/blob/master/images/Pic5.png)

- Using an SSH client of your choice ssh into the edge node using the **sshuser** and **password** that you set in the custom ARM script. 

- In the next section we would configure the Confluent Kafka Schema Registry that we installed on the edge node.  

Click [**[Next](https://github.com/nikkh/january/blob/master/ConfigureSchemaRegistry.md)**]
<!--stackedit_data:
eyJoaXN0b3J5IjpbLTQyMjc3MTUzLC0xOTgxMzU5MTksMTM0Mz
EyMjI0NCw5NzIzNDg5MTQsMTc4NDI0ODMyNiwtMTA4MTk0OTQz
NywtMzc2NjQxMDE5LC0xOTQ2NTk4MDAyLDEyMzk2MjUwMzUsMT
Y3NDQxNTQ2M119
-->
