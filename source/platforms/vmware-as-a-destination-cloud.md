---
title: "VMware as a destination cloud"
wp_id: 39837
---

# VMware as a destination cloud

### Migrating (CMaaS) to VMWare vSphere

Migrations to VMWare vSphere operate in the same way Replicas do and thus entail the same requirements and steps described below.

### Replicating (DRaaS) to VMWare vSphere

#### Requirements:

In order to **Replicate** to VMWare vSphere, **VM templates** for temporary Coriolis workers are required.

  
The templates need the following:

#### Linux

  * **Ubuntu Server 18.04/20.04** (recommended) 
  * **sudo** must be configured to work as **passwordless**
  * Must **disable security/unattended** updates on Ubuntu as those will **conflict with Coriolis**
  * **Template VM config** must have a **SCSI** controller bus attached
  * **VMware tools** need to be installed
  * Configuration to a **network** with a **DHCP server** , which Coriolis can reach



#### Windows

  * OS used for the image must be the same version or newer than the VM to be **replicated/migrated**
  * **VMWare tools** need to be installed
  * Configuration to a **network** with a **DHCP server** , a network which Coriolis can reach
  * **Template VM config** must have a **SCSI** controller bus attached
  * for more information regarding Coriolis' Worker template, please check the **[Coriolis Temporary Migration Worker](https://cloudbase.it/coriolis-temporary-migration-worker) **page.



#### Replica executions

#### Steps performed by Coriolis

  1. if this is the first replica execution for the VM, create an empty volume disk on the destination cloud, each matching the specifications of a disk the VM had on the source.  
If this is a later replica execution, the previously created volume disks are used
  2. if this is the first replica execution of the VM, create a new live snapshot of the disks of the VM on the source cloud (handled by whatever source cloud plugin we are using).  
If this is a later replica execution, create a new live snapshot based on the one from the last successful replica execution
  3. create a temporary Linux worker VM on VMWare vSphere (the "disk copy worker") on the destination cloud and attach the disk volumes from Step 1 to it
  4. read the contents of the snapshot created at step 2 via the source platform's snapshot/backup APIs (handled by whatever source cloud plugin we are using), transferring the written chunks to the temporary VM created in step 3, which then writes the chunks at the appropriate index/offset of the disks made at Step 1
  5. once the contents of all the disks have been synced to the volumes created in Step 1, detach the volumes and delete the disk copy worker made in Step 3



#### Replica deployments

#### Steps performed by Coriolis

  1. create snapshots of the replicated volumes on the destination cloud in order to be able to roll back any changes. By default, new volumes are made from these snapshots, leaving the original replica volumes intact for future replica executions
  2. depending on the OS of the VM whose replica is being deployed, boot a temporary worker VM ("the OSMorphing worker") with the same OS type on the destination cloud, and attach the Cinder volumes from step 1 to it
  3. perform the "OSMorphing process", where Coriolis commands the OSMorphing worker created at step 2 to scan all attached disks for the OS installation of the VM we are migrating, mount, and perform the steps needed to prepare the installation for the new platform (ex: uninstalling the VirtIO drivers and installing VMWare drivers if deploying a replica of a Windows VM from OpenStack to VMWare vSphere)
  4. detach the volumes created at step 1 from the OSMorphing worker created at step 2 and delete the temporary worker VM 
  5. create and boot the migrated VM on the destination cloud with the specifications of the original VM on the source cloud (which have been noted during the particular replica execution we are deploying), and attach the volumes.



### Configuration Options

#### Advanced Target options for VMWare target destination

In the case of Replicating or Migrating to VMWare vSphere, there will need to be images that the worker will use to create temporary VMs in order to perform the tasks, for both Linux and Windows machines. 

The template OS version must be at least the same as the OS of the VM that needs to be Replicated or Migrated. 

