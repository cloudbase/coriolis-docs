---
title: "Oracle Cloud Infrastructure (OCI) Coriolis Plugin"
wp_id: 38527
---

# Oracle Cloud Infrastructure (OCI) Coriolis Plugin

**Coriolis** integrates the platform Plugin on the Appliance itself, this way there is no need for agents to be deployed on platforms to establish the communication between the platform and the Coriolis components. Using this type of architecture, Coriolis guarantees the connection to the supported platform set up to be used as either Source or Destination, as long as the requirements are met.
This section describes the functionality available via Coriolis' OCI plugin, enabling Coriolis to migrate (CMaaS) and replicate (DRaaS) instances to OCI.

[![](_static/images/image-3.png)](https://i0.wp.com/cloudbase.it/wp-content/uploads/2020/04/image-3.png?ssl=1)

### Deployment requirements

The worker components of Coriolis need network access to the public OCI API.

Additionally, network access from the Coriolis worker components to the Internet is required to reach temporary VMs Coriolis will be spawning on OCI during the migration/replication operations.

Alternatively, one may deploy the Coriolis worker components on OCI directly and thus avoid any API/VM network access limitations.

### Migrating Windows VMs

When migrating Windows VMs, the OSMorphing workers need to install VirtIO drivers to the migrated Windows VMs to make sure they boot properly on OCI. 

The user needs to self-host the drivers using their Oracle account, by accepting Oracle's EULA and downloading the ZIP file containing the drivers. Downloading steps can be found [here](https://docs.oracle.com/en/operating-systems/oracle-linux/kvm-virtio/kvm-virtio-DownloadingtheOracleVirtIODriversforMicrosoftWindows.html#kvm-virtio-download) under the **Downloading the Oracle VirtIO Drivers** section.

As of June 2024, the latest version of the **Oracle VirtIO Drivers Version for Microsoft Windows is 2.1.0** , the archive filename is **V1037432-01.zip** (44.4 MB).

Please ensure that the zip archive contains the file "winvirtio.iso" as Coriolis will be requiring that to slipstream the Windows VirtIO drivers.

The ZIP file's URL is then used in the Migration/Replica settings or can be passed to the **windows_virtio_zip_url** configuration option in **coriolis.conf**.

Refer to the [Oracle VirtIO Drivers for Microsoft Windows for Use With KVM page](https://docs.oracle.com/en/operating-systems/oracle-linux/kvm-virtio/kvm-virtio-WhatsNew.html#kvm-virtio-supported-os) for more details on the VirtIO drivers support matrix for Windows guest versions.

### Oracle Cloud Infrastructure as a destination cloud

Coriolis' Oracle Cloud Infrastructure plugin supports both migrating (CMaaS) and replicating (DRaaS) to OCI.

### Migrating (CMaaS) to Oracle Cloud Infrastructure

#### Steps performed by Coriolis

Migrations to OCI operate like Replicas do and thus entail the same requirements and steps described below.

### Replicating (DRaaS) to Oracle Cloud Infrastructure

#### Replica executions:

#### Steps performed by Coriolis

  1. if this is the first replica execution for the VM, create an empty boot volume (this is achieved by creating a VM with an all-zeros image and tearing it down) as well as empty data disks on OCI, each matching the specifications of a disk the VM had on the source. If this is a later replica execution, the previously created boot volume and disks are used
  2. if this is the first replica execution of the VM, create a new live snapshot of the disks of the VM on the source cloud (handled by whatever source cloud plugin we are using). If this is a later replica execution, create a new live snapshot based on the one from the last successful replica execution
  3. create a temporary Linux worker VM on OCI (the "disk copy worker") and attach the boot volume and data disks from step 1 to it
  4. read the contents of the snapshot created at step 2 via the source platform's snapshot/backup APIs (handled by whatever source cloud plugin we are using), transferring the written chunks to the temporary VM created in step 3, which then writes the chunks at the appropriate index/offset of the disks created at step 1
  5. once the contents of all the disks have been synced to the disks created in Step 1, detach the disks and delete the disk copy worker created in Step 3



#### Replica deployments:

#### Steps performed by Coriolis

  1. create snapshots of the already-replicated boot volume and data disks on OCI. By default, new disks are created from these snapshots, leaving the original replica volumes intact for future replica executions
  2. depending on the OS of the VM getting migrated, boot another temporary worker VM ("the OSMorphing worker") with the same OS type on the destination cloud, and attach the boot volume and data disks from steps 1 and 2 to it
  3. perform the "OSMorphing process", where Coriolis commands the OSMorphing worker created in step 2 to scan all attached disks for the OS installation of the VM we are migrating, mount, and perform the steps needed to prepare the installation for OCI
  4. [Linux] injects a temporary initrd into the VM which will allow for connection and reconfiguration of iSCSI targets on the first boot
  5. detach the boot volume and disks of the replicated VM from the OSMorphing worker created in step 2 and delete the worker VM 
  6. create the migrated VM on OCI with the specifications of the original VM on the source cloud (which have been passed into the OCI plugin from whatever migration source plugin we were using to export the VM off the source cloud), creating and attaching any necessary NICs and disks to it



### OCI using Coriolis Minion Pools

By default, Coriolis automatically creates and cleans up all of the temporary resources it needs throughout the transfer, thus only limiting resources used to the duration of the transfer itself, but at the cost of time overhead for the actual creation/cleanup of the temporary resources.

In cases where resource usage limitations are not a factor, or where the time cost outweighs the resource allocation costs, Coriolis offers the ability to pre-allocate the Minion Machines on source/destination platforms into so-called “Minion Machine Pools”.

For more information, please check the **[Minion Pools page](https://cloudbase.it/coriolis-minion-pools-operations-and-usage)**.

### OSMorphing steps taken when Migrating/Replicating to OCI

The following other notable steps will be performed as part of the OSMorphing process:

#### Linux

  * rebuilding initrd on RHEL-based systems
  * install the latest available kernel for Oracle Linux and Ubuntu Server 
    * This is to ensure that the required drivers are present and updated when running on OCI
  * installing cloud-init
  * applying appropriate iSCSI configurations



#### Windows

  * due to worker image initialization issues as well as increased complexity during OSMorphing, migrating/replicating Windows VMs to OCI is currently unsupported as **Native**
  * migrations are supported only for **Emulated or Paravirtualized instances**.



### OSMorphing worker images

The OSMorphing worker images (governed by the **migr_image_map**  option) which are used for temporary disk copy/OSMorphing VMs on OCI bear no special requirements and any generic Oracle Linux or Windows OCI image may be used as long as they have cloud-init or Cloudbase-init installed and configured for a first run. Windows worker image must be an English edition or set to use English as the system language.

For more information regarding the Coriolis Worker template, please check the **[Coriolis Temporary Migration Worker](https://cloudbase.it/coriolis-temporary-migration-worker) **page.

###  Oracle Cloud Infrastructure user/group policy requirements 

Coriolis allows users to choose two compartments when migrating to OCI, for more details regarding the compartments and their requirements, follow **[Oracle Cloud Infrastructure user/group policy requirements documentation](https://cloudbase.it/oracle-cloud-infrastructure-user-group-policy-requirements)**.

### Oracle Cloud Infrastructure connection parameters

To connect to OCI to perform a migration/replica to it, the following connection parameters must be supplied:

#### Example of connection info JSON to be passed to the OCI plugin

```json
{
     "region": "",
     "tenancy": "",
     "user": "",
     "private_key_passphrase": "",
     "private_key_data": "",
     "fingerprint": "private_key_fingerprint_hex"
 }
```

The parameters representing

  * **region (string)** - the name of the OCI region (example: us-phoenix-1)
  * **tenancy (string)** - ID of the OCI tenancy
  * **user  (string)** - ID of the OCI user
  * **private_key_data (string)** - a string containing the private key in .pem file format
  * **private_key_passphrase  (string)** - string passphrase for the private key (if any)
  * **fingerprint (string)** - MD5 fingerprint of the private key data (optional)



For more information on how to generate the PKI, see the [Oracle documentation](https://docs.oracle.com/en-us/iaas/Content/API/Concepts/apisigningkey.htm).

### OCI destination environment parameters

The destination environment parameters are a set of key-value pairs (some may have nested key-value pairs of their own), that allow you to overwrite default values set in the provider. For example, you may configure the OCI provider to behave in a certain way. Still, for some migrations of replicas, you would like to overwrite that behavior with a different set of settings.

Below is a listing of the destination environment parameters the OCI plugin supports when migrating/replicating a VM to OCI:

#### Example of destination environment JSON to be passed to the OCI plugin

```json
{
     "network_map": {
         "source_network_1": {
             "id": "",
             "security_groups": ["network_secgroup_id_1", …]
     },
     "storage_mapping": {
         "default": "emulated",
         "backend_mappings": [{"source": "datastor1", "destination": "iscsi"}],
         "disk_mappings": [{"disk_id": "", "destination": "paravirtualized"}]
     },
     "use_pv_mode": true,
     "availability_domain": "",
     "compartment": "",
     "vcn_compartment": "",
     "set_public_ip": true,
     "migr_subnet_id": "",
     "migr_image_map": {
         "linux": "",
         "windows": ""
     }
     "migr_shape_name": "VM.Standard1.2",
     "shape_name": "VM.Standard2.2",
 }
```

A short description of the parameters:

  * **availability_domain (string)** - ID of the availability domain on OCI 
  * **network_map (string-object mapping)** - a mapping between the names of networks on the source cloud and a corresponding pre-existing network on OCI, in addition to an optional list of security groups
  * **storage_mappings (string-object mapping)** - a mapping between source storage backend names and OCI volume attachment types (not compatible with root disks).
  * **use_pv_mode** **(boolean)** - Whether or not to use para-virtualized mode for instances running on BIOS firmware.
  * **migr_image_map (string-string mapping)** - a mapping between os types (accepted keys being either 'Linux' or 'windows') and image IDs on OCI
  * **migr_subnet_id (string)** - ID of the subnet where worker VMs will have NICs attached
  * **migr_shape_name (string)** - Name of the OCI shape to be used for the worker instance.
  * **compartment (string)** - the name of the OCI compartment to boot the use for the Migration/Replica 
  * **vcn_compartment (string)** - This option allows the selection of VCNs from a different compartment
  * **set_public_ip (boolean)** - whether or not to set a public IP address for the migrated VM
  * **shape_name (string)** - Name of the OCI shape used when creating the final migrated instance.



Destination environment parameters are also exposed in the **[oci_migration_provider]** section of the Coriolis configuration file. Setting a value for any of the above parameters in the config will provide defaults for options that are not explicitly set by the user during Migration/Replica creation.

### Configuration Options

Below is a listing of the configuration section needed when migrating/replicating to OCI:

#### Configuration options for OCI as a destination

```json
 [oci_migration_provider]
  
 # Default image names used for worker instances during migrations:
 migr_image_map = linux: <linux_image_ID>, windows: <windows_image_ID>
  
 # Whether to use paravirtualized mode by default for
 # instances that use BIOS.
 default_to_pv_mode = true
  
 # Default shape name used for final instances:
 shape_name = VM.Standard2.8
  
 # Default shape name used for worker instances during migration/replica:
 migr_shape_name = VM.Standard2.8
  
 # Default subnet id used for worker instances during migration/replica:
 migr_subnet_id = <migr_subnet_id_value>
  
 # Default compartment in which the migration/replica should take place:
 compartment = <compartment_name_value>
  
 # Fallback option for determining whether or not to create and
 # associate a public IP for the Migrated VMs:
 set_public_ip = true/false
  
 # Default attach type to be used when attaching secondary
 # disks to the migrated instance. Accepted values:
 # 'iscsi', 'emulated', 'paravirtualized'
 default_attach_type = iscsi
  
 # Windows VMs that are migrated to OCI need virtio drivers.
 # Please refer to the documentation page of the Coriolis OCI plugin for more
 # information on how to obtain the .zip file containing the drivers:
 # https://cloudbase.it/oracle-cloud-infrastructure-oci-coriolis-plugin/
 # The downloaded ZIP has to be self-hosted. Paste the ZIP URL to the option below:
 # windows_virtio_zip_url = https://example.com/virtio-1.1.3.zip 
```

#### Coriolis Advanced Options for Target Destinations

In the case of Replicating or Migrating to Oracle Cloud Infrastructure, the required parameters are to be selected from the ones available in the OCI environment, also select the correct versions for Windows and Linux “Migration Image Map”. The template OS version must be at least the same as the OS of the VM that needs to be migrated. 

**Option name (UI)**  | **Parameter**  | **Description**    
---|---|---  
Availability Domain | availability_domain | ID of the availability domain on OCI   
Use Paravirtualized Mode | use_pv_mode | whether to use para-virtualized mode for instances running on BIOS firmware.   
Migration Image Map | migr_image_map | a mapping between OS types (accepted keys being either 'Linux' or 'windows') and image IDs on OCI   
Migration Subnet ID | migr_subnet_id | ID of the subnet where worker VMs will have NICs attached   
Migration Shape Name | migr_shape_name | name of the OCI shape to be used for the worker instance.   
VCN Compartment ID | vcn_compartment | this option allows the selection of VCNs from a different compartment   
Set Public IP | set_public_ip | whether to set a public IP address for the migrated VM   
Shape Name | shape_name | name of the OCI shape used when creating the final migrated instance.   

### Storage Mapping Limitations

When migrating VMs to OCI, source cloud data disks are mapped to OCI-specific [attachment types](https://docs.cloud.oracle.com/iaas/Content/Block/Concepts/overview.htm#iSCSI). Coriolis will use this mapping when attaching the replicated data disks to the migrated instance. 

The worker VM will always use the iSCSi attachment type when replicating/migrating disks.

When the source cloud disks get replicated, Coriolis first creates an empty volume using a custom all-zero image(also created by Coriolis when needed). Since each image has a launch mode, and each launch mode has its predefined boot volume type, storage mapping is limited to data disks. 

More about custom images and launch modes: <https://docs.cloud.oracle.com/iaas/Content/Compute/Tasks/imageimportexport.htm>

### Launch mode characteristics and compatibility

**OCI Launch Mode**| **Firmware**| **NIC Attachment Type**| **Boot Volume Type**|  **Remote Data Volume**| **Supported Block Volume Attachment Types**| **Supported Shapes**  
---|---|---|---|---|---|---  
Native| UEFI| Directly Attached| iSCSI| Paravirtualized| iSCSI, Paravirtualized| All VM and bare-metal shapes supported  
Paravirtualized| BIOS| Paravirtualized NIC| Paravirtualized SCSI| Paravirtualized SCSI| iSCSI, Paravirtualized| Only VM shapes supported  
Emulated| BIOS| Emulated NIC| IDE| Emulated SCSI| iSCSI, Emulated| Only VM shapes supported  

### OCI platform specifics

Supported Actions: | Migration Destination - Replica Destination| Comments  
---|---|---  
Plugin identifier| **oci**|  Identifies the plugin. Used for the **- provider** CLI parameter  
Credentials needed| User name and private key| Necessary credentials to give to Coriolis  
Deployment requirements| Coriolis worker component(s) need network access to the OCI APIs.| Coriolis deployment and environment connectivity requirements  
DRaaS source requirements| OCI is not currently supported as a DRaaS source| Requirements to use the replica export (DRaaS source) features  
Instance identification scheme| Names must be unique| How instances to migrate/replicate are identified on a source cloud handled by this plugin  
Network identification scheme| IDs the OCI VCNs and their Subnets| How networks are identified by the plugin. Required for the **network_map** field of the **- destination-environment**
