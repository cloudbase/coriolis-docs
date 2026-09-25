---
title: "OVM as a destination cloud"
wp_id: 39520
---

# OVM as a destination cloud

### Migrating (CMaaS) to OVM

NOTE! Support for OVM as a target platform in Coriolis has been deprecated. This documentation will be kept for reference, but the plugin is no longer maintained or supported.

### Replicating (DRaaS) to OVM

####   
Replica executions:

**Steps performed by Coriolis** :

  1. if this is the first replica execution for the VM, create empty disks on OVM, each matching the specifications of a disk the VM had on the source. If this is a later replica execution, the previously-created volumes are used
  2. if this is the first replica execution of the VM, create a new live snapshot of the disks of the VM on the source cloud (handled by whatever source cloud plugin we are using). If this is a later replica execution, create a new live snapshot based on the one from the last successful replica execution
  3. create a temporary Linux worker VM in OVM (the "disk copy worker") on the destination cloud and attach the volumes from step 1 to it
  4. read the contents of the snapshot created at step 2 via the source platform's snapshot/backup APIs (handled by whatever source cloud plugin we are using), transferring the written chunks to the temporary VM created in step 3, which then writes the chunks at the appropriate index/offset of the disks created at step 1
  5. once the contents of all the disks have been synced to the volumes created during step 1, detach the volumes and delete the disk copy worker created during step 3



#### Replica deployments:

**Steps performed by Coriolis** :

  1. create snapshots of the previously-replicated volumes on the OVM in order to be able to roll back any changes. By default, new volumes are created from these snapshots, leaving the original replica volumes intact for future replica executions
  2. depending on the OS of the VM whose replica is being deployed, boot a temporary worker VM ("the OSMorphing worker") with the same OS type on the destination cloud, and attach the volumes from step 1 to it
  3. perform the "OSMorphing process", where Coriolis commands the OSMorphing worker created during step 2 to scan all attached disks for the OS installation of the VM we are migrating, mount, and perform the steps needed to prepare the installation for the new platform (ex: uninstalling the VMWare guest tools and installing VirtIO drivers if deploying a replica of a Windows VM from source VMWare vSphere)
  4. detach the volumes created at step 1 from the OSMorphing worker created at step 2 and delete the temporary worker VM 
  5. create and boot the migrated VM on OVM with the specifications of the original VM on the source cloud (which have been noted during the particular replica execution we are deploying), creating and attaching any necessary NICs and volumes.



### Configuration Options

**Coriolis Advanced options for Target Destinations**

In the case of Replicating or Migrating to Oracle VM, there will have to be VM templates on the destination platform having set username and password for the Coriolis worker to access it and use it as a temporary VM.  This is valid for both Windows and Linux machines, and the template OS version must be at least the same as the OS of the VM that needs to be Replicated or Migrated.

