---
title: "Preparing a VM for migration/replication"
wp_id: 38777
---

# Preparing a VM for migration/replication

When migrating VMs, it is important to verify that the source VM guest OS version is still supported by the vendor itself or ensure that the package repositories are properly maintained on the source VM.
When attempting to migrate an EOL distro release, additional manual steps might be required, as Coriolis will require installing some packages for the migrated VM and the repositories will have to be present. Otherwise, such packages will have to be manually pre-installed on the source VM prior to the migration. Please refer to the official list of supported guest OSes and versions, older ones might not work as part of the migration and are not supported by Coriolis

Please refer to the vendor's pages for the supported version, or consider upgrading the source VM prior to starting the migration.

For SUSE products, including OpenSUSE variants, you can head to this page: [Lifetime - openSUSE Wiki](https://en.opensuse.org/Lifetime)

### Other backup software considerations

**Important:** Before starting a VM migration with Coriolis, pause any other third-party backup tools that protect the source VMs, or explicitly exclude the VMs from those backup jobs for the duration of the migration. Running concurrent backup operations during migration can interfere with snapshot handling, change tracking, or disk consistency and may cause migration failures or inconsistent migrated workloads.

NOTE! The guest OS on the source platform must also be correctly set to at least the higher level, such as (generic) Linux or (generic) Windows. As the overall recommendation, the guest OS should already be defined as good practice, such as Ubuntu Server or Windows Server. As Coriolis is agentless, we rely on such information to be correctly set, in order to perform operations such as the OSMorphing stage according to the migrated OS.

For example, in the case of a VM running on VMware, the guest OS can be set under the VM settings:

[![](_static/images/image.png)](https://i0.wp.com/cloudbase.it/wp-content/uploads/2025/10/image.png?ssl=1)

While in the source VM settings, any CD-ROM attachments should be unmounted or removed, as Coriolis will not migrate such types.

## Setting the network configuration

In the migration process, Coriolis will do its best to ensure that the instance on the destination is booted with a similar, or, if possible, identical networking setup.

While certain aspects cannot be guaranteed for every supported destination platform (such as the exact bus setup or the order in which the devices appear to the VM), Coriolis will always attempt to create virtual NIC resources with the **same MAC address**.

NOTE!  Some platforms may not support explicitly setting a MAC address when creating a virtual NIC. Please review the documentation for the respective platform plugins for any warnings related to this aspect.

Depending on the situation, there are several aspects apart from the MAC address to consider:

  * does the destination platform use a DHCP server?
  * do all the network name mappings in the **network_map** parameter describe networks with matching (ideally 1:1) virtual subnet ranges?
  * do the **network_map**  mappings also consider other parameters, such as DHCP being enabled on all the destination networks mapped to a DHCP-enabled network on the source?

### Recommended steps for Linux VMs

  * **install the guest agent** of the respective platform hosting the VM in the case of platforms that rely on the agent to report the network configuration. This will later allow Coriolis to query the APIs of the platform for exact details of the internal networking configuration of the VM (interfaces, addresses, etc)
  * configure static IPs on all network interfaces that are configured with DHCP. This allows full user control over the instance's addresses on the destination platform. Granted, the subnet ranges of the source and destination networks as mapped in the network_map coincide
  * update any udev rules describing interface naming to rely explicitly on the MAC address of the interfaces. Coriolis guarantees that the MAC address of the interfaces will be replicated on destination clouds that support the explicit setting of a MAC address on a vNIC
  * check package repositories for local sources. The sources should be available from the destination Cloud during the OSMorphing stage. Any local sources i.e. CD-ROM should be commented out. 
    * make sure that the repositories are updated successfully on the source VM
    * for RedHat-based distros use "**yum update**" and for Debian/Ubuntu use "**apt update**"
    * if the repositories are not available or reachable on the target platform, the packages can be manually pre-installed by the user on the source VM before running the Coriolis migration. The required packages are outlined [here](https://cloudbase.it/coriolis-airgapped-environments/#Other_considerations). This skip check on the repository validity has been superseded by checking for the required packages to be pre-installed, starting with Coriolis v2603.4.

### Recommended steps for Windows VMs 

  * **install the guest agent** of the respective platform hosting the VM in the case of platforms that rely on the agent for reporting the network configuration. This will later allow Coriolis to query the APIs of the platform for exact details of the internal networking configuration of the VM (interfaces, addresses, etc)
  * configure static IPs on **all network interfaces** that are configured with DHCP. This allows full user control on the addresses the instance will have on the destination platform, granted that the subnet ranges of the source and destination networks, as mapped in the network_map coincide

* * *

## Setting storage configuration

In the migration/replication process, Coriolis will do its best to preserve the block device ordering the VM had on the source platform.

Depending on the destination platform's limitations (such as supported bus types, block storage paravirtualization features, and so on) the order of block devices, and thus the naming scheme for Linux-based OSes may differ.

### Recommended storage steps for Linux VMs

  * **update /etc/fstab to use filesystem UUIDs** to identify partitions to be mounted. Any other naming scheme may be unreliable due to limitations on some supported destination platforms The UUIDs of the partitions can be found by using the "**blkid**" command, and then the **/etc/fstab** file has to be edited to replace the references with the **UUID=value** or **LABEL=value** instead

  * update/remove any udev rules describing block device naming that rely on a disk's physical aspects, such as a vendor ID, bus ID, and so on. Depending on the limitations of the destination platform, Coriolis may not be able to guarantee that such specific aspects relating to the disk devices will be preserved

  * **if replicating, install the guest agent** of the respective platform hosting the VM, in the case of platforms that rely on an agent to support filesystem quiescing. During the replication process, Coriolis will always attempt to quiesce the filesystems of a running instance to ensure the consistency of the filesystems of the replica after a replica execution

  * ensure that the **/boot** partition has enough free disk space to accommodate rebuilding all existing installed kernels' initramfs image. This is a step in the OSMorphing process before the instance is booted onto the destination cloud.

### Recommended steps for Windows VMs

  1. Just as for Linux VMs, for Windows VMs, ensure that the latest virtualization guest agent (such as the Windows VirtIO agent) is installed and running on the Windows guest system. The guest agent is specific to the respective platform hosting the VM for platforms that rely on an agent to support filesystem quiescing. During the replication process, Coriolis will always attempt to quiesce the filesystems of a running instance to ensure the consistency of the replica filesystems after a replica execution.
  2. **For Windows VMs, ensure that the latest Windows updates are installed** and that the guest OS is rebooted to finish the installation of the updates. This is due to all the components involved in the snapshotting process, such as VSS, related to the Windows OS, and used as part of the migration process.

* * *

## Firmware type support

This table will outline all the supported virtualization/cloud platforms by Coriolis, and whether their respective providers support UEFI firmware, with/without Secure Boot.

| **Supported in Export Provider**| **Supported in Import Provider**  
---|---|---  
![](_static/images/openstack.png)  
**OpenStack**|  ![:check_mark:](_static/images/check_mark_32.png)*| ![:check_mark:](_static/images/check_mark_32.png)  
![](_static/images/Vmware.svg.png)| ![:check_mark:](_static/images/check_mark_32.png)| ![:check_mark:](_static/images/check_mark_32.png)  
![](_static/images/aws.png)| ![:ballot_box_with_check:](_static/images/2611.png)| ![:ballot_box_with_check:](_static/images/2611.png)  
![](_static/images/Microsoft_Azure.svg_.png)  
**Microsoft Azure**| ![:ballot_box_with_check:](_static/images/2611.png)| ![:ballot_box_with_check:](_static/images/2611.png)  
![](_static/images/Blank-diagram.png)  
**Linux servers**| ![:check_mark:](_static/images/check_mark_32.png)| ![:heavy_minus_sign:](_static/images/2796.png)  
![](_static/images/oracle2022.png)  
**Oracle PCA**| ![:heavy_minus_sign:](_static/images/2796.png)| ![:check_mark:](_static/images/check_mark_32.png)  
![](_static/images/oracle2022.png)  
**OCI**| ![:heavy_minus_sign:](_static/images/2796.png)| ![:check_mark:](_static/images/check_mark_32.png)  
![](_static/images/lxd-logo.png)  
**MicroCloud (LXD)**| ![:heavy_minus_sign:](_static/images/2796.png)| ![:check_mark:](_static/images/check_mark_32.png)  
![](_static/images/ovm.jpg)| ![:x:](_static/images/274c.png)| ![:x:](_static/images/274c.png)  
![](_static/images/OVirt-logo-highres.png)  
**OLVM & RedHat Virtualization (RHV)** | ![:check_mark:](_static/images/check_mark_32.png)| ![:check_mark:](_static/images/check_mark_32.png)  
![](_static/images/ws2022.png)  
**Microsoft Hyper-V**| ![:check_mark:](_static/images/check_mark_32.png)| ![:heavy_minus_sign:](_static/images/2796.png)  
![](_static/images/18700703.png)  
**SUSE Virtualization (Harvester)**| ![:heavy_minus_sign:](_static/images/2796.png)| ![:check_mark:](_static/images/check_mark_32.png)  
![](_static/images/proxmox-logo-stacked-color.svg)| ![:heavy_minus_sign:](_static/images/2796.png)| ![:check_mark:](_static/images/check_mark_32.png)  
*OpenStack instances do not have an exact way of telling if they’re UEFI instances or not, besides reading instance metadata, which may not always be available. In those cases, the Firmware type can be overridden by a source environment option

![:check_mark:](_static/images/check_mark_32.png) : fully supports UEFI with Secure Boot

![:ballot_box_with_check:](_static/images/2611.png) : only supports UEFI firmware, but no Secure Boot

![:x:](_static/images/274c.png): the underlying platform does not support UEFI or Secure Boot

Secure Boot is not yet fully supported on AWS, only on Windows instances, but Coriolis will not be enabling it until proper support is added. Coriolis does not yet support Secure Boot for Azure.

### Bootloader checks on the source VM

As part of migrating Linux instances, Coriolis will run several steps that touch the boot configuration and kernels of the migrated guest OS (on the target disks, source VM configuration is untouched).

To ensure a smooth process, we recommend the following to be done on the source VM, before running the migrations:

  * update the kernel to the latest available version and reboot the source VM. This will ensure that regenerating the initramfs kernel images is also functional, this being a step that Coriolis will perform as part of the OS Morphing process.
  * Remove any obsolete / no longer required older kernels on the source VM. This will also cover the requirement that enough free disk space is available on the /boot partition.

* * *

For the supported guest OSes, Coriolis can handle the default bootloaders.

To check the bootloader on the VM(s) meant to be migrated, run the following command:

```bash
sudo dd if=/dev/<relevant OS partition/disk> bs=512 count=1 2>/dev/null | strings | grep -Eoi 'grub|lilo'
```

The command above will check on the selected disk if the bootloader is installed. Please make sure that the selected partition/disk in the one hosting the OS.

```text
##output##

root@coriolis:~# sudo dd if=/dev/sda bs=512 count=1 2>/dev/null | strings | grep -Eoi 'grub|lilo'
GRUB
root@coriolis:~#
```

* * *

## On-demand Linux images subscription in Public Clouds

Several cloud service providers, such as Amazon Web Services (AWS) or Microsoft Azure, provide on-demand Linux images bundled with a paid subscription. Such subscription-based services are provided for RedHat Cloud Access or Ubuntu Advantage and are bundled as part of the cloud provider access.

NOTE! When moving a subscription-based Linux VM from a supported cloud provider to a different environment - either a different cloud or internal infrastructure - the user is responsible for the license continuity and ensuring that the license terms are not violated.

In the case of Red Hat Enterprise Linux (RHEL), you must handle this either by bringing your own subscription (BYOS) or by contacting the sales representative of the Linux vendor on what the best subscription switch path is.

Coriolis requires that, as part of the OS Morphing stage, it will continue to access the distribution repositories to prepare the OS for the destination endpoint.

This implies installing a set of Linux packages, depending on the distribution. Therefore, the VM must be prepared to ensure that packages can be installed successfully from the repositories before moving the VM from the source to the destination endpoint. Please refer to the distribution license terms to ensure that you are eligible to continue using the subscription and comply with the destination cloud or platform-supported license methods.

* * *

## VMware migrations

To ensure consistency between the running VMware (ESXi) version and the VMs, it is recommended to check and ensure that for the VMs to be migrated, the VM hardware version in VMware must be set to match the running VMware version.

For Coriolis, the requirement is that the minimum hardware version for virtual machines be version 13 or newer (ESXi 6.5).

* * *

## Source VM Guest Agent

Depending on the source platform and underlying hypervisor, a guest agent is usually present on the source VM. For example, this can be the QEMU Guest Agent for KVM-based hypervisors and platforms, VMware Tools, and other similar agents.

QEMU guest agent is highly recommended to be running inside the VM that is being migrated to ensure the application snapshot consistency and additional integrations, such as shutting down the source VM before the last sync feature in Coriolis. The same will apply to other platforms, so before starting the migration, you should ensure that the latest guest agent is installed and running on the VMs.
