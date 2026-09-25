---
title: "OVM as a source cloud"
wp_id: 39511
---

# OVM as a source cloud

**Coriolis ' OVM plugin supports both migrating (CMaaS) and replicating (DRaaS) from OVM.**

### Migrating (CMaaS) from OVM

Migrations to OVM operate in the same way Replicas do and thus entail the same requirements and steps described below.

### Replicating (DRaaS) from OVM

**Input** : the names of the instances.

#### Steps performed by Coriolis

Considering that in OCI there are no publicly available APIs for fetching the contents of disks of instances off of OVM, the OVM Coriolis plugin must bypass the issue by booting a temporary machine to Replicate the contents of the disks through.

  1. Read the instance configuration on the source OVM (CPU, RAM, disks, etc…)
  2. create snapshots of all the volumes of the instance
  3. create a temporary instance on OVM (the "disk replication worker") and attach the volumes based on the snapshots created during step 2
  4. scan the disks of the VM being Replicated for written disk areas
  5. if this is the first Replica execution, transfer over all of the allocated disk chunks. If this is an incremental Replica execution, only transfer over the disk chunks which have changed since the last execution
  6. once the transfer of all disks is complete, delete the worker created at step 3 and its attached disks
  7. remove the volume snapshots created at step 2, along with any other temporary resources used in the disk copy process (such as the key pair for the disk copy worker)

During step 5, the data chunks will be handed directly to the destination cloud plugin, which will ensure they are written to the Replica disks on the destination.

### Configuration Options

![](_static/images/ovm-source.jpg)

#### Configuration options for OVM as a migration source

```ini
[oracle_vm_migration_provider]
 # Name of the repository to create the temporary disk Replication VM in.
 repository_name = repo1

 # For export we may need to use a different template than the linux one
 # specified in the template map. We specify that here
 export_template_name = OracleLinux7_template

 # Credentials for the export template
 export_template_username = root
 export_template_password = Passw0rd

 # What cloning method to use when cloning the source disks to be migrated. 
 # The 'Thin Clone' option is recommended, though it may not be supported by 
 # all OVM storage repository types.
 virtual_disk_clone_type = "THIN_CLONE" 
```

The **export_template_name** parameter which is used for the **temporary worker** must use an Oracle Linux VM (**recommended version 7.x or newer**) for the template.

Please ensure that the Oracle VM Guest Additions Daemon, **ovmd** , is installed on the guest OS that will be used as the template. This will allow Coriolis to fetch the IP address of the temporary worker once it is spawned. Refer to the Oracle VM documentation for the required steps.

NOTE! you must ensure that the OS type property is correctly set for the Template in OVM, that being setting the corresponding Oracle Linux distribution and the release for it.

### OVM source environment parameters

The source environment parameters are a set of source-cloud-specific parameters that expose additional options to the migration/replication process on a per-VM basis.

Below is a listing of the source environment parameters the OVM plugin supports when migrating/replicating a VM from OVM:

#### Example of source environment JSON to be passed to the OVM plugin

```json
 {
          "repository_name": "",
          "export_template_name": "",
          "export_template_username": "",
          "export_template_password": "",
          "virtual_disk_clone_types": "THIN_CLONE"
  }
    
```

Each parameter represents:

  * **repository_name (string)** - name of the repository to create temporary worker VMs in
  * **export_template_name(string)** - name of Linux template to use for the temporary disk export VMs. The template must be configured with a NIC attached to a network that is both reachable from the Coriolis installation and has a DHCP server available to allocate a new IP to the temporary VM.
  * **export_template_username (string)** - username for the temporary VM template
  * **export_template_password (string)** - password for the temporary VM template
  * **virtual_disk_clone_type (string)** - What cloning method to use when cloning the source disks to be migrated. The 'Thin Clone' option is recommended, though it may not be supported by all OVM storage repository types.

Most destination environment parameters can also be found in the global configuration section. These may be overridden on a per-migration/replica basis by setting them in the destination environment.

NOTE! In case a DHCP server is not available in the network, a static IP can be set on the VM template, though it will limit the use of that respective VM template to a single Migration/Replica execution at a time. Multiple VM templates for different Migration or Replica tasks can be configured otherwise.

### OSMorphing steps taken when migrating from OVM

For OVM guests, Coriolis will take the following OSMorphing steps as part of the migration process from OVM:

#### Linux

  * uninstalling OVMd (if applicable)

#### Windows

  * removing Windows PV drivers
