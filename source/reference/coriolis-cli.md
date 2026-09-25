---
title: "Coriolis CLI and REST API"
wp_id: 39361
---

# Coriolis CLI and REST API

This section will provide an overview of how to use the CLI and API to interact with Coriolis.

For an overview of the functioning and mechanics of Coriolis, please review the Product Overview page **[here](https://cloudbase.it/coriolis-getting-started)**.

Due to Coriolis' pluggable nature, this guide presents general interactions with Coriolis and applies to working with any source/destination cloud Coriolis supports. Please review the documentation of each respective cloud's Coriolis plugin to get exact details on the required fields of parameters, such as the **- -connection** or  **- -destination-environment** 

The following outlines running the Coriolis CLI client from the Coriolis appliance. Coriolis CLI client can be installed and executed from other systems that have access to Coriolis.

## Installing the Coriolis command-line client

The following commands will install the Coriolis command-line client on the local machine.

### Coriolis CLI installation commands

```bash
$ git clone https://github.com/cloudbase/python-coriolisclient
```

![](_static/images/cli1.png)

```bash
$ pip3 install python-coriolisclient
$ # verify client is available in path:
$ /usr/bin/env coriolis
```

![](_static/images/cli2.png)

### Expose the Coriolis appliance

By default, all the Coriolis appliance services listen only on localhost. In order to expose all the services from the appliance, you will use the respective option from the Coriolis console menu.

This is a one-time step that must be performed for an appliance.

**Apply the RC file so you can run the Coriolis commands from where the Coriolis client has been installed**

By default, the Coriolis RC file for the admin account is to be found under /etc/kolla/ on the Coriolis Appliance

```text
#select option '3) Edit/Inspect Coriolis Configuration'
```

![](_static/images/coriolis-options.png)

```text
$cat /etc/kolla/admin-openrc.sh
```

![](_static/images/coriolis-rc-file1.png)

It will also need to be copied to the machine where the Coriolis client has been installed.

```text
$scp /etc/kolla/admin-openc.sh adrian@<IP address>:/mnt/c/coriolis/
```

After copying it, the file needs to be sourced on the machine where the client runs, and Coriolis commands can be performed afterwards.

Please modify the OS_AUTH_URL with the corresponding IP of the Coriolis appliance. A ping test can confirm the connectivity from the client machine where you have installed the CLI to the Coriolis remote-facing IP address.

```text
$source admin-openrc.sh

$coriolis endpoint list
```

![](_static/images/coriolis-apply-rc.png)

## Defining a Coriolis endpoint for a given cloud

In order to perform the steps needed to migrate/replicate to/from a given platform, Coriolis will need credentials for accessing the said platform.

Coriolis endpoints are a type of resource definable in Coriolis that simply declares the type and connection parameters for a given cloud platform. The connection parameters must be in JSON format, the exact structure of which depends on the type of cloud Coriolis is interacting with. Please review the documentation of the plugin for the respective cloud you are dealing with to see the format needed for the connection info JSON.

Below is an example of creating an endpoint for a fictitious "CloudX"

### Endpoint creation example

```text
#the example of the RC file is reffering to the one on the Coriolis Appliance
$source /etc/kolla/admin-openrc.sh
$coriolis endpoint create \
      --name cloudx --description "CloudX endpoint" \
      --provider cloudx --connection '{"username": "iamtheowner", "password": "SeKr37"}'
```

The cloud plugin identifier given through the **- provider** parameter is unique to each plugin. Please review the documentation of the respective platform's Coriolis plugin to find the correct plugin identifier for it.

Later on, when we want to start migration jobs to/from CloudX, we will be able to simply reference the endpoint created above by its ID instead of having to fill in the credentials of the clouds involved at each and every new task.

### Storing Coriolis endpoint connection info in Barbican

Coriolis features integration with Barbican, the OpenStack project dedicated to the storage and management of sensitive information.

Instead of providing the plaintext JSON **- connection** directly to Coriolis, one might first store it in Barbican and only provide Coriolis with a reference to it.

#### Endpoint creation example with Barbican secret

```text
#the example of the RC file is reffering to the one on the Coriolis Appliance
$source /etc/kolla/admin-openrc.sh
$openstack secret store --name "CloudX credentials" -t "text/plain" \
 -p '{"username": "iamtheowner", "password": "SeKr37"}'
$coriolis endpoint create \
 --name cloudx --description "CloudX endpoint" \
 --provider cloudx --connection-secret "$URL_OF_ABOVE_BARBICAN_SECRET"
```

Barbican will encrypt the connection info before storing it in the database, and Coriolis will only access the credentials and pass them to the respective Coriolis platform plugin when it uses its services.

### Validating a Coriolis endpoint 

Once a cloud endpoint has been created for the specific platform we are dealing with, Coriolis may be instructed to validate that the provided credentials are correct by performing a test with the credentials.

From the command line client, this may be done by running the following:

#### Endpoint validation example

```text
#the example of the RC file is reffering to the one on the Coriolis Appliance
$source /etc/kolla/admin-openrc.sh
$coriolis endpoint validate connection $ENDPOINT_ID
```

Should the credentials be in order, the command will terminate with no output and error code 0. Otherwise, a descriptive error message received back from the Coriolis service will be displayed.

### Listing instances available for migration/replication from a source platform

If Coriolis supports migrating/replicating _from_ a particular platform, then the Coriolis plugin for that platform implements functionality for listing the instances available for the operation.

From the command line client, the following may be run to list instances available for export:

#### Endpoint instance list example

```text
#the example of the RC file is reffering to the one on the Coriolis Appliance
$source /etc/kolla/admin-openrc.sh
$coriolis endpoint instance list --source-environment '{"source": "parameters"}' $ENDPOINT_ID
```

The parameters for the **- source-environment** are source cloud-specific and will aid Coriolis in listing instances (e.g: 'resource_group' for Azure/AzureStack). Please review the documentation of the Coriolis platform plugin of the source cloud for the exact parameters that are expected.

For starting migrations/replicas for a given instance, whether or not it may be identified via its name and/or its ID depends on the implementation of the Coriolis platform plugin for that particular cloud. Please review the documentation of the respective platform's Coriolis plugin for exact instance referencing requirements.

### Additional operations for Coriolis endpoints

In addition to the above notable commands, the Coriolis command line client also offers the following operations on cloud endpoints:

```text
#the example of the RC file is reffering to the one on the Coriolis Appliance
$source /etc/kolla/admin-openrc.sh
 #list all defined endpoints:
$coriolis endpoint list
 #detailed view of a specific endpoint:
$coriolis endpoint show $ENDPOINT_ID
 #update the parameters of a specific endpoint:
$coriolis endpoint update --param "updated value for --param" $ENDPOINT_ID
 #delete a specific endpoint:
$coriolis endpoint delete $ENDPOINT_ID
```

## Creating migration jobs

### Prerequisites

  * an existing Coriolis endpoint for the migration source cloud (granted the source cloud has a Coriolis platform plugin available)
  * an existing Coriolis endpoint for the migration destination cloud (granted the source cloud has a Coriolis platform plugin available)
  * the parameters for the **- source-environment**, which are source cloud-specific. Please review the documentation of the Coriolis platform plugin of the source cloud for the exact parameters which are expected 
  * the parameters for the **- destination-environment**, which are destination cloud-specific. Please review the documentation of the Coriolis platform plugin of the destination cloud for the exact parameters which are expected 
  * a unique identifier of the instance we would like to migrate

Granted all the above, a migration job may be created for an instance by running the following:

### Creating a Coriolis migration

```text
#the example of the RC file is reffering to the one on the Coriolis Appliance
$source /etc/kolla/admin-openrc.sh
$coriolis migration create \
 --origin-endpoint $ID_OF_SOURCE_CLOUD_ENDPOINT \
 --destination-endpoint $ID_OF_DESTINATION_CLOUD_ENDPOINT \
 --source-environment '{"the": "source cloud specific params"}' \
 --destination-environment '{"the": "destination cloud specific params"}' \
 --network-map '{"source network name": "name or ID of network on destination"}' \
 --instance $IDENTIFIER_OF_INSTANCE_ON_SOURCE
```

The above command will create a migration job within Coriolis, which may later be queried or halted by referencing its ID.

### Additional operations for Coriolis migrations

In addition to the above create command, the Coriolis command line client also offers the following operations on migration jobs:

```text
#the example of the RC file is reffering to the one on the Coriolis Appliance
$source /etc/kolla/admin-openrc.sh
 #list all registered migration jobs:
$coriolis migration list
 #view a particular migration's status:
$coriolis migration show $MIGRATION_ID
 #cancel a running migration:
$coriolis migration cancel $MIGRATION_ID
 #delete records of a previous migration:
 #this does not delete the migrated instance on the destination cloud
 #should that migration have been ended successfully.
 #the migration must not be running.
$coriolis migration delete $MIGRATION_ID
```

## Creating replication (DRaaS) jobs

### Prerequisites

  * an existing Coriolis endpoint for the replication source cloud (granted the source cloud has a Coriolis platform plugin available)
  * an existing Coriolis endpoint for the replication destination cloud (granted the source cloud has a Coriolis platform plugin available)
  * the parameters for the **- source-environment**, which are source cloud-specific. Please review the documentation of the Coriolis platform plugin of the source cloud for the exact parameters which are expected 
  * the parameters for the **- destination-environment**, which are destination cloud-specific. Please review the documentation of the Coriolis platform plugin of the destination cloud for the exact parameters which are expected 
  * a unique identifier of the instance we would like to replicate

Granted all the above, a replication job may be **defined** (but not yet executed) for an instance by running the following:

### Creating a Coriolis replica

```text
#the example of the RC file is reffering to the one on the Coriolis Appliance
$source /etc/kolla/admin-openrc.sh
$coriolis replica create \
 --origin-endpoint $ID_OF_SOURCE_CLOUD_ENDPOINT \
 --destination-endpoint $ID_OF_DESTINATION_CLOUD_ENDPOINT \
 --source-environment '{"the": "source cloud specific params"}' \
 --destination-environment '{"the": "destination cloud specific params"}' \
 --network-map '{"source network name": "name or ID of network on destination"}' \
 --instance $IDENTIFIER_OF_INSTANCE_ON_SOURCE
```

The above command will define a replication job with Coriolis, which may later have executions (syncs) scheduled, canceled, and deployed by referencing the replication job's ID.

### Starting an execution for a replication job

**Prerequisites** : an already defined replication job that does not already have a running execution

An existing replica may have a new execution (sync run) started by running the following:

#### Executing a Coriolis replica

```text
#the example of the RC file is reffering to the one on the Coriolis Appliance
$source /etc/kolla/admin-openrc.sh
$coriolis replica execute $REPLICA_ID
```

The above command will launch a new replica execution, which may later be queried for status, canceled, or deleted by referencing both the ID of the Replica, and the ID of the newly-created replica execution.

### Additional operations for Coriolis replica executions

In addition to the above execution command, the Coriolis command line client also offers the following operations on replica executions:

```text
#the example of the RC file is reffering to the one on the Coriolis Appliance
$source /etc/kolla/admin-openrc.sh
 #list all executions of a replica:
$coriolis replica execution list $REPLICA_ID
 #view a particular replica execution's status:
$coriolis replica execution show $REPLICA_ID $REPLICA_EXECUTION_ID
 #cancel a running replica execution:
$coriolis replica execution cancel $REPLICA_ID $REPLICA_EXECUTION_ID
 #delete records of a non-running replica execution:
 #this will not delete any resources which might have been
 #replicated on the destination cloud if the replica execution
 #had completed successfully (such as the replica disks)
$coriolis replica execution delete $REPLICA_ID $REPLICA_EXECUTION_ID
 #delete the replica disks:
 #this will delete the disks on the destination cloud we are
 #replicating to, but it will not delete replica in Coriolis.
 #Later executions may be launched for the replica, but the next one
 #will be a full execution to completely new disks on the destination.
$coriolis replica disks delete $REPLICA_ID
```

### Deploying a replica on the destination cloud

**Prerequisite** : a pre-existing Coriolis replica that has at least one successful replica execution

An existing replica may be deployed on the destination cloud by running the following:

#### Deploying a Coriolis replica

```text
#the example of the RC file is reffering to the one on the Coriolis Appliance
$source /etc/kolla/admin-openrc.sh
$coriolis migration deploy replica $REPLICA_ID
```

The above command will start a replica migration job that will recreate the instance on the destination cloud with the state of the last replica execution.

Using the replica migration job's ID to reference it, you may run the same "Coriolis migration …" operations detailed in the section on creating migration jobs.

### Coriolis Replica/Migration task tutorial

For more information on how to create a Replica/Migration using Coriolis' CLI, please check the **[Coriolis Replica/Migration task](https://cloudbase.it/coriolis-cli-example)** page.

## Coriolis Minion Pools

Coriolis Minion Pools are a resource that relies on **temporary virtual machines,** which it deploys on the source/target platforms to perform various actions during transfer operations during **Coriolis Replica/Migration jobs**.

For more information regarding Coriolis Minion Pools using CLI, please check **[Minion Pools- Creation and Management](https://cloudbase.it/minion-pools---creation-and-management)** page.

## Coriolis REST API

As a generic workflow, before sending out API requests to Coriolis, you will need to do 2 things:

  1. Make sure the Coriolis API service is reachable from where you make the requests.
  2. Get authorization from Keystone for the API user.

Coriolis services running on the appliance are bound to localhost by default. To expose them to the appliance VM's IP address, head to its console and execute the option **6) Expose Coriolis Services Endpoints**.

This will redeploy the services run inside Coriolis to the IP address; therefore, API calls should be made to that IP address from this point on. 

After the service exposure is done, you will need to prepare the authentication body. This will look similar to standard Keystone authentication. In this example, we will use scoped authentication to scope authorization inside a project. The request body should look something like this: 

Where OS_USERNAME is the login user for Coriolis (usually 'admin'), OS_PASSWORD is the login password, and OS_TENANT_NAME is the project name (also usually 'admin'). Save this as `curl-auth.json` in order to pass it to curl as shown below:

```json
{
  "auth": {
    "identity": {
      "methods": ["password"],
      "password": {
        "user": {
          "name": "__OS_USERNAME__",
          "domain": { "name": "Default" },
          "password": "__OS_PASSWORD__"
        }
      }
    },
    "scope": {
      "project": {
        "domain": { "name": "Default" },
        "name": "__OS_TENANT_NAME__"
      }
    }
  }
}
```

```bash
export OS_TOKEN=$(curl -ik -H "Content-Type: application/json" -d @./curl-auth.json https://${APPLIANCE_IP}:5000/v3/auth/tokens 2> /dev/null | grep X-Subject-Token | cut -d' ' -f2 | tr -d '\t\r\n ')
```

This will save the token in `$OS_TOKEN`, so you can pass it to all of your API calls.

Once we have the token, we can go ahead and execute some calls, like listing endpoints:

```bash
curl -s -X GET -H "Accept: application/json" -H "X-Auth-Token: $OS_TOKEN" -k https://${APPLIANCE_IP}:7667/v1/${PROJECT_ID}/endpoints
```

You can get your PROJECT_ID from the UI URL or from the console by executing **#openstack project list** , after entering option 3. 

The above API call has been made in insecure mode, as Coriolis hosts its own PKI.

In order to make verified calls, you will need to download Coriolis' CA certificate (you can download it from the appliance at **http://${APPLIANCE_ID}:9001/coriolis-ca.crt**). 

Then, you can run the same API call by running as follows:

```bash
curl -s -X GET -H "Accept: application/json" -H "X-Auth-Token: $OS_TOKEN" --cacert coriolis-ca.crt https://${APPLIANCE_IP}:7667/v1/${PROJECT_ID}/endpoints
```

For the API reference, please refer to this page: [GitHub - cloudbase/coriolis: Cloud Migration as a Service](https://github.com/cloudbase/coriolis?tab=readme-ov-file#api-documentation)
