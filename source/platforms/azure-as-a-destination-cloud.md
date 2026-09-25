---
title: "Azure as a destination cloud"
wp_id: 39531
---

# Azure as a destination cloud

### Migrating (CMaaS) to Azure

Migrations to Azure operate in the same way Replicas do and thus entail the same requirements and steps described below.

### Replicating (DRaaS) to Azure

#### Replica executions:

#### Steps performed by Coriolis

  1. if this is the first replica execution for the VM, create empty disks (configurable to either Managed Disks or blob-storage-based VHDs) on Azure, each matching the specifications of a disk the VM had on the source. If this is a later replica execution, the previously-created disks are used
  2. if this is the first replica execution of the VM, create a new live-snapshot the disks of the VM on the source cloud (handled by whatever source cloud plugin we are using). Is this is a later replica execution, create a new live-snapshot based on the one from the last successful replica execution
  3. create a temporary Linux worker VM on Azure (the "disk copy worker") on Azure and attach the disks from step 1 to it
  4. read the contents of the snapshot created at step 2 via the source platform's snapshot/backup APIs (handled by whatever source cloud plugin we are using), transferring the written chunks to the temporary VM created in step 3, which then writes the chunks at the appropriate index/offset of the disks created at step 1
  5. once the contents of all the disks have been synced to the disks created at step 1, detach the disks and delete the disk copy worker created at step 3

#### Replica deployments:

#### Steps performed by Coriolis

  1. create snapshots of the replicate disks on the destination cloud in order to be able to roll back any changes. By default, new disks are created from these snapshots, leaving the original replica volumes intact for future replica executions. This is an Azure disk snapshot, and not related to the Coriolis option of Clone disk(s)
  2. depending on the OS of the VM whose replica is being deployed, boot a temporary worker VM ("the OSMorphing worker") with the same OS type on the destination cloud, and attach the disks from step 1 to it
  3. perform the "OSMorphing process", where Coriolis commands the OSMorphing worker created at step 2 to scan all attached disks for the OS installation of the VM we are migrating, mount and perform the steps needed to prepare the installation for Azure
  4. detach the disks created at step 1 from the OSMorphing worker created at step 2 and delete the temporary worker VM 
  5. create and boot the migrated VM on Azure with the specifications of the original VM on the source cloud (which have been noted during the particular replica execution we are deploying), creating and attaching any necessary NICs and disks to it

### Azure destination environment parameters

The destination environment parameters are a set of destination-cloud-specific parameters that offer additional options to the migration/replication process on a per-VM basis.

Below is a listing of the destination environment parameters the Azure plugin supports when migrating/replicating a VM to Azure:

#### Example of destination environment JSON to be passed to the Azure plugin

```json
{
     
     "location": "westus",
     "resource_group": "Migrations",
     "network_map":{
         "source network name": "azure-network-name/test-subnet-name"
     },
     "storage_map": {
         "default": "Standard_LRS",
         "backend_mappings": [
             {"source": "source_backend", "destination": "Premium_LRS"}
         ],
         "disk_mappings": [
             {"disk_id": "source_disk_id", "destination": "Premium_SSD"}
         ]
     },
     "vm_size": "Standard_D1",
     
     "worker_size": "Standard_D1",
     "linux_migr_image": {
         "publisher": "Canonical",
         "offer": "UbuntuServer",
         "sku": "16.04.0-LTS",
         "version": "latest"
     },
     "windows_migr_image": {
         "publisher": "MicrosoftWindowsServer",
         "offer": "WindowsServer",
         "sku": "2016-Datacenter-Server-Core",
         "version": "latest"
     },
     
     "storage_account_name": "storage-account",
     "storage_container_name": "coriolis",
     "preserve_nic_ips": false
 }
```

Each parameter represents:

  * **location (string)** - the Azure location to which to migrate/replicate (ex: westus, eastus, etc…)
  * **resource_group (string)** - the name of a pre-existing resource group to which to migrate/replicate and must exist in the specified **location**
  * **network_map (string-string mapping)** - a mapping between the names of networks on the source cloud and a corresponding pre-existing network in the configured **resource_group  **on Azure as well as its subnet name separated by a slash (ex: "testing-network/default" for the "default" subnet of the "testing-network" Azure network) For each NIC of the instance on the source cloud, Coriolis will lookup the mapped network on Azure, and ensure the NIC corresponding to each interface on the source is attached to the right Azure network
  * **storage_map (string-string mapping)** - a mapping between identifiers of storage backends on the source cloud and the corresponding Azure storage account types. For each disk of the instance on the source cloud, Coriolis will lookup the Azure storage account type on Azure
  * **storage_account_name (string)** - Name of the Azure storage account to create VHD Page blobs on
  * **storage_container_name (string)** - Name of the Azure storage container to create VHD Page blobs on
  * **vm_size (string)** - the size of the new VM on Azure, please ensure that the size allows for the number of disks the instance had on the source to be attached to the VM
  * **worker_size (string)** - the size of the temporary replication/OSMorphing workers to use during the migration/replication process
  * **linux_migr_image (object)** - the parameters of a Linux Azure image to use during replication/Linux OSMorphing, default is the 16.04 image exemplified in the listing above
  * **windows_migr_image (object)** - the parameters of a Windows Azure image to use during Windows OSMorphing, default is the Server 2016 image exemplified in the listing above
  * **preserve_nic_ips (boolean)** - Whether or not to set the same IP address on migrated VM NICs if the mapped network/subnet combination includes the IP address(es) the NICs had on the source within their IP range.

