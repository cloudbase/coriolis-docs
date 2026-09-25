---
title: "Snapshot Agent for Bare Metal Servers prerequisites"
wp_id: 42200
---

# Snapshot Agent for Bare Metal Servers prerequisites

### Storage prerequisites

Before installing the snapshot agent on the machines, make sure you either have an extra empty disk attached to the machine or have an empty iSCSI target connected, having at least **the same size as the disks of the machine itself**.

Coriolis Snapshot Agent **requires an extra disk device attached** to the server, where it can store the created snapshots. The **extra disk** device can be either a **physical** disk, a **removable** disk, or an **iSCSI** attached disk. The size of this extra disk should be at least the same as the total storage capacity of the server.

Before starting to install the **Snapshot Agent** , the **extra disk** must be **formatted and mounted**.

**The minimum size** of the **extra disk** must be **at least the size of the largest disk** available on the Bare Metal Server.

The file system for the snapstore disk must support a Linux-specific system call named fallocate (zero range), which is available on the following file systems:

  * ext4
  * xfs
  * btrfs 

Snapstore destination is an array of paths on the disk where the snap store watchers will allocate disk space for the snap stores. The device on which these folders reside will be excluded from the list of snapshot-able disks. If this path is on a device mapper, all disks that make up that device mapper, will be excluded. Paths set here should be on a separate block volume (physical, iSCSI, rbd, etc).

```text
snapstore_destinations = "/mnt/snapstores/snapstore_files"
```

#### Adding, formatting, and mounting the extra disk

  * list the current disks after adding the extra disk and start its partitioning

```text
ls /dev/sd*

fdisk /dev/sdx
```

  * run through the partitioning tool steps

```text
list partitions = p

create new partition = n

set the partition number = 1 (default)

write to disk = w
```

  * format the newly created partition

```bash
sudo mkfs.ext4 /dev/sdx1
```

  * mount the previously formatted partition

```text
mount /dev/sdx1 /mnt/snapstores/snapstore_files
```

Once the disk is formatted and mounted Coriolis will automatically add the new mount to fstab, while running the Agent install script.

### Network prerequisites 

The network requirement will be for the machine to have **port 80** and **port 9999** (if the default port for the server is used during the Snapshot Agent installation process) opened.

Coriolis will use**port 80** for connecting and generating **Certificates** for the **Bare Metal Server** using its built-in CA which will perform an HTTP challenge.

This is required to be open only during the Agent installation, or any other time when the Agent is reinstalled or upgraded.

**Port 9999** will be used for the Coriolis Appliance to connect and communicate with the server.
