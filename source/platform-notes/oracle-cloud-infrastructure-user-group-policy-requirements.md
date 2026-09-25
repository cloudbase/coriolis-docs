---
title: "OCI policy requirements for Coriolis"
wp_id: 39029
---

# OCI policy requirements for Coriolis

## Oracle Cloud Infrastructure user/group policy requirements

Coriolis allows users to choose two compartments when migrating to OCI: the main compartment where the Migrated/Replicated VMs' resources will be created, as well as a VCN compartment from which the user can choose the VCNs the migrated VM(s) should connect to.

This results in the necessity of setting appropriate permissions for the OCI user/group Coriolis is using for each chosen compartment.

If the user chooses the same compartment for both options, all permissions should be set for the said compartment. Additional permission might be required based on new OCI features or migration-specific features.

The tables below describe the minimum required permissions for each compartment:

| | **Main Compartment**  
---|---|---  
Action (Verb)| OCI Resource Type| Required for  
inspect| compartments| Listing main and VCN compartment options.  
manage| instance-images| Listing and using official and custom images, but also creating the all-zero images, in case they are not available in the OCI region.  
manage| instances| Creating and terminating temporary minion machines that handle disk transfers, as well as creating the final Migrated VM.  
manage| volumes| Creating, cloning, and deleting transferred VM volumes.  
inspect| vnic-attachments| Checking minion machines' IP addresses, as well as attaching existing security groups to VMs.  
manage| volume-attachments| Attaching and detaching volumes to the temporary minion machines performing the transfer, as well as the final Migrated VMs.  
manage| boot-volume-backups| Creating and deleting Replica boot volume backups when cloning Replica boot volumes.  
manage| volume-backups| Creating and deleting volume backups for each Replica data disk when cloning Replica disks.  
manage| buckets| Creating the bucket in which to store the all-zero qcow image.  
manage| objects| Uploading the all-zero qcow image to the bucket.  
manage| objectstorage-namespaces| Getting object storage namespace of a compartment.  
use| dedicated-vm-hosts| Listing and creating final VMs inside the selected dedicated VM host.  
| |   
| | **VCN Compartment**  
Action (Verb)| OCI Resource Type| Required for  
manage| vcns| Listing VCNs and creating Network Security Groups for minion machines.  
use | subnets| Listing subnets, creating and terminating temporary minion machines, creating and deleting Network Security Groups for the minion machines, creating migrated VMs, and attaching secondary VNICs to migrated VMs.  
manage| network-security-groups| Creating and deleting Network Security Groups and adding them to the temporary minion machines, as well as to the final Migrated VMs.  
use| vnics| Creating and deleting minion machines, creating and deleting Network Security Groups for the minion machines, creating migrated VMs, and attaching secondary VNICs to Migrated VMs.