[![](_static/images/ovm-dest.jpg)](https://i0.wp.com/cloudbase.it/wp-content/uploads/2022/04/ovm-dest.jpg?ssl=1)

**Configuration options for OVM as a destination**

```json
[oracle_vm_migration_provider]
 # If migrating/replicating a heterogeneous workload with both Linux and
 # Windows instances, separate template names will need to be provided for the
 # temporary OSMorphing workers for each OS type.
 # The 'linux' image will be used for the disk copy worker during the replica
 # execution process as well
 # Only accepted keys are 'linux' and 'windows'
 migr_template_name_map = linux: OracleLinux7_template, windows: WS2016_template
 # Default migration template guest OS username.
 migr_template_username_map = linux: root, windows: Administrator
 # Default migration template guest OS password.
 migr_template_password_map = linux: S3kre7, windows: M1cr0S3kre7
 # Default server pool name.
 server_pool_name = pool1
 # Default repository name.
 repository_name = repo1
 # virtual_disk_clone_type can be: THIN_CLONE, SPARSE_COPY, NON_SPARSE_COPY
 virtual_disk_clone_type = THIN_CLONE
 # Whether or not to just create VMs but skip powering them on.
 leave_migrated_vm_off = false
 # XEN VM domain type.
 # can be 'XEN_PVM', 'XEN_HVM', 'XEN_HVM_PV_DRIVERS', 'LDOMS_PVM', 'UNKNOWN'
 vm_domain_type = XEN_HVM_PV_DRIVERS
 # virtual_disk_clone_type can be: THIN_CLONE, SPARSE_COPY, NON_SPARSE_COPY
 virtual_disk_clone_type = THIN_CLONE
 windows_pv_drivers_url = https://fileserver-address/win_pv_drivers.zip 
```
  
### OVM destination environment parameters

The destination environment parameters are a set of destination-cloud-specific parameters that offer additional options to the migration/replication process on a per-VM basis.

Below is a listing of the destination environment parameters the OVM plugin supports when migrating/replicating a VM to OVM:

**Example of destination environment JSON to be passed to the OVM plugin**

```json
{
      "network_map": {
          "source network name": "name or ID of existing network on destination OVM",
      },
      "storage_mappings": {
          "default": "default_repository",
          "backend_mappings": [{"source": "datastor1", "destination": "Main"}],
          "disk_mappings": [{"disk_id": "", "destination": "Local"}]
      },
          "server_pool_name": "",
          "repository_name": "",
          "set_dhcp":"",
          "migr_template_name_map": {
          "linux": "OracleLinux7_template",
          "windows": "Windows2012R2_template"
          },
          "migr_template_username_map": { "linux": "root", "windows": "Administrator" },
          "migr_template_password_map": { "linux": "", "windows": "<Administrator password" },
      "leave_migrated_vm_off": false,
          "os_label": "coriolis-migrated",
          "virtual_disk_clone_type": "THIN_CLONE"
  }
   
```
  
Each parameter represents:

  * **network_map** - a mapping between the names of networks on the source cloud and names or of corresponding pre-existing networks on the destination OVM
  * **storage_mappings** - storage-related options such as how to map each disk or storage type on the source to repositories on OVM
  * **server_pool_name** - name of the server pool to create migrated/replicated VMs, as well as temporary worker VMs
  * **repository_name** - name of the storage repository to store migrated/replicated VMs in
  * **set_dhcp** - sets whether or not to configure the migrated VM to use DHCP
  * **migr_template_map** - if migrating/replicating a heterogeneous workload with both Linux and Windows instances, separate template names will need to be provided for the temporary OSMorphing workers for each OS. The only accepted keys are 'Linux' and 'windows'. Please review the "OSMorphing worker images" section for exact details on the requirements of the worker images for each OS type.
  * **migr_template_username_map** - Mapping between OS types and the pre-created usernames of the corresponding template set in the 'migr_template_name_map' to be used for the temporary worker VMs.
  * **migr_template_password_map** - Mapping between OS types and the pre-set password of the corresponding template set in the 'migr_template_name_map' to be used for the temporary worker VMs.
  * **leave_migrated_vm_off** - whether or not to just create VMs but skip powering them on
  * **os_label** - Label for the new OS on OVM
  * **virtual_disk_clone_type** - What cloning method to use when creating migrated disks. The 'Thin Clone' option is recommended, though it may not be supported by all OVM storage repository types.



Most destination environment parameters can also be found in the global configuration section, in which case they may be overridden on a per-migration/replica basis by setting them in the destination environment as well.

### OSMorphing steps taken when migrating/replicating to OVM

Depending on the OS release being migrated/replicated, the following notable steps will be performed as part of the OSMorphing process:

**Linux:**

  * installing cloud-init/OVMd
  * rebuilding initrd on RHEL-based systems



**Windows:**

  * installing the VirtIO drivers
  * installing Cloudbase-init and enabling the Cloudbase-init service