**[![](_static/images/vmware-target.jpg)](https://i0.wp.com/cloudbase.it/wp-content/uploads/2022/11/vmware-target.jpg?ssl=1)**

### Required permissions in vCenter

For role isolation purposes, we highly recommend creating a new service role in vCenter. This role will then be assigned to a new service user that will be used in Coriolis.

When having **VMware as a destination platform** , the role of the user account given to Coriolis must have the following privileges:

**Object** | **Required on** | **Required Privilege** | **Motivation/observation**  
---|---|---|---  
**Datacenter** | The datacenter object(s) to be migrated to | Read-only | Listing target VMWare datacenters; accessing datacenter resources (clusters, datastores, etc.)  
**Cluster** | The cluster object(s) to be migrated to | Read-only | Listing target VMWare clusters and accessing cluster hosts  
**Datastore** | The datastore object(s) to be migrated to | Browse Datastore | Browsing datastore files for VM folders, replica disks, etc.  
Low level file operations | Creating/Cloning/Removing replica disk files.  
Allocate Space | Allocating disk space when creating worker VM  
**Network** | The host object(s) to be migrated to | Assign network | Assign network to the NICs of the migrated VM  
**Virtual Machine** | The host object(s) to be migrated to | Edit Inventory -> Create From Existing | Creating worker VM from existing template  
Edit Inventory -> Remove | Deleting worker VM  
Provisioning -> Deploy Template | Deploying worker VM from existing template  
Interaction -> Power on | Starting worker and final VMs  
Interaction -> Power off | Stopping worker VMs  
Change configuration -> Add existing disk | Attaching replica disks to worker VMs; attaching disks to final VMs  
Change configuration -> Remove disk | Removing replica disks from worker VMs  
Change configuration -> Add or remove device | Adding required buses, migrated NICs and disk devices to migrated VM  
Edit Inventory -> Create new | Creating final VM  
**Resource** | The host object(s) to be migrated to | Assign virtual machine to resource pool | Assigning created worker or final VM to a resource pool  
  
#### Configuration options for VMWare vSphere as a destination

  * **Title** = The name that will be listed in Coriolis' Dashboard. The default will be the name of the machine on the source platform
  * **Execute Now** = Whether or not the Replica/Migration will be executed at the end of its configuration. Default is set to true
  * **Execute Now Options** = Whether or not to power off the Instance/s before the Replica/Migration execution starts. Default is set to false
  * **Import Datacenter** = The name of the datacenter to import to
  * **Import Datastore** = The inventory path of the VMware datastore from the selected 'import datacenter' in which to create Migrated VMs
  * **Import Cluster** = The inventory path of the compute cluster
  * **Import Resource Pool** = The name of the resource pool to deploy the migrated VMs in. Must reside within the selected 'import cluster'
  * **Import VM Folder** = Inventory path of a pre-existing VM folder on the selected 'Import Datacenter' in which to put the migrated VMs
  * **Power On Migrated Machines** = Whether or not Coriolis should power on machines after migrating them
  * **Import Enable CBT** = Whether or not Coriolis attempts to enable CBT on migrated VMs
  * **Imported VM Guest ID** = The VMware guest ID for the VMs to be migrated to VMware.
  * **Preserve MAC Addresses** = Whether or not Coriolis should preserve the MAC addresses of the network interfaces of the migrated VMs
  * **NICs Device Model** = The network interface device model to use for migrated virtual machines.
  * **Imported VM Hardware Version** = The VMware hardware version for the migrated VMs
  * **Set DHCP** = Whether or not Coriolis should reconfigure the Migrated VMs to use DHCP on all network interfaces during the OSMorphing process.
  * **Windows Drivers ZIP URL** = URL for the ZIP file containing the VMware Tools data and drivers to be injected within instances during OSMorphing stage.
  * **Use First Class Disks** = Whether or not Coriolis should create virtual disks as First Class Disks.
  * **Migration Minion Folder** = Inventory path of the VM folder on the selected 'import datacenter' in which to house temporary minion VMs, excluding the top-level datacenter 
  * **Migration Template Map** = Mapping between operating system types and the inventory paths of pre-existing VM templates available on VMware
  * **Migration Disk Shell Template** = Inventory path of an empty VM template to be used as a proxy for disk operations. The template's only requirement is having a SCSI controller bus 
  * **Migration Template Username Map** = Mapping between operating system types and the names of pre-existing usernames on the template(s) specified in the 'migration template map' option
  * **Migration Template Password Map** = Mapping between operating system types and the passwords of pre-existing usernames on the template(s)
  * **Migration Minion Datastore** = The inventory path of the VMware datastore from the selected 'import datacenter' in which to store temporary minion VMs
  * **Migration Minion Cluster** = The inventory path of the compute cluster from the selected 'import datacenter' in which temporary minion VMs should be created
  * **Migration Minion Resource Pool** = The name of the resource pool in which temporary minion VMs should be created on 



#### Using the First Class Disks option

When using the option for **First Class Disks** , Coriolis will require that the vCenter version **be at least 6.7 or newer**. Coriolis is able to use First Class Disk if the **Hosts are running on an earlier version** , but the **mandatory** version of **vCenter is 6.7 or newer**.

In the situation of creating a **Replica Deployment** using an existing **Replica Execution** , Coriolis will **support** the option of **Cloning Replica Disks** only if **First Class Disks** are used.

### OSMorphing steps taken when migrating/replicating to VMWare vSphere

#### Linux

  * install the VMWare drivers



#### Windows

  * install the VMWare drivers 
    * required tools and drivers. Instructions are found on the **[OS Morphing tools and drivers](https://cloudbase.it/vmware-tools-and-drivers-for-osmorphing)** page.



**NOTE:** During the OSMorphing process, Coriolis will install only the drivers from the **VMware Tools ZIP file**. For full integration of the guest instance with the VMware platform, the user should install the VMware Tools after the instance migration is complete. Refer to the following VMware KB article for more details: [How to install VMware Tools (1014294)](https://kb.vmware.com/s/article/1014294)
