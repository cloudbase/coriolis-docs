---
title: "Proxmox as a destination cloud"
wp_id: 42900
---

# Proxmox as a destination cloud

### Migrating (CMaaS) to Proxmox
Migrations to Proxmox VE operate in the same way Replicas do and thus entail the same requirements and steps described below.

### Replicating (DRaaS) to Proxmox

![](_static/images/proxmox-target.png)

#### Requirements:

To **Replicate** to Proxmox VE, **VM templates** for temporary Coriolis workers are required. The templates need the following platform specifics in addition to **[Coriolis Temporary Migration Worker](https://cloudbase.it/coriolis-temporary-migration-worker)**.

In the case of Replicating or Migrating to Proxmox VE, images will need to be created for both Linux and Windows machines for the worker to create temporary VMs to perform the tasks. The template OS version must be at least the same as the VM OS that needs to be migrated.

**NOTE!** When Replicating/Migrating a **Windows VM** , both **Linux and Windows templates**  have to be specified, as **Disk cloning**  is performed using the Linux template and **OSMorphing**  is performed using the Windows template.

#### Linux

  * **Ubuntu Server 22.04** LTS (recommended) or higher


  * **sudo** must be configured to work **passwordless**


  * Must **disable security/unattended** updates on Ubuntu as those will **conflict with Coriolis**


  * **Template VM config** must have a **SCSI** controller bus attached


  * **Qemu-guest-agent** must be installed



```bash
apt update && apt -y install qemu-guest-agent
systemctl enable qemu-guest-agent
systemctl start qemu-guest-agent
systemctl status qemu-guest-agent
```

  * Configuration to a **network** with a **DHCP server** , a network which the Coriolis appliance can reach.



#### Windows

  * OS used for the image must be the same version or newer than the VM to be **replicated/migrated**
    * example: when migrating a Windows Server 2019 VM, the temporary worker image must be at least WS2019 or newer.


  * **VirtIO drivers** and **Qemu-guest-agent** need to be installed 
    * Qemu-guest-agent is included in VirtIO drivers: 
      * Start the virtual machine and connect to a graphical console.
      * Log in to a Windows user session.
      * Open **Device Manager** and expand **Other devices** to list any **Unknown device**.
      * Open the Device Properties to identify the unknown device. Right-click the device and select **Properties**.
      * Click the **Details** tab and select **Hardware IDs** in the **Property** list.
      * Compare the **Value** for the **Hardware IDs** with the supported VirtIO drivers.
      * Right-click the device and select **Update Driver Software**.
      * Click **Browse my computer for driver software** and browse to the attached SATA CD drive, where the VirtIO drivers are located. The drivers are arranged hierarchically according to their driver type, operating system, and CPU architecture.
      * Click **Next** to install the driver.
      * Repeat this process for all the necessary VirtIO drivers.
      * After the driver installs, click **Close** to close the window.
      * Reboot the virtual machine to complete the driver installation


  * Configuration to a **network** with a **DHCP server** , a network which Coriolis can reach


  * **Template VM config** must have an **SCSI** controller bus attached


  * for more information regarding Coriolis’ Worker template, please check the **[Coriolis Temporary Migration Worker](https://cloudbase.it/coriolis-temporary-migration-worker) **page.



#### User Role requirements

When using Coriolis to migrate to Proxmox, a Proxmox user with the following roles need to be used (these roles exist on any Proxmox deployment by default):

**Role Name**| **Usage**  
---|---  
PVEDatastoreAdmin| Coriolis creates, manages, clones, deletes transferred volumes on destination Proxmox datastores  
PVEVMAdmin| Coriolis creates, deletes, edits, clones worker or migrated VMs on the destination Proxmox  
PVESDNUser| Coriolis may use SDN networks when creating worker or migratied VMs (depending on how you configure the migrations)  

#### Replica executions:

#### Steps performed by Coriolis

  1. if this is the first replica execution for the VM, create empty volumes on the destination cloud, each matching the specifications of a disk the VM had on the source. If this is a later replica execution, the previously created volumes are used
  2. if this is the first replica execution of the VM, create a new live snapshot of the disks of the VM on the source cloud (handled by whatever source cloud plugin we are using). If this is a later replica execution, create a new live snapshot based on the one from the last successful replica execution
  3. create a temporary Linux worker VM in Proxmox VE (the "disk copy worker") on the destination cloud and attach the volumes from Step 1 to it
  4. read the contents of the snapshot created at step 2 via the source platform's snapshot/backup APIs (handled by whatever source cloud plugin we are using), transferring the written chunks to the temporary VM created in step 3, which then writes the chunks at the appropriate index/offset of the disks created at step 1
  5. once the contents of all the disks have been synced to the volumes created in Step 1, detach the volumes and delete the disk copy worker created in Step 3



#### Replica deployments:

#### Steps performed by Coriolis

  1. create snapshots of the replicated volumes on the destination cloud in order to be able to roll back any changes. By default, new volumes are created from these snapshots, leaving the original replica volumes intact for future replica executions
  2. depending on the OS of the VM whose replica is being deployed, boot a temporary worker VM ("the OSMorphing worker") with the same OS type on the destination cloud, and attach the volumes from step 1 to it
  3. perform the "OSMorphing process", where Coriolis commands the OSMorphing worker created in step 2 to scan all attached disks for the OS installation of the VM we are migrating, mount, and perform the steps needed to prepare the installation for the new platform (ex: uninstalling the VMWare guest tools and installing VirtIO drivers if deploying a replica of a Windows VM from vSphere to Proxmox)
  4. detach the volumes created at step 1 from the OSMorphing worker created at step 2 and delete the temporary worker VM 
  5. create and boot the migrated VM on the destination cloud with the specifications of the original VM on the source cloud (which have been noted during the particular replica execution we are deploying), creating and attaching any necessary network ports and volumes.



### OSMorphing steps taken when migrating to Proxmox VE

Depending on the OS release being migrated/replicated, the following notable steps will be performed as part of the OSMorphing process:

#### Linux

  * install guest agent (ovirt-guest-agent or qemu-guest-agent)



#### Windows

  * install the VirtIO drivers
  * install the QEMU guest agent
  * install cloudbase-init for guest OS provisioning and configuration



### Configuration Options

#### Configuration options for Proxmox VE as a destination

  * **Title** = The name that will be listed in Coriolis’ Dashboard. The default will be the name of the machine on the source platform
  * **Skip OS Morphing** = Whether or not to skip the OS Morphing process (installing platform-specific drivers)
  * **Shutdown Instances** = Whether or not to shutdown the source instance before performing the last incremental sync
  * **Replication Count** = The number of times to run incremental syncs
  * **Import Node** = The name of the Proxmox node to import the VM to
  * **Cloud-init New Authorized SSH Keys** = SSH public keys to be set by Cloud-init userdata
  * **Cloud-init New Username** = New username to be set via Cloud-init userdata
  * **Migrated Disks Device Model** = The device model to be used for disk attachments for the migrated VM (default is set to VirtIO)
  * **Migrated Network Interfaces Device Model** = The network interface device model to be used for disk attachments for the migrated VM (default is set to virtio)
  * **Preserve Migrated VM MAC Addresses** = Whether or not Coriolis should preserve the MAC address of the network interfaces for the migrated VM
  * **Set DHCP** = Whether or not to configure the VM to use DHCP during the OS Morphing process (default is set to true)
  * **Cloudbase Init ZIP URL** = URL of the .ZIP file containing Cloudbase-init used for migrating Windows VM (HTTP/HTTPS URLs only) - note that Cloudbase-init releases are CPU architecture specific
  * **Cloud-init New Password** = New password to set via Cloud-init userdata (only working for Linux Distributions)
  * **CPU Model** = Default virtual CPU model to be used for migrated VM (default is set to 'x86-x64-v2-AES' )
  * **Linux Template** = The name of the Ubuntu 22.04 Linux Template on the provided Proxmox 'Import-node' (must have 'Cloud-init' and 'Qemu-guest-agent' installed already )
  * **Windows Template** = The name of the Windows template on the provided Proxmox 'Import-node' (must have 'WinRM/HTTPS' enabled and 'Qemu-guest-agent' installed already ) - note template version must be the same version or newer than the migrated VM
  * **Enable Firewall** = Whether or not to configure the cluster-wide Proxmox firewall configuration for the migrated VM
  * **Retain User Credentials** = Whether or not Coriolis reconfigure the Cloud-init during the OS Morphing process to set a new user/remove root account
  * **Skip Starting Migrated VMs** = Whether or not to skip starting the migrated VM once the Migration is complete
  * **Windows VirtIO Drivers ISO URL** = URL to a .ISO containing the Windows VirtIO drivers


