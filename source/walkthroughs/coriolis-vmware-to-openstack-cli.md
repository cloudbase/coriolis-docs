---
title: "How to migrate VMs from VMware to OpenStack using the CLI"
wp_id: 37728
---

# How to migrate VMs from VMware to OpenStack using the CLI

Coriolis provides a portable command line interface (CLI) available on Linux, Macos or Windows. It is already available in the VM appliance and it can be easily installed anywhere with “**pip install python-coriolisclient** ”.

### Basic usage

Coriolis uses Keystone for identity management and the CLI usage resembles the OpenStack client for setting the required variables. The easiest way to start is just to SSH into the VM appliance. The connection parameters are available in "**/etc/kolla/admin-openrc.sh** ”:

```text
OS_AUTH_URL=http://127.0.0.1:35357/v3
OS_IDENTITY_API_VERSION=3
OS_INTERFACE=internal
OS_PASSWORD=<your password here>
OS_PROJECT_DOMAIN_NAME=default
OS_PROJECT_NAME=admin
OS_TENANT_NAME=admin
OS_USERNAME=admin
OS_USER_DOMAIN_NAME=default
```
  
 

### Creating an endpoint for OpenStack

To begin with, we need to store in Barbican the OpenStack credentials and connection information:

```text
openstack secret store -p '{"username": "demo", "password": "YourPassword", "auth_url": "http://controller:35357/v3", "project_name": "demo", "project_domain_name": "default", "user_domain_name": "default", "identity_api_version": 3,"allow_untrusted": true}'
```
  
Replace the values to match your OpenStack endpoint,  _allow_untrusted_ is needed if your endpoint uses a self signed certificate for HTTPS.

The above call will return an output similar to:

```text
+---------------+-----------------------------------------------------------------------+
| Field         | Value                                                                 | 
+---------------+-----------------------------------------------------------------------+
| Secret href   | http://127.0.0.1:9311/v1/secrets/eb3e0343-671e-4b8e-bfe2-1d7ef9848575 |
| Name          | None                                                                  |
| Created       | 2017-08-19T17:44:06+00:00                                             |
| Status        | ACTIVE                                                                |
| Content types | {u'default': u'text/plain'}                                           |
| Algorithm     | aes                                                                   |
| Bit length    | 256                                                                   |
| Secret type   | opaque                                                                |
| Mode          | cbc                                                                   |
| Expiration    | None                                                                  |
+---------------+-----------------------------------------------------------------------+
```
  
Copy the “Secret href” in order to create the Coriolis endpoint along with a name, a description and the provider type (openstack in this case):

```text
coriolis endpoint create --provider openstack --name OpenStack --description "My OpenStack" --connection-secret http://127.0.0.1:9311/v1/secrets/eb3e0343-671e-4b8e-bfe2-1d7ef9848575
```
  
You can now list the endpoints with:

coriolis endpoint list

```text
coriolis endpoint list
```
  
The output will look like this:

```text
+--------------------------------------+-----------+-----------+--------------+
| ID                                   | Name      | Type      | Description  |
+--------------------------------------+-----------+-----------+--------------+
| 1769beb7-0fdf-4211-b47e-8d9056e757a5 | OpenStack | openstack | My OpenStack |
+--------------------------------------+-----------+-----------+--------------+
```
  
It is recommended to validate the connection to make sure coriolis can properly connect to your OpenStack API, using the ID of the connection:

```text
coriolis endpoint validate connection 1769beb7-0fdf-4211-b47e-8d9056e757a5
```
  
In case of success, the command will exit with 0. In case of connection problems, you will get an error message for troubleshooting the issue.

Connections can be managed with **coriolis endpoint show <id>**, **coriolis endpoint update <id>** and **coriolis endpoint delete <id>**

 

### Creating an endpoint for VMware vSphere

Similarly to the OpenStack case, an endpoint can be created for your VMware vSphere endpoint:

```text
openstack secret store -p '{"username": "your_user@vsphere.local", "password": "your_password", "host": "your_vsphere_host", "port": 443, "allow_untrusted": true}’
```
  
```text
coriolis endpoint create --provider vmware_vsphere --name VMware --description "My VMware vSphere" --connection-secret <secret_href>
```
  
