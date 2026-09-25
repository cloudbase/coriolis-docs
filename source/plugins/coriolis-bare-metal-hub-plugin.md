---
title: "Coriolis Bare Metal Hub Plugin"
wp_id: 41641
---

# Coriolis Bare Metal Hub Plugin

**Coriolis** integrates the platform Plugin on the Appliance itself. Here, Coriolis will need to take advantage of Snapshot Agents deployed on the Bare Metal Server to establish communication with the Plugin. This way, Coriolis guarantees the connection to the Bare Metal server, as long as all requirements are met.

**Bare Metal Hub Plugin** is one of the supported Source platforms by Coriolis, which will allow Migrating workload from bare-metal to the cloud, for what is called **Physical to Virtual (p2v)** , as Coriolis supports multiple clouds as Destination platforms.

[![Coriolis P2V](_static/images/p2v-3.jpg)](https://i0.wp.com/cloudbase.it/wp-content/uploads/2025/08/p2v-3.jpg?ssl=1)

Coriolis P2V

Source to Coriolis required ports:

  1. TCP port 9999 for communication between Coriolis and the Bare Metal Server. The port can be customized.
  2. TCP port 80 for the Coriolis certificate issuing process upon Snapshot Agent install on the Bare Metal Server. This is required only once - during Agent installation.



For the Coriolis appliance to the target platform port requirements, you can refer to [this page](https://cloudbase.it/coriolis-network-ports-requirements/).

In the **Bare Metal Hub** , which is a UI section for Coriolis-metal-hub functionality, you will be able to:

  * Register bare metal servers that already have the snapshot agent installed;
  * Show bare metal server information;
  * Edit bare metal endpoint information (in case of the snapshot agent API endpoint changes - i.e. the server’s IP changes);
  * Force refresh bare metal server information pulled from the snapshot agent
  * There are Create Replica and Create Migration buttons available straight in the bare metal server’s information page, which brings you directly to choosing the target in the execution wizard;
  * Coriolis-metal-hub CLI tool is also available on the appliance, which exposes most of the operations mentioned above.



The **Bare Metal Hub Endpoint** comes pre-configured with the **Coriolis** Appliance, meaning that the service is running and ready for **Replica/Migration**.

For this type of Replica/Migration to work, we will need to have an agent running on the machine, which is quite different from all our other Plugins for supported platforms.

### Supported Releases

The following Linux distributions have been validated, and based on the kernel mapping below, the releases are known to be working. A newer minor kernel release for the below is expected to continue to work with the Coriolis Bare-Metal Agent as listed.

**NOTE! Incremental Replica syncs for a bare-metal server using the Coriolis Agent are currently supported only for Linux kernel 5.11 and below.**

**For other kernels, only the "lift-and-shift" Coriolis Migrations are supported, incremental syncs not being available.**

**Release**| **Supported versions**| **Latest kernel verified**  
---|---|---  
![](_static/images/ubuntu.svg)   
**Ubuntu Server**|  16.04 - 22.04| 5.15.0-83  
![](_static/images/redhat.jpg)  
#### Red Hat Enterprise
**Linux**|  7.0 - 8.3| 4.18.0-240  
![](_static/images/centos.svg)  
**CentOS**|  7.0 - 8.3| 4.18.0-240.22  
![](_static/images/oracle.jpg)  
**Oracle Linux**|  7.9 - 8.3| 4.18.0-240  
Red Hat Compatible Kernel
![](_static/images/suse.jpg)  
**SUSE Linux**|  12 - 15 SP4| 5.14.21-150400.24  
![](_static/images/opensuse.svg)  
**openSUSE Leap**|  15.4| 5.14.21-150400.24  
![](_static/images/debian.jpg)  
**Debian**|  10| 4.19.0-21  
**NOTE:** Oracle Linux Unbreakable Kernel is not supported, **Red Hat Compatible Kernel** must be used instead.

### Installing the Snapshot Agent

The Coriolis Snapshot Agent for Bare Metal Servers is used for the process of Replica/MIgrate to be possible, and the agent is required to be installed on the machine for Coriolis to be able to communicate with it and fetch the machine info and clone the disks.

The installation guide can be found on the **[Snapshot Agent](https://cloudbase.it/installing-the-snapshot-agent) **page.

### Add Bare Metal Server using Coriolis Dashboard

As the Endpoint and the Snapshot Agent are installed, the next step is to add the machine as a Bare Metal Server in Coriolis:

  * in the Dashboard, navigate from the left side menu to Bare Metal Server



[![](_static/images/bm-severs.jpg)](https://i0.wp.com/cloudbase.it/wp-content/uploads/2022/10/bm-severs.jpg?ssl=1)

  * Select 'Add a Bare Metal Server' and add the Host address and the port for the machine, and click 'Add'
    * the IP address of the machine
    * the port set upon installing the snapshot agent



[![](_static/images/addbm.jpg)](https://i0.wp.com/cloudbase.it/wp-content/uploads/2022/10/addbm.jpg?ssl=1)

  * Once the machine has been contacted, the connection will be validated and listed as **active** , meaning that the machine is ready to be used for **Replica/Migration**.


  * Also, Coriolis will display the hardware details of the newly added machine



[![](_static/images/addedsrv1.png)](https://i0.wp.com/cloudbase.it/wp-content/uploads/2022/10/addedsrv1.png?ssl=1)

### File-systems supported

The Coriolis Bare Metal Agent supports consistent snapshot-based backup for the following file systems:

  * ext4
  * ext3
  * ext2
  * btrfs
  * xfs
  * reiserfs
  * jfs
  * hfsplus
  * f2fs
  * hfs
  * ntfs
  * vfat
  * nilfs2



Additional file systems should also be supported as long as the corresponding kernel module and tools/utilities for the file system are present on the host system.

Note! If the bare-metal server running the Coriolis Snapshot Agent is rebooted, on the next Coriolis Replica run, a full data sync will occur, and not incremental. That is due to the kernel module tracker for incremental snapshots, which gets reset in the event of a bare-metal reboot.
