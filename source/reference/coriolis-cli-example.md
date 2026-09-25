---
title: "Coriolis CLI Replica/Migration task"
wp_id: 40005
---

# Coriolis CLI Replica/Migration task

## Installing the Coriolis command line client

The following commands will install the Coriolis command line client on the local machine.

### Coriolis CLI installation commands

```bash
$ git clone https://github.com/cloudbase/python-coriolisclient
$ pip3 install python-coriolisclient
$ # verify client is available in path:
$ /usr/bin/env coriolis
```
  
### Expose Coriolis appliance

By default, all the Coriolis appliance services listen only on localhost. In order to expose all the services from the appliance, execute the following:

```bash
$ ~/coriolis-docker/expose_coriolis.py 
```
  
## Defining a Coriolis endpoint for a given cloud

Defining Endpoints in Coriolis represent a one time job, once stored Coriolis will be able to use the Endpoint details to further perform Replica/Migration jobs.

For instructions on how to create Coriolis Endpoints please check Defining a Coriolis endpoint for a given cloud under **[Coriolis CLI](https://cloudbase.it/coriolis-cli)** page.

## Creating migration jobs

### Prerequisites

  * an existing Coriolis endpoint for the migration source cloud (granted the source cloud has a Coriolis platform plugin available)
  * an existing Coriolis endpoint for the migration destination cloud (granted the source cloud has a Coriolis platform plugin available)
  * the parameters for the **- source-environment**, which are source cloud specific. Please review the documentation of the Coriolis platform plugin of the source cloud for the exact parameters which are expected 
  * the parameters for the **- destination-environment**, which are destination cloud specific. Please review the documentation of the Coriolis platform plugin of the destination cloud for the exact parameters which are expected 
  * a unique identifier of the instance we would like to migrate



Granted all the above, a migration job may be created for an instance by running the following:

```text
source /etc/kolla/admin-openrc.sh
 
coriolis migration create \
--origin-endpoint $ID_OF_SOURCE_CLOUD_ENDPOINT \
--destination-endpoint $ID_OF_DESTINATION_CLOUD_ENDPOINT \
--source-environment '{"the": "source cloud specific params"}' \
--destination-environment '{"the": "destination cloud specific params"}' \
--instance $IDENTIFIER_OF_INSTANCE_ON_SOURCE
```
  
The above command will create a migration job within Coriolis, which may be later queried or halted by referencing its ID.

### Additional operations for Coriolis migrations

In addition to the above create command, the Coriolis command line client also offers the following operations on migration jobs:

```text
source /etc/kolla/admin-openrc.sh
 
# list all registered migration jobs:
coriolis migration list
 
# view a particular migration's status:
coriolis migration show $MIGRATION_ID
 
# cancel a running migration:
coriolis migration cancel $MIGRATION_ID
 
# delete records of a previous migration:
# this does not delete the migrated instance on the destination cloud
# should that migration have been ended successfully.
# the migration must not be running.
coriolis migration delete $MIGRATION_ID
```
  
## Creating replication (DRaaS) jobs

### Prerequisites

  * an existing Coriolis endpoint for the replication source cloud (granted the source cloud has a Coriolis platform plugin available)
  * an existing Coriolis endpoint for the replication destination cloud (granted the source cloud has a Coriolis platform plugin available)
  * the parameters for the **- source-environment**, which are source cloud specific. Please review the documentation of the Coriolis platform plugin of the source cloud for the exact parameters which are expected 
  * the parameters for the **- destination-environment**, which are destination cloud specific. Please review the documentation of the Coriolis platform plugin of the destination cloud for the exact parameters which are expected 
  * a unique identifier of the instance we would like to replicate



Granted all the above, a replication job may be **defined**  (but not yet executed) for an instance by running the following:

```text
source /etc/kolla/admin-openrc.sh
 
coriolis replica create \
--origin-endpoint $ID_OF_SOURCE_CLOUD_ENDPOINT \
--destination-endpoint $ID_OF_DESTINATION_CLOUD_ENDPOINT \
--source-environment '{"the": "source cloud specific params"}' \
--destination-environment '{"the": "destination cloud specific params"}' \
--network-map '{"source network name": "name or ID of network on destination"}' \
--instance $IDENTIFIER_OF_INSTANCE_ON_SOURCE
```
  
The above command will define a replication job with Coriolis, which may be later have executions (syncs) scheduled, cancelled and deployed by referencing the replication job's ID.

#### Cloud specific parameters for Source/Destination environments

For more information regarding the **Source/Destination cloud specific parameters** , please check the **[Coriolis Replica/Migration parameters](https://cloudbase.it/coriolis-replica-migration-cli-parameters)** list.

The list that is available on **Coriolis Replica/Migration parameters** page can be shown using the following commands on Coriolis machine:

```text
$coriolis endpoint list
#listing all available coriolis endpoints

$coriolis provider schema list $platform_type source/destination
#listing the schema available for the selected type of platform specific for source or destination

$coriolis endpoint source/destination options list $ENDPOINT_ID
#listing all the available options for the endpoint depending if source or destination was chosen
```
  
### Starting an execution for a replication job

**Prerequisites** : an already defined replication job which does not already have a running execution

An existing replica may have a new execution (sync run) started by running the following:

```text
source /etc/kolla/admin-openrc.sh
 
coriolis replica execute $REPLICA_ID
```
  
The above command will launch a new replica execution, which may later be queried for status, cancelled or deleted by referencing both the ID of the replica, and the ID of the newly-created replica execution.

### Additional operations for Coriolis replica executions

In addition to the above execution command, the Coriolis command line client also offers the following operations on replica executions:

```text
source /etc/kolla/admin-openrc.sh
 
# list all executions of a replica:
coriolis replica execution list $REPLICA_ID
 
# view a particular replica execution's status:
coriolis replica execution show $REPLICA_ID $REPLICA_EXECUTION_ID
 
# cancel a running replica execution:
coriolis replica execution cancel $REPLICA_ID $REPLICA_EXECUTION_ID
 
 
# delete records of a non-running replica execution:
# this will not delete any resources which might have been
# replicated on the destination cloud if the replica execution
# had completed successfully (such as the replica disks)
coriolis replica execution delete $REPLICA_ID $REPLICA_EXECUTION_ID
 
 
# delete the replica disks:
# this will delete the disks on the destination cloud we are
# replicating to, but it will not delete replica in Coriolis.
# Later executions may be launched for the replica, but the next one
# will be a full execution to completely new disks on the destination.
coriolis replica disks delete $REPLICA_ID
```
  
### Deploying a replica on the destination cloud

**Prerequisite** : a pre-existing Coriolis replica which has at least one successful replica execution

An existing replica may be deployed on the destination cloud by running the following:

```text
source /etc/kolla/admin-openrc.sh
 
coriolis migration deploy replica $REPLICA_ID
```
  
The above command will start a replica migration job which will recreate the instance on the destination cloud with the state of the last replica execution.

Using the replica migration job's ID to reference it, you may run the same "**coriolis migration …**" operations detailed in the section on creating migration jobs.

## Replica execution example

The following will demonstrate how a Replica task can be created, performed and inspected using Coriolis' CLI.

In the example **VMware** will be used as **source platform** and**OVM** will be used as **destination platform**.

**The source environment parameters** are a set of source-cloud-specific parameters that offer some extra options to the migration/replication process on a per-VM basis.

Below is a listing of the source environment parameters the VMWare plugin supports when migrating/replicating a VM from vSphere/ESXi:

```json
{
"vixdisklib_compatibility_version": "6.7",
"automatically_enable_cbt": false
}
```
  
Each Parameter representing:

  * **vixdisklib_compatibility_version**  (string) - The vSphere version for which to initialize vixDiskLib.
  * **automatically_enable_cbt**  (boolean) - Whether or not Coriolis should attempt to automatically enable CBT on the VM before Replication.



**The destination environment parameters** are a set of destination-cloud-specific parameters that offer some extra options and configurability to the migration/replication process on a per-VM basis.

Below is a listing of the destination environment parameters the OVM plugin supports when migrating/replicating a VM to OVM:

```text
'{
      "network_map": {
          "source network name": "0a6b0100",
      },
      "storage_mappings": {
          "backend_mappings": [{"source": "datastor1", "destination": "Main"}],
          "disk_mappings": [{"disk_id": "2000", "destination": "Main"}]
      },
      "server_pool_name": "Main",
      "repository_name": "Main",
      "migr_template_name_map": {
          "linux": "linux_migration_worker",
 }, "migr_template_username_map": { "linux": "root" }, "migr_template_password_map": { "linux": "Passw0rd" }, "leave_migrated_vm_off": false, "os_label": "coriolis-migrated", "virtual_disk_clone_type": "THIN_CLONE"'
```
  
Each parameter representing:

  * **network_map**  (string-string mapping) - a mapping between the names of networks on the source cloud and names or of corresponding pre-existing networks on the destination OVM
  * **storage_mappings**  (string-object mapping) - storage-related options such as how to map each disk or storage type on the source to repositories on OVM
  * **server_pool_name**  (string) - name of the server pool to create migrated/replicated VMs, as well as temporary worker VMs
  * **repository_name**  (string) - name of the storage repository to store migrated/replicated VMs in
  * **migr_template_map**  (string-string mapping) - if migrating/replicating a heterogeneous workload with both Linux and Windows instances, separate template names will need to be provided for the temporary OSMorphing workers for each OS. Only accepted keys are 'linux' and 'windows'. Please review the "OSMorphing worker images" section for exact details on the requirements of the worker images for each OS type
  * **migr_template_username_map**  (string) - Mapping between OS types and the pre-created usernames of the corresponding template set in the 'migr_template_name_map' to be used for the temporary worker VMs.
  * **migr_template_password_map**  (string) - Mapping between OS types and the pre-set password of the corresponding template set in the 'migr_template_name_map' to be used for the temporary worker VMs.
  * **leave_migrated_vm_off**  (boolean) - whether or not to just create VMs but skip powering them on
  * **os_label**  (string) - Label for the new OS on OVM
  * **virtual_disk_clone_type**  (string) - What cloning method to use when creating migrated disks. The 'Thin Clone' option is recommended, though it may not be supported by all OVM storage repository types.



#### Execution script example

```text
coriolis replica create \
     --origin-endpoint 0b9774fd-c39b-4c7e-acf8-4ba37dad155e \
     --destination-endpoint 807e2f7f-fcd6-4423-a0f6-7550277f2182 \
     --source-environment '{"vixdisklib_compatibility_version": "6.7", "automatically_enable_cbt": true}' \
     --destination-environment '{"network_map": {"vmnetwork": "0a6b0100"}, "storage_mappings": {"backend_mappings": [{"source": "datastore1", "destination": "Main"}], "disk_mappings": [{"disk_id": "2000", "destination": "Main"}]}, "server_pool_name": "Main", "repository_name": "Main", "migr_template_map": {"linux": "linux_migration_worker"}, "migr_template_username_map": { "linux": "root" }, "migr_template_password_map": { "linux": "Passw0rd" }, "leave_migrated_vm_off": false, "os_label": "coriolis-migrated", "virtual_disk_clone_type": "THIN_CLONE"}' \
      --network-map '{"vmnetwork": "0a6b0100"}' \
      --instance ha-datacenter/Ubuntu-Bionic-Demo \
```
  
Verifying the current Replica tasks:

```text
$coriolis replica list
#listing all availale coriolis replicas

 | ID                                  | Instances                       | Notes             | Last Execution Status | Created

 | 926a49bb-2bd9-4533-87e1-2d0e7505e06d| ha-datacenter/Ubuntu-Bionic-Demo| Ubuntu-Bionic-Demo| COMPLETED| 2021-04-08T07:26:35.000000|
```
  
Using the Replica ID, the Replica can be further inspected:

```text
$coriolis replica show 926a49bb-2bd9-4533-87e1-2d0e7505e06d
#inspecting the coriolis replica
```
  
```text
  Field                                    | Value       
------------------------------------------------------------------------------------                                    
  id                                       | 926a49bb-2bd9-4533-87e1-2d0e7505e06d            
  created                                  | 2021-04-08T07:26:35.000000                      
  last_updated                             | 2021-04-08T08:29:21.000000                      
  reservation_id                           | 746a8605-a60f-4475-88d2-d6d4205fa160            
  instances                                | ha-datacenter/Ubuntu-Bionic-Demo                
  notes                                    | Ubuntu-Bionic-Demo                              
  origin_endpoint_id                       | 0b9774fd-c39b-4c7e-acf8-4ba37dad155e            
  origin_minion_pool_id                    | None                                            
  destination_endpoint_id                  | 807e2f7f-fcd6-4423-a0f6-7550277f2182            
  destination_minion_pool_id               | None                                            
  instance_osmorphing_minion_pool_mappings | {}                                              
  destination_environment                  | {                                               
                                           |   "leave_migrated_vm_off": false,               
                                           |   "virtual_disk_clone_type": "THIN_CLONE",      
                                           |   "os_label": "Other Linux",                    
                                           |   "repository_name": "Main",                    
                                           |   "server_pool_name": "Main",                   
                                           |   "migr_template_map": {                        
                                           |     "linux": "0004fb0000060000917777556dc30f6c" 
                                           |   },                                            
                                           |   "migr_template_password_map": {               
                                           |     "linux": "Passw0rd"                         
                                           |   },                                            
                                           |   "migr_template_username_map": {               
                                           |     "linux": "root"                             
                                           |   },                                            
                                           |   "network_map": {                              
                                           |     "vmnetwork": "0a6b0100"                     
                                           |   },                                            
                                           |   "storage_mappings": {                         
                                           |     "backend_mappings": [                       
                                           |       {                                         
                                           |         "source": "datastore1",                 
                                           |         "destination": "Main"                   
                                           |       }                                         
                                           |     ],                                          
                                           |     "disk_mappings": [                          
                                           |       {                                         
                                           |         "disk_id": "2000",                      
                                           |         "destination": "Main"                   
                                           |       }                                         
                                           |     ]                                           
                                           |   }                                             
                                           | }                                               
  source_environment                       | {                                               
                                           |   "automatically_enable_cbt": true,             
                                           |   "vixdisklib_compatibility_version": "6.7"     
                                           | }                                               
  network_map                              | {                                               
                                           |   "vmnetwork": "0a6b0100"                       
                                           | }                                               
  disk_storage_mappings                    | '2000'='Main'                                   
  storage_backend_mappings                 | 'datastore1'='Main'                             
  default_storage_backend                  | None                                            
  user_scripts                             | {}                                              
  executions                               | 9a2cf852-1efd-48b7-aa14-fd08663a0e23 COMPLETED  
                                           | 7a91d209-5843-4dc2-869d-27e0d5b37ade COMPLETED  
                                           | 86ce4c6f-7a44-4651-8b43-55744416910e COMPLETED  
```
  
#### Defining Coriolis default parameters for Source/Destination environments

Some of the parameters can be set as default by editing the **coriolis.conf** file.

The coriolis.conf file is available on the Coriolis Appliance:

```text
$cd /etc/coriolis/coriolis.conf
```
  
For the example above, some parameters that can be set as default are **server_pool_name , repository_name , migr_template_map , migr_template_username_map , migr_template_password_map**.

After the parameters are set as default and the newly edited **coriolis.conf** file is saved, a restart of the **Coriolis Worker container** is required.

```text
$docker restart coriolis-worker
```
  
Once the Coriolis Worker container is up and running after the restart, the **Replica/Migration command** can be run **without** adding the **parameters** that were set as default in the **coriolis.conf** file.

#### Coriolis Replica Schedule

List of Coriolis Replica Schedule commands:

```text
coriolis replica schedule create $replica_ID
#creating a new schedule for an existing replica
coriolis replica schedule delete $replica_ID
#deleting on schedule for a replica
coriolis replica schedule list $replica_ID
#listing all the available schedules for a replica
coriolis replica schedule show $replica_ID $schedule_ID
#listing the details of a schedule that is part of a replica
coriolis replica schedule update $replica_ID $schedule_ID
#updating the configuration of a replica schedule
```
  
Coriolis Replica Schedule details using the above execution example:

```text
$coriolis replica list
#listing all available coriolis replicas

 | ID                                  | Instances                       | Notes             | Last Execution Status| Created

 | 926a49bb-2bd9-4533-87e1-2d0e7505e06d| ha-datacenter/Ubuntu-Bionic-Demo| Ubuntu-Bionic-Demo| COMPLETED| 2021-04-08T07:26:35.000000
-------------------------------------------------------------------------------------------------------------------

$coriolis replica schedule list 926a49bb-2bd9-4533-87e1-2d0e7505e06d
#listing all schedules for the requested replica

| Replica ID                          | ID                                  | Schedule                            | 

| 926a49bb-2bd9-4533-87e1-2d0e7505e06d| 16e3f953-a38d-4235-87e4-b2dac4ee160b| {'hour': 22, 'minute': 0, 'dom': 30} | 
-------------------------------------------------------------------------------------------------------------------

$coriolis replica schedule show 926a49bb-2bd9-4533-87e1-2d0e7505e06d 16e3f953-a38d-4235-87e4-b2dac4ee160b
#inspecting the requested schedule of that replica

 +-------------------+--------------------------------------+
 | Field             | Value                                |
 +-------------------+--------------------------------------+
 | id                | 16e3f953-a38d-4235-87e4-b2dac4ee160b |
 | replica_id        | 926a49bb-2bd9-4533-87e1-2d0e7505e06d |
 | schedule          | {'hour': 22, 'minute': 0, 'dom': 30} |
 | created           | 2021-04-09T09:39:44.000000           |
 | last_updated      | 2021-04-09T09:40:25.000000           
 | enabled           | True                                 |
 | expires           | 2021-06-29T21:00:00.000000           |
 | shutdown_instance | False                                |
 +-------------------+--------------------------------------+
```
