---
title: "Azure as a source cloud"
wp_id: 39529
---

# Azure as a source cloud

### Migrating (CMaaS) from Azure

Migrations from Azure operate in the same way Replicas do and thus entail the same requirements and steps described below.

### Replicating (DRaaS) from Azure

#### Inputs

  * some parameters related to the ARM environment to aid in locating the VM (example: location, resource group name, etc…)
  * the name of the VM on Azure



Please consider reviewing the general steps recommended to be performed before creating migration for an instance from Azure [here](https://cloudbase.it/preparing-a-vm-for-migration-replication/).

#### Steps performed by Coriolis

Considering there are no publicly-available APIs for fetching the contents of disks of instances off of Azure, the Azure Coriolis plugin must bypass the issue by booting a temporary machine to read the contents of the disks through.

  1. read the configuration of the instance on the source Azure (VM size, disk specifications, etc…)
  2. [optional] if the instance is running, shut down the instance via Azure API
  3. create snapshots of all the disks of the instance and create new disks from them
  4. create a temporary instance on Azure (the "disk replication worker") and attach the volumes created in step 3
  5. compute the state of the disks (i.e. hash the disk chunks)
  6. if this is the first Replica execution, read all non-zero disk chunks and pass them to the destination plugin  
If this is incremental sync, only the chunks which have changed from the previous Replica execution are transferred.
  7. delete the temporary replication created at step 4 and its attached disks
  8. remove the volume snapshots created at step 3, along with any other temporary resources used in the disk copy process (such as the NIC or public IP)



During step 6, the changed blocks are transferred and written to disks on the destination platform via the destination cloud plugin.

#### Example of source environment JSON to be passed to the Azure plugin

```json
{
     "location": "westus",
     "resource_group": "coriolis-testgroup",
     "export_worker_size": "Standard_A1",
     "export_worker_image": {
         "publisher": "Canonical",
         "offer": "UbuntuServer",
         "sku": "16.04.0-LTS",
         "version": "latest"},
     // Below options are for Blob storage-based scenarios:
     "storage_account_name": "storage-account",
     "storage_container_name": "coriolis"
 }
```
  
Each parameter representing:

  * **location (string)** - the Azure location where to search for the VM to migrate/replicate (ex: westus, eastus, etc…)
  * **resource_group (string)** - the name of the resource group in which the VMs to migrate/replicate are in
  * **export_worker_size (string)** - the size to use for the temporary disk replication worker VM
  * **export_worker_image (object)** - the parameters of the image to use for the temporary worker VM
  * **storage_account_name (string)** - If configured to Migrate/Replicate to Blob storage, the name of an Azure Blob storage account must be provided. The Storage account must reside within the selected 'Resource Group'
  * **storage_container_name (string)** - If configured to Migrate/Replicate to Blob storage, the name of an Azure storage container must be provided. The container must reside within the Azure storage account provided using 'Storage Account Name'. The container will be automatically created during the Migration/Replication process if it doesn't exist.