Most destination environment parameters can also be found in the global configuration section, in which case they may be overridden on a per-migration/replica basis by setting them in the destination environment as well.

### Configuration Options

Below is a listing of the configuration section needed when migrating/replicating from Azure:

#### Configuration options for Azure as a source

```ini
 [azure_migration_provider]
 # The Azure location to use for any temporary export resources.
 # Under most circumstances, this should be the same as the location of the VM
 # being Migrated/Replicated which should be specified in the source-env.
 export_location = westus
  
 # Default Migration worker VM size. This will be used if no worker_size is set in
 # the source_environment. If none is provided, Coriolis will list all available
 # flavors on Azure and select the smallest available one that can accommodate
 # the number of disks. If not given, Coriolis will select the first worker
 # size available which can accomodate attaching all the disks for the
 # particular VM being migrated/replicated.
 export_worker_size = Standard_D1
  
 # Params of the Azure image to use for the temporary VM:
 export_worker_image = version: latest, publisher: Canonical, offer: UbuntuServer, sku: 18.04-LTS
  
 # For use with AzureStack, the following ARM Provider API versions must be
 # configured to API versions supported by the AzureStack. If unset, they will
 # default to the latest API versions which are supported by the ARM client
 # libraries bundled with Coriolis.
 # export_arm_resource_api_version = 2016-09-01
 # export_arm_compute_api_version = 2016-03-30
 # export_arm_network_api_version = 2015-06-15
 # export_blob_storage_api_version = 2015-04-05 
```

Below is a listing of the configuration section needed when migrating/replicating to Azure:

#### Configuration options for Azure as a destination

```ini
 [azure_migration_provider]
 # The default Azure location to which to migrate. 
 # Can be overridden by the 
 # 'location' --destination-environment parameter.
 # ex: westus, eastus, etc...
 migr_location = westus
  
 # Default migrated instance size. This will be used if no
 # "vm_size" is set in the --destination-environment .
 # Note: migration will fail if migrated instance size cannot 
 # accommodate the number of disks that can be migrated.
 default_vm_size = Standard_A1
  
 # Default migration worker size.This will be used in case no
 # "worker_size" is set in the --destination-environment. If none is "
 # provided, Coriolis will list all available flavors on Azure "
 # and select the smallest available one that can accommodate the number
 # of disks.
 # Note: migration will fail if worker size cannot accommodate "
 # the number of disks that can be migrated."
 default_worker_size = Standard_D1
  
 # Name of the Azure storage account to create
 # VHD Page blobs in (only when using Blob storage)
 storage_account_name = StorageAccountName
  
 # The type of storage backing to use for the disks of VMs migrated to Azure.
 # If set to 'blob_storage', disks will be transferred as VHD Page Blobs inside
 # a pre-existing Blob Storage Account inside the resource group being migrated
 # to. If set to 'managed_disks', disks will be transferred as Managed Disks
 # within the resource group being migrated to. If not set, Coriolis will query
 # the available Compute API versions to determine if Managed Disks are 
 # available (2017-03-30 onwards), else it defaults to using Blob Storage.
 disk_storage_backing_type = managed_disks
  
 # Name of the Azure storage container to create
 # VHD Page blobs in (only when using Blob storage)
 storage_container_name = coriolis
  
 # The parameters of a Linux Azure image to use during disk copy/Linux OSMorphing
 # Default is the 16.04 image exemplified below
 linux_migr_image = publisher: Canonical, offer: UbuntuServer, sku: 16.04.0-LTS, version: latest
  
 # The parameters of a Windows Azure image to use during Windows OSMorphing
 # Default is the Server 2016 image exemplified below
 windows_migr_image = publisher: MicrosoftWindowsServer, offer: WindowsServer, sku: 2016-Datacenter-Server-Core, version: latest
  
 # Whether or not to set any IP addresses read from source VM NIC configurations
 # to destination NICs on Azure. This requires that the network/subnet mappings
 # in the 'network_map' are to networks/subnets on Azure which include the range
 # of the source networks. Default is true
 preserve_nic_ips = true
  
 # For use with AzureStack, the following ARM Provider API versions must be
 # configured to API versions supported by the AzureStack. If unset, they will
 # default to the latest API versions which are supported by the ARM client
 # libraries bundled with Coriolis.
 # arm_resource_api_version = 2016-09-01
 # arm_compute_api_version = 2016-03-30
 # arm_network_api_version = 2015-06-15
 # blob_storage_api_version = 2015-04-05
 # arm_storage_api_version = 2018-07-01
  
 # The URLs to .zip releases of Cloudbase-init for each supported architecture
 # The default values are for the official upstream releases available on cloudbase.it
 cloudbaseinit_x64_url = https://www.cloudbase.it/downloads/CloudbaseInitSetup_x64.zip
 cloudbaseinit_x86_url = https://www.cloudbase.it/downloads/CloudbaseInitSetup_x86.zip 
```

