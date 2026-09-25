---
title: "Oracle Cloud Infrastructure Classic (OCI-C/OPC) Coriolis Plugin"
wp_id: 38531
---

# Oracle Cloud Infrastructure Classic (OCI-C/OPC) Coriolis Plugin

! NOTE

This platform is no longer supported by Oracle and has been archived in Coriolis.

**Coriolis** integrates the platform Plugin on the Appliance itself, this way there is no need for agents to be deployed on platforms to establish the communication between the platform and the Coriolis components. Using this type of architecture, Coriolis guarantees the connection to the supported platform set up to be used as either Source or Destination, as long as the requirements are met.

In concordance with the legacy naming scheme, Coriolis's OCI-C plugin was initially labeled as the "OPC" (Oracle Public Cloud) plugin. For operations on "modern" OCI, please refer to the documentation section on the vanilla Oracle Cloud Infrastructure (OCI) Coriolis plugin.

[![](_static/images/image-4.png)](https://i0.wp.com/cloudbase.it/wp-content/uploads/2020/04/image-4.png?ssl=1)

## Deployment requirements and supported OCI-C instances

### Deployment requirements

The worker components of Coriolis need network access to the OCI-C APIs.

Additionally, network access from the Coriolis worker components to the Internet is required in order to reach temporary VMs Coriolis will be spawning on OCI-C during the migration/replication operations.

Alternatively, one may deploy the Coriolis worker components on OCI-C directly and thus avoid any API/VM network access limitations.

### Worker image requirements

#### Linux image requirements

The image used for the Disk Copy and OSMorphing worker instance might need a user called **opc**. The OCI-C plugin defaults to this user when setting up and sending SSH commands because most of the Oracle public images have **opc-init** installed, which includes the **opc** user. 

Recommended image: _/oracle/public/OL_7.5_UEKR4_x86_64_MIGRATION_

The above requirement doesn't apply when exporting instances from OCI-C. The default user can be set in the source environment (**export_img_username** option). Core Coriolis worker image requirements still apply (i.e. must have cloud-init installed).

#### Windows image requirements

There are no Windows public images on OCI-C, so the user must upload one. The default user is **Administrator**.

For more information regarding Coriolis Worker template, please check the **[Coriolis Temporary Migration Worker](https://cloudbase.it/coriolis-temporary-migration-worker) **page.

### Supported instances

**The OCI-C source Coriolis plugin only supports migrating OCI-C VMs which are running** , as a deprovisioned VM's disks can't be identified reliably.

OCI-C Coriolis plugin cannot replicate/migrate UEFI-based instances(not supported by OCI-C cloud).

## OCI-C as a source cloud

### Migrating (CMaaS) from OCI-C

Migrations from OCI-C operate in the same way Replicas do, and thus entail the same requirements and steps described below.

### Replicating (DRaaS) from OCI-C

**Input** : the names of the instances. The instance must be in the same region parameter supplied in the connection info used to create the OCI-C Coriolis endpoint.

Please consider reviewing the general steps recommended to be performed before creating migration for an instance from OCI-C [here](https://cloudbasedev.atlassian.net/wiki/spaces/COR/pages/1845333/Preparing+a+VM+for+migration+replication).

#### Steps performed by Coriolis

Considering there are unfortunately no publicly-available APIs for fetching the contents of disks of instances off of OCI-C, the OCI-C Coriolis plugin must bypass the issue by booting a temporary machine in order to Replicate the contents of the disks through.

  1. read the configuration of the instance on the source OCI-C (shape information, disks, etc…)
  2. create snapshots of all the volumes of the instance
  3. create a temporary instance on OCI (the "disk replication worker") and attach the volumes based on the snapshots created at step 2
  4. scan the disks of the VM being Replicated for written disk areas
  5. if this is the first Replica execution, transfer over all of the allocated disk chunks. If this is an incremental Replica execution, only transfer over the disk chunks which have changed since the last execution
  6. once the transfer of all disks is complete, delete the worker created at step 3 and its attached disks
  7. remove the volume snapshots created at step 2, along with any other temporary resources used in the disk copy process (such as the key pair for the disk copy worker)



During step 5, the data chunks will be handed directly to the destination cloud plugin, which will ensure they are written to the Replica disks on the destination.

### OSMorphing steps taken when migrating/replicating from OCI-C

For OCI-C guests, Coriolis will take the following OSMorphing steps as part of the migration process from OCI-C:

#### Linux

  * uninstalling OVMd (if applicable)



#### Windows

  * removing Windows PV drivers



### OCI-C source environment parameters

The source environment parameters are a set of source-cloud-specific parameters that offer some extra options and configurability to the migration/replication process on a per-VM basis.

Below is a listing of the source environment parameters the OCI-C plugin supports when migrating/replicating a VM from OCI:

#### Example of source environment JSON to be passed to the OCI-C plugin

```json
{
     "export_image_name": "/oracle/public/OL_7.2_UEKR4_x86_64",
     "export_img_username": "cloud-user",
     "export_shape_name": "oc3",
     "export_root_disk_size": 20
 }
```

Each parameter represents:

  * **export_image_name (string)** - name of a Linux image on OCI-C to use for the temporary VMs which will be exporting disk data from OCI-C
  * **export_img_username (string)** - username to use when a connection to the temporary disk copy worker
  * **export_shape_name (string)** - name of the shape to use for the temporary VMs which will be exporting disk data from OCI-C
  * **export_root_disk_size (integer)** - size (in GBs) of the root disk of temporary worker VMs. This is only affected by the selected image as the Coriolis Replica export process from OCI bears no extra storage requirements



Most source environment parameters can also be found in the global configuration section, in which case they may be overridden on a per-migration/replica basis by setting them in the destination environment as well.

### Source Configuration Options

Below is a listing of the configuration section needed when migrating from OCI-C:

#### Configuration options for OCI-C as a migration source

```ini
[opc_migration_provider]
 # Image used for the export worker
 export_image_name = /oracle/public/OL_7.2_UEKR4_x86_64
  
 # Shape used for export worker
 export_shape_name = oc3
  
 # Exporting an instance may require an extra disk to be attached, to accomodate the size of the
 # largest disks that belong to the exported instance. Make sure to allocate enough space here.
 export_root_disk_size = 150
  
 # Admin username for the export_image_name. Default username is 'opc'.
 # export_img_username = 
```

## OCI-C as a destination cloud

Coriolis' OCI-C plugin supports both migrating (CMaaS) and replicating (DRaaS) to OCI-C.

### Migrating (CMaaS) to OCI-C

Migrations to OCI-C operate in the same way Replicas do, and thus entail the same requirements and steps described below.

### Replicating (DRaaS) to OCI-C

#### Replica executions:

#### Steps performed by Coriolis

  1. if this is the first replica execution for the VM, create empty volumes on OCI-C, each matching the specifications of a disk the VM had on the source. If this is a later replica execution, the previously-created volumes are used
  2. if this is the first replica execution of the VM, create a new live-snapshot of the disks of the VM on the source cloud (handled by whatever source cloud plugin we are using). Is this is a later replica execution, create a new live-snapshot based on the one from the last successful replica execution
  3. create a temporary Linux worker VM in OCI-C (the "disk copy worker") on the destination cloud and attach the volumes from step 1 to it
  4. read the contents of the snapshot created at step 2 via the source platform's snapshot/backup APIs (handled by whatever source cloud plugin we are using), transferring the written chunks to the temporary VM created in step 3, which then writes the chunks at the appropriate index/offset of the disks created at step 1
  5. once the contents of all the disks have been synced to the volumes created at step 1, detach the volumes and delete the disk copy worker created at step 3



#### Replica deployments:

#### Steps performed by Coriolis

  1. create snapshots of the previously-replicated volumes on the OCI-C in order to be able to rollback any changes. By default, new volumes are created from these snapshots, leaving the original replica volumes intact for future replica executions
  2. depending on the OS of the VM whose replica is being deployed, boot a temporary worker VM ("the OSMorphing worker") with the same OS type on the destination cloud, and attach the volumes from step 1 to it
  3. perform the "OSMorphing process", where Coriolis commands the OSMorphing worker created at step 2 to scan all attached disks for the OS installation of the VM we are migrating, mount, and perform the steps needed to prepare the installation for the new platform (ex: uninstalling the VMWare guest tools and installing VirtIO drivers if deploying a replica of a Windows VM from source VMWare vSphere)
  4. detach the volumes created at step 1 from the OSMorphing worker created at step 2 and delete the temporary worker VM 
  5. create and boot the migrated VM on the destination cloud with the specifications of the original VM on the source cloud (which have been noted during the particular replica execution we are deploying), creating and attaching any necessary NICs and volumes.



### OSMorphing steps taken when migrating/replicating to OCI-C

Depending on the OS release being migrated/replicated, the following notable steps will be performed as part of the OSMorphing process:

#### Linux

  * installing cloud-init/OVMd
  * rebuilding initrd on RHEL-based systems



#### Windows

  * installing cloudbase-init and enabling cloudbase-init service
  * installing the VirtIO drivers



### Disk copy worker images

During the migration process from OCI-C, Coriolis creates a temporary worker VM to which it attaches snapshots of the original instance's disks to read them through it.

The disk reading process involves rsync transmission over an SSH channel, so both security and transfer efficiency should be maximized, though at the cost of the disk copy worker having to do some compression itself, which is why it is recommended to use more compute-capable instance shapes, such as from **oc3** onwards.

The images do **NOT** require any special Coriolis agent running in them and can be images already available on OCI-C, granted the following requirements:

  * image is recommended to be an Oracle Linux 7+
  * image must have OVMd installed and configured for an initial run on OCI-C



For each instance it is migrating, Coriolis will create a dedicated disk copy worker on OCI-C to fetch its storage.

For OS Morphing of Windows VM's it is required to have a Windows template that uses English edition or is set to use English as the system language 

### OCI-C destination environment parameters

The destination environment parameters are a set of destination-cloud-specific parameters that offer some extra options and configurability to the migration/replication process on a per-VM basis.

Below is a listing of the destination environment parameters the OCI-C plugin supports when migrating/replicating a VM to OCI-C:

#### Example of destination environment JSON to be passed to the OCI-C plugin

```json
{
     "network_map": {
         "source network name": "name of an existing IP network on destination OPC"
     },
     "storage_mappings": {
         "default": "/oracle/public/storage/default",
         "backend_mappings": [{"source": "datastor1", "destination": "/oracle/public/storage/default"}],
         "disk_mappings": [{"disk_id": "", "destination": "/oracle/public/storage/latency"}]
     },
     "migr_image_map": {
         "linux": "/oracle/public/OL_7.2_UEKR4_x86_64",
         
         "windows": "/Compute-a488347/user@mail.com/Windows_2012_R2"
     },
     "migr_shape_name": "oc3",
     "shape_name": "oc3",
     "default_volume_pool": "/oracle/public/storage/default",
     "keypair_name": "key1",
     "set_public_ip": true
 }
```

Each parameter represents:

  * **network_map (string-object mapping)** - a mapping between the names of networks on the source cloud and names of corresponding pre-existing IP networks on the destination OPC
  * **storage_mappings (string-object mapping)** - storage-related options such as how to map each disk or storage type on the source to OPC storage pools.
  * **migr_image_map (string-string mapping)** - if migrating/replicating a heterogeneous workload with both Linux and Windows instances, separate image names/IDs will need to be provided for the temporary OSMorphing workers for each OS. The only accepted keys are 'Linux' and 'Windows'. Please review the "OSMorphing worker images" section for exact details on the requirements of the worker images for each OS type
  * **migr_shape_name (string)** - name of the shape to use for temporary OCI-C worker VMs
  * **shape_name (string)** - name of the shape to use for migrated VM(s) on OCI-C (can be omitted, in which case Coriolis will pick the minimum viable shape in your stead)
  * **default_volume_pool (string)** - name of the default OPC storage pool if none is selected for a source disk or backend.
  * **keypair_name (string)** - name of the pre-created keypair of the account to use when creating the final migrated instance.
  * **set_public_ip (boolean)** - Whether or not the migrated instance will have a public IP attached to its first vNIC.



Most destination environment parameters can also be found in the global configuration section, in which case they may be overridden on a per-migration/replica basis by setting them in the destination environment as well.

### Configuration Options

Below is a listing of the configuration section needed when migrating/replicating to an OCI-C:

#### Configuration options for OCI-C as a destination

```ini
[opc_migration_provider]
 # Linux and Windows images for the temporary Worker VMs:
 migr_image_map = linux: /oracle/public/OL_7.2_UEKR4_x86_64, windows: /Compute-a488347/user@mail.com/Windows_2012_R2
  
 # The shape to use for the migration Worker VMs:
 migr_shape_name = oc3
  
 # Default volume pool to use. Oracle exposes 2 pools: "default" and "latency".
 # The default pool leverages rotary disks, while the latency disks are backed
 # by SSD and low latency storage subsystem. The latency pool is suitable for 
 # databases.
 default_volume_pool = default
  
 # Default network name used for worker instances
 # during migrations.
 migr_network_name = private
  
 # URL of a zip file with the Windows PV drivers:
 windows_pv_drivers_url = https://cloudbase.it/downloads/ovm_win_pv_drivers_all_323.zip 
```

#### Coriolis Advanced options for Target Destinations

In the case of Replicating or Migrating to Oracle Cloud Infrastructure Classic, there are the following requirements for the worker images: 

  * **Linux image requirements**



The image used for the Disk Copy and OSMorphing worker instance might need a user called opc. The OCI-C plugin defaults to this user when setting up and sending SSH commands because most of the Oracle public images have opc-init installed, which include the opc user.

  * **Windows image requirements**



There are no Windows public images on OCI-C, so the user must upload one. The default user is Administrator. 

The template OS version must be at least the same as the OS of the VM that needs to be Replicated or Migrated. 

**Option name (UI)**  | **Parameter**  | **Description**    
---|---|---  
Migration Image Map | migr_image_map | if migrating/replicating a heterogeneous workload with both Linux and Windows instances, separate image names/IDs will need to be provided for the temporary OSMorphing workers for each OS. The only accepted keys are 'Linux' and 'windows'. Please review the "OSMorphing worker images" section for exact details on the requirements of the worker images for each OS type   
Migration Shape Name | migr_shape_name | name of the shape to use for temporary OCI-C worker VMs   
Shape Name | shape_name | name of the shape to use for migrated VM(s) on OCI-C (can be omitted, in which case Coriolis will pick the minimum viable shape in your stead)   
Volume Pool | volume_pool | name of the default OPC storage pool if none is selected for a source disk or backend   
Keypair Name | keypair_name | name of the pre-created keypair of the account to use when creating the final migrated instance   
Set Public IP | set_public_ip | whether or not the migrated instance will have a public IP attached to its first vNIC   

## OCI-C connection parameters

In order to connect to OCI-C to perform a migration from it, the following connection parameters are required:

### Example of connection info JSON to be passed to the OCI-C plugin

```json
{
     "identity_domain": "a514847",
     "username": "user@email.com",
     "password": "SuperS3kre7",
     
     "api_endpoint": "https://compute.eucom-north-1.oraclecloud.com/",
     "storage_api_endpoint": "https://Storage-a514847.storage.oraclecloud.com/v1/Storage-6264247ef814462f8dd4908f3eaaf288",
     "storage_auth_endpoint": "https://Storage-6264247ef814462f8dd4908f3eaaf288.storage.oraclecloud.com/auth/v1.0"
 }
```

Each parameter representing:

  * **identity_domain (string)** - the OCI identity domain ID
  * **username (string)** - the username to login as. Must feature the trailing '@sub.domain' part
  * **password (string)** - the password for the given username
  * **api_endpoint (string)** - the full URL of the OCI-C API endpoint for the desired region
  * **storage_api_endpoint (string)** - the full URL of the OCI-C storage API endpoint for the desired region
  * **storage_auth_endpoint (string)** - the full URL of the OCI-C storage authentication API endpoint for the desired region



### OPC platform specifics

Supported Actions: | Migration Source/Destination - Replica Source/Destination| Comments  
---|---|---  
Plugin identifier| **opc**|  Identifies the plugin. Used for the **- provider** CLI parameter  
Credentials needed| Standard OPC user/pass credentials| Necessary credentials to give to Coriolis  
Deployment requirements| Coriolis worker component(s) need network access to the OCI-C APIs| Coriolis deployment and environment connectivity requirements  
Source disk export requirements| OCI-C is supported as a DRaaS source only through Coriolis' in-build data replication engine.The source VM must be running throughout the process.| Requirements to use the replica export (DRaaS source) features  
Instance identification scheme| VM names| How instances to migrate/replicate are identified on a source cloud handled by this plugin  
Network identification scheme| Names of OCI-C IP Networks| How networks are identified by the plugin. Required for the **network_map** field of the **- destination-environment**  
Storage identification scheme| Storage pool names| How storage backends are identified by the plugin. Required for the **storage_map** field of the **- destination-environment**