```text
coriolis endpoint validate connection <id>
```
  
 

### Configuring a replica for a VM from vSphere to OpenStack

At this point you should have two valid endpoints configured in Coriolis:

coriolis endpoint list

```text
coriolis endpoint list
```
  
```text
+--------------------------------------+-----------+----------------+-------------------+
| ID                                   | Name      | Type           | Description       |
+--------------------------------------+-----------+----------------+-------------------+
| 1769beb7-0fdf-4211-b47e-8d9056e757a5 | OpenStack | openstack      | My OpenStack      |
| 9f4ee75c-215d-48e8-9a0f-e337fbdf4581 | VMware    | vmware_vsphere | My VMware vSphere |
+--------------------------------------+-----------+----------------+-------------------+
```
  
If you don’t know the name of the VMs to replicate, you can just list them with **coriolis endpoint instance list**.

For example the following command will list the first 10 VMs with a name containing “oracle”:

```text
coriolis endpoint instance list 9f4ee75c-215d-48e8-9a0f-e337fbdf4581 --limit 10 --name 'oracle'
```
  
```text
+---------+-----------------------+--------+-----------+-------+---------+
| ID      | Name                  | Flavor | Memory MB | Cores | OS Type |
+---------+-----------------------+--------+-----------+-------+---------+
| vm-157  | Oracle Linux 7        |        | 2048      | 4     | linux   |
+---------+-----------------------+--------+-----------+-------+---------+
```
  
We need to let Coriolis know about how to map the networks between origin (VMware) and destination (OpenStack) and what flavor to use:

```text
REPLICA_ENV='{"network_map": {"VM Network": "private"}, "flavor_name": "m1.small"}'
```
  
In this example, the VMware network is called “VM Network” and the corresponding network on OpenStack is called “private”.

We can now create the replica:

```text
coriolis replica create --origin-endpoint 9f4ee75c-215d-48e8-9a0f-e337fbdf4581 --destination-endpoint 1769beb7-0fdf-4211-b47e-8d9056e757a5 --instance "Your VM Name” --destination-environment "$REPLICA_ENV"
```
  
Note: to replicate a group of VMs, just add more “**- instance <VM name>**” clauses.

You can list the replicas with:

coriolis replica list

```text
coriolis replica list
```
  
 

### Performing the replica

Now it’s time to get Coriolis copy all the VM data from VMware to OpenStack, with a Cinder volume created for each disk. The first time it will perform a full copy of the content of the VM, while from the second time onwards it will only copy incrementally the data that changed:

```text
coriolis replica execute <replica_id>
```
  
Add **- shutdown-instances** in case you would like Coriolis to shutdown the VMs before the replica starts.

This will return an ID that identifies this particular execution along with info about all the tasks that will need to be completed as part of the process.

You can now check the status of the execution:

```text
coriolis replica execution show <replica_id> <execution_id>
```
  
Depending on the size of the VM, this might take a while, so this is a perfect time to grab a coffee and periodically check on the status.

In case of errors, Coriolis will also give you all the information available, for example letting you know if Change Block Tracking (CBT) is not enabled on the VMware VM.

Once completed, you will have a 1-1 copy of all the content of the VM on your OpenStack environment. If you execute the replica again you will notice that this time it is way faster, due to the incremental feature that copies only the bytes that changed since the last execution.

Since the data is fully replicated on the target infrastructure you won’t be affected by any failure on the source, allowing disaster recovery scenarios.

 

### Migrating the VM from the replica

Since the replica execution completed, we can now get the VM to run on OpenStack. This requires a migration:

```text
coriolis migration deploy replica <replica id>
```
  
The command will return a migration id and info about the tasks that are going to be executed.

Like for the replica case, you can check the status of the migration:

```text
coriolis migration show <migration_id>
```
  
You can also list all migrations at once to get an overview of the status:

coriolis migration list

```text
coriolis migration list
```
  
Once the migration is completed, your VM will be up and running in OpenStack!

 

#### Troubleshooting

In a complex environment involving multiple clouds it becomes useful to get detailed information about possible issues. Coriolis logs all errors, warnings and other details in the **/var/log/coriolis** folder.

 
