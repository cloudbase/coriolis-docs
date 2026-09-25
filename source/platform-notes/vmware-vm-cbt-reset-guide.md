---
title: "VMware VM CBT reset guide"
wp_id: 41525
---

# VMware VM CBT reset guide

The following guide will provide information on resetting CBT for VMs that cannot perform backups using VMware CBT. VMware provides more info on the matter on its documentation page **[here](https://kb.vmware.com/s/article/1020128)**.

Changed Block Tracking (CBT) is a VMkernel feature that keeps track of the storage blocks of virtual machines as they change over time. The VMkernel keeps track of block changes on virtual machines, which enhances the backup process for applications developed to take advantage of VMware’s vStorage APIs.

CBT needs to be reset once the backups can no longer be performed, as the task will fail:

  * The reference error will be 
    * **One or more VM disks have incorrect changed block tracking configuration.**
  * Secondly, the backup job will show a similar error
    * **Disk "Hard disk #" has an incorrect changed block tracking configuration.**
    * **One or more VM disks have incorrect changed block tracking configuration.**

### Resetting CBT

To reset CBT on a vSphere virtual machine:

  1. Open the vSphere Web Client.

![](_static/images/login.jpg)

2\. Right-click the virtual machine and click **Power Off**.

3\. Right-click the virtual machine, click the **Snapshot** and navigate to Snapshot Manager. Ensure there are no active snapshots. If there are snapshots present, consolidate them to commit the changes. For more information, see [Consolidating/Committing snapshots in ESXi (1002310)](https://kb.vmware.com/s/article/1002310)

![](_static/images/manage-snap.jpg)

4\. Right-click the virtual machine and click **Edit Settings**.

![](_static/images/edit-settings.jpg)

5\. Click the **Options** tab, select the **Advanced  **section and then click **Edit Configuration Parameters**.

![](_static/images/advanced-set.jpg)

6\. Disable CBT for the virtual machine by setting the **ctkEnabled** value to **false**.

![](_static/images/cbt-false.jpg)

7\. Disable CBT for the individual virtual disks attached to the virtual machine by setting the **scsix:x.ctkEnabled** value for each attached virtual disk to **false**.

![](_static/images/scsi-false.jpg)

**NOTE:** Where **scsix:x** is the SCSI controller and SCSI device ID of your virtual disk.

8\. Open the virtual machine's working directory using the Datastore Browser or ESXi shell. For more information on identifying the working directory, see [Locating virtual machine log files on an ESXi/ESX host (1007805)](https://kb.vmware.com/s/article/1007805).

![](_static/images/vmwarestorage.png)

9\. Ensure no snapshot files (.delta.vmdk) are present in the virtual machine's working directory. For more information, see [Determining if there are leftover delta files or snapshots that VMware vSphere or Infrastructure Client cannot detect (1005049)](https://kb.vmware.com/s/article/1005049).

10\. Delete any -CTK.VMDK files within the virtual machine's working directory.

11\. In the vSphere Client, right-click the virtual machine and click **Power On**.

12\. Before you will run the **Coriolis Replica/Migration** task with the help of **CBT** , you must re-enable CBT manually or allow**Coriolis** to enable CBT when selecting **VMware** as a source. Some backup tools automatically enable CBT, For more information, see [Enabling or disabling Changed Block Tracking (CBT) on virtual machines (1031873)](https://kb.vmware.com/s/article/1031873).

### Reset CBT for multiple VMs using PowerCLI script

This process can be performed using a script provided by VMware alongside the instructions on their documentation page **[here](https://kb.vmware.com/s/article/2139574)**.