#### Coriolis Advanced options for Target Destinations

In the case of Replicating/Migration to Azure, Worker images have the following requirements: 

  * **Linux image requirements**

The Linux image should have the walinuxagent installed and configured for the first boot. Coriolis will create a unique key pair for each migration/replication and add it as authorized via metadata. 

  * **Windows image requirements**

The Windows image should have the Azure provisioning agent or cloudbase-init installed and configured for the first boot. Coriolis will create a unique password for each migration deployment and use it to set up WinRM access via a VM extension. 

The template OS version must be at least the same as the OS of the VM that needs to be Replicated or Migrated. 

[![](_static/images/azure-target-options.png)](https://i0.wp.com/cloudbase.it/wp-content/uploads/2020/04/image-2.png?ssl=1)

**Option name (UI)**  | **Parameter**  | **Description**    
---|---|---  
Location | location | the Azure location to which to migrate/replicate (ex: westus, eastus, etc…)   

Resource Group | resource_group | the name of a pre-existing resource group in which to migrate/replicate to, must exist in the specified location   
Storage account name | storage_account_name | name of the Azure storage account to create VHD Page blobs on   
Storage container name | storage_container_name| name of the Azure storage container to create VHD Page blobs on   
VM Size | vm_size | the size of the new VM on Azure, please ensure that the size allows for the number of disks the instance had on the source to be attached to the VM   
Worker Size | worker_size | the size of the temporary replication/OSMorphing workers to use during the migration/replication process   
Linux Migration image | linux_migr_image | the parameters of a Linux Azure image to use during replication/Linux OSMorphing, default is the 16.04 image exemplified in the listing above   
Windows Migration image | windows_migr_image | the parameters of a Windows Azure image to use during Windows OSMorphing, default is the Server 2016 image exemplified in the listing above   
Preserve NIC IPs | preserve_nic_ips | whether to set the same IP addresses on migrated VM NICs if the mapped network/subnet combination includes the IP address(es) the NICs had on the source within their IP range   

### OSMorphing steps taken when migrating/replicating to Azure

The OSMorphing process for Azure mandatorily consists of setting all interfaces on the migrated/replicated VM to use DHCP on boot, as one cannot specify the desired MAC address for a NIC upon its creation, nor can we know what MAC address Azure will assign to the NIC utils the NIC is attached to the final VM

The following other notable steps will be performed as part of the OSMorphing process:

#### Linux

  * installing the walinuxagent for supported guest OS releases
  * installing Hyper-V integration tools
  * installing the appropriate LTS Hardware Enablement (HWE) stack on Ubuntu and derivatives 
  * rebuilding initrd on RHEL-based systems
  * other distribution-related steps recommended by the Azure team and available [here](https://docs.microsoft.com/en-us/azure/virtual-machines/linux/classic/create-upload-vhd).

#### Windows

  * installing Cloudbase-init and enabling the Cloudbase-init service

### OSMorphing worker images

During the OSMorphing process, Coriolis will create a temporary VM to scan the Azure disk volumes it has just migrated/replicated for the OS installation of the VM it is migrating and perform the necessary changes to ensure it will boot correctly on Azure. Because the OSMorphing process is OS-specific, Coriolis will need to be configured with the parameters of two Azure images (one Linux, another one Windows) to boot the temporary OSMorphing workers.

The images do **NOT** require any special Coriolis agent running in them and can be images already available in Azure, granted the following requirements:

**Linux** : the Linux image should have the **walinuxagent**  installed and configured for first boot. Coriolis will create a unique key pair for each migration/replication and add it as authorized via metadata.

**Windows** : the Windows image should have the Azure provisioning agent OR cloudbase-init installed and configured for the first boot. Coriolis will create a unique password for each migration deployment and use it to set up WinRM access via a VM extension.

For more information regarding the Coriolis Worker template, please check the **[Coriolis Temporary Migration Worker](https://cloudbase.it/coriolis-temporary-migration-worker) **page.
