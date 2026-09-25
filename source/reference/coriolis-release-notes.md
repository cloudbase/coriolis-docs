---
title: "Coriolis Release Notes"
wp_id: 40587
---

# Coriolis Release Notes

Latest Release

## Version 2608.2

### Changes and improvements

  * Linux OSMorphing: 
    * Fix static preservation if the mac changes on the destination;
    * Fix resolv.conf restoration;
    * Fix volume management when using minion pools;
    * Fix LVM auto-mounting disks when using minion pools;
  * Adds FQDN export info, fixes hostname porting
  * Upgrade process improvements
  * Adds support for the **StackIt** platform, as source and destination;
  * Security fixes: 
    * Fully updated with latest security patches provided by Ubuntu;

### Coriolis Provider Kubevirt

  * Fixes PVC access mode management when creating destination volumes

### Coriolis Provider Nutanix

  * Adds ability to export VM inventory in CSV format;
  * Improves upon source VM shutdown

### Coriolis Provider Openstack

  * Updates endpoint Glance version to v2;
  * Fix os_type/os_distro image metadata assignment;
  * Fix volume attachment management

### Coriolis Provider oVirt

  * Excludes link-local addresses when testing minion connection;
  * Increase ballooning minimum memory for Windows

### Coriolis webUI

  * various UX and security fixes

* * *

### Previous Releases

## Version 2608.1

### Changes and improvements

### Coriolis Provider VMware

  * Adds **export_mechanism** source option, with the ability to use the in-built **[OpenVixDiskLib](https://github.com/cloudbase/OpenVixDiskLib)** library to export VMs. 
    * Updating to this release will install OpenVixDiskLib, as well as exposing an option to load a licensed VDDK provided by the end-user.

## Version 2608.0

### Changes and improvements

  * Linux OSMorphing: 
    * Add support for migrating VMs with **LABEL=** fstab entries;
    * Fix Debian static IP preservation issue (cannot decode 'str' object);
    * Added support for RHEL-family release 10 migrations (exceptions: Azure & OCI as destination);
    * Installs required packages for migrating encrypted VMs to minion machine;
    * Added configurable TPM PCRs to be applied when migrating encrypted VMs;
    * Added support for Ubuntu 26 as minion, and any other minion that uses **sudo-rs** ;
    * Optimizes dracut rebuilding;
  * Windows OSMorphing: 
    * cloudbase-init no longer sets real time clock to UTC post-deployment;
    * Stages virtio ballooning service installation;
    * All Windows migrations will use stable cloudbase-init builds by default;
  * Improves boolean value handling in API requests;
  * Fixed API reference build;
  * Removed **< string>.log** log entry;
  * Added **SAP on SLES KVM** migration provider;
  * Added **Nutanix** source provider;
  * Added **CloudStack** destination provider;
  * Fixed replicator ssh tunneling;
  * Added ability to patch individual components for smaller appliance updates;
  * Fixed mariaDB logs filling up the appliance disk;
  * Security fixes: 
    * Fully updated with latest security patches provided by Ubuntu;

### Coriolis Web UI

  * Masks temporary encryption key set in the target environment;
  * Displays SAP migration licensing;
  * Updates with security fixes;

### Coriolis Provider AWS

  * Updates minion list;

### Coriolis Provider Azure

  * Adds ability to export VM inventory in CSV format;

### Coriolis Provider Kubevirt

  * Fix cloud-init crash when no user data is being passed;
  * Fix memory readings from migrated VM;
  * Fix pod network validation (errors out if multiple NICs of the same VM are set to use the **pod network**);
  * Added **data_transfer_mechanism** as a target environment option (exposed to UI);

### Coriolis Provider Libvirt

  * Adds support for importing VMs with shared disks;

### Coriolis Provider LXD

  * Fix disk bus option;

### Coriolis Provider OpenStack

  * Add Storage AZ override option;

### Coriolis Proivder oVirt

  * Adds support for preserving the first NIC of the migrated VM;
  * Adds ability to export VM inventory in CSV format;

### Coriolis Provider Proxmox

  * Makes config drive optional via **use_config_drive** option;
  * Fix VMID and disk attachment race conditions;
  * Adds **add_tpm_device** target option;

### Coriolis Provider VMWare

  * Adds support for exporting VMs with shared VMDKs (destination cloud options are currently limited);
  * Improves upon VMWare tools and drivers removal by making it an offline uninstallation instead of post-deployment removal;

## Version 2603.4

### Changes and improvements

  * Linux OSMorphing: 
    * commands retrial optimizations;
    * grub mounts/dismounts fixes;
    * RedHat-based guest repository management improvements;
    * SUSE repository/modules management improvements;
    * install fallback uefi bootloader on Debian;
    * Fix migrated VM's grub entries from gathering minion entries;
    * Fix DHCP migrations for Redhat and SUSE guests;
    * Fix UEFI grub executable entries on BIOS guests ('linuxefi' not found on boot);
    * Customise cloud-init datasources on various destination platforms;
  * Windows OSMorphing: 
    * Drops creation of 'Admin' user when migrating Windows;
    * Validate downloaded virtio ISO;
  * Deployer manager optimizations;
  * Task cancellation fixes;
  * Adds support for new user script phases (pre-osmount, post-osmount, first-boot scripts);
  * Adds ability to migrate disk-encrypted VMs by LUKS and BitLocker to various destination platforms: SUSE Virtualization and SUSE KVM destinations officially supported;
  * Fix transfer scheduling;
  * Adds API-side pagination for optimized loading;
  * Security fixes: 
    * Disables weak SSH MAC algorithms & adds ability to disable SSH service entirely;
    * Updated TLS cipher support to 1.2+ only;
    * Allows editing barbican, keystone, rabbitmq apache/wsgi configs (mainly for hardening purposes);
    * Fully updated with latest security patches provided by Ubuntu;

### Coriolis Web UI

  * Optimizes page loading;
  * Fixes config option defaults when loading transfer options;
  * Supports setting new user script phases;
  * Various security updates;

### Coriolis Provider Kubevirt

  * Adds support for booting UEFI-backed minions;
  * Adds "retain_user_credentials" option to target environment;
  * Fix SELinux relabeling post-migration;
  * Adds native encrypted VM migration support;
  * Adds support for migrating RHEL 10 (and supported derivates);
  * Adds QEMU Guest Agent installation for Windows Migrations;

### Coriolis Provider Libvirt

  * Adds native encrypted VM migration support;

### Coriolis Provider LXD

  * Adds Ubuntu 24 & 26 OSMorphing support;
  * Fix Replica VM cloning;
  * Added "set_dhcp" option, static IP preservation will be supported from this point on;
  * Fixes migrations with multiple disks;
  * Fix LXD live-migration incompatibilities with config drive;
  * Fix backup writer-reported "device is busy" problem by force unmounting minion's EFI partition;
  * Adds "disk_bus" option, so users can customize what bus to use for migrated volumes;
  * Adds "target_profile" and "migr_worker_profile" options, so users can customize what LXD profiles to use on migrated and minion VMs;
  * Fix network forward creation once on each available CIDR;
  * Adds "use_config_drive" option. Users can control whether the migrated VM will have a config drive or not;
  * Added complete Virtio Driver installation when migrating Windows VMs;

### Coriolis Provider OpenStack

  * Adds ability to export VM inventory in CSV format;
  * Fix hostname normalization for migrated VMs;

### Coriolis Proivder oVirt

  * Adds support for preserving the first NIC of the migrated VM;
  * Adds ability to export VM inventory in CSV format;

### Coriolis Provider Proxmox

  * Optimize disk identification;
  * Fixes machine type option input for i440fx;
  * Enables KVM virtualization by default for migrated VMs;
  * Fix volume deactivations on LVM backends;

### Coriolis Provider VMWare

  * Updates VM inventory CSV format;
  * Fixes TLS certificate verification on endpoint connections;
  * Improves upon source disk identification;

## Version 2603.2

### Changes and improvements

  * Fixed tasks hanging in "PENDING" or "RUNNING" statuses;
  * Introduces SUSE KVM as destination provider; 
  * Improved command retrial;
  * Added VM inventory CSV export capability (limited to source provider support);
  * Fix percentage progress not showing 100% on complete transfers;
  * Adds OSMorphing support for Ubuntu 24.04 and Ubuntu 26.04;
  * Disable /etc/hosts reset when preserving static IPs;
  * Improved proxy configuration workflow in the console.

### Coriolis Web UI

  * Added VM inventory CSV export in the endpoint screen;
  * Various evnrionment options and cosmetic improvements.

### Coriolis Provider Kubevirt

  * Added Minion Pooling support;
  * Worker VM deployment speed and configuration improvements;
  * SUSE Virtualization: Add support for VMImages residing on custom CSI types;
  * Attach TPM device on migrated VMs.

### Coriolis Proivder Ovirt

  * Improved replica disk management;
  * Fixes migrated Windows machines' memory display in the oVirt dashboard.

### Coriolis Provider Proxmox

  * Adds options for SCSI Controller model, Machine Type, Data Transfer Mechanism;
  * Fix template cloning on storage that doesn't support linked clones.

### Coriolis Provider VMWare

  * Adds ability to use fastlz compression when retrieving disk data;
  * Adds ability to export VM inventory in CSV format;
  * Fixes left-over VMWare service removal;
  * Fixes disk integrity validation.

## Version 2603.1

### Changes and improvements

  * New feature: Add post-transfer disk checksum verification - VMware source
  * Added support for SUSE minions;
  * Fixed error and loading delay on transfer execution creation;
  * Added disk detection improvements for the writer service;
  * More network preservation fixes.

### Coriolis web UI

  * Improved option reload and display.

### Coriolis Provider Azure

  * Updated public IPv4 usage from deprecated 'Basic' to 'Standard'.

### Coriolis Provider Kubevirt

  * Fix worker NIC model;
  * Improve worker connections (skips link-local IPs).

### Coriolis Provider oVirt

  * Improve agent installation on older linux systems;
  * Adds high availability enablement option;
  * Adds memory ballooning force disablement option. 

### Coriolis Provider Proxmox

  * Fix disk resize on incremental executions.

### Coriolis Provider VMware

  * Add disk integrity validation.

## Version 2603.0

### Changes and improvements

  * Added fix for **Rakuten Cloud**(KubeVirt plugin)
  * Improve virtIO drivers' logic on all applicable platforms
  * Add cache listed instances for large environments for faster VM inventory
  * Fix grub issue for all Red Hat-based OSes with version 9+
  * Handle files containing non-utf8 characters
  * New feature - Added a Coriolis upgrade option
  * Defaulting internal services to TLS 1.2+
  * Reduce internal Coriolis services network exposure
  * Static IP preservation improvements

### Coriolis web UI

  * Improved logs download
  * Security fixes

### Coriolis Provider Kubevirt

  * Update default Windows VirtIO ISO URL to latest release

### Coriolis Provider oVirt

  * Fix OS release pass to final VM
  * Add TPM support for Windows OS releases that require it
  * Set proper timezone by default when creating VMs
  * Automatically set valid OS release
  * Setup QEMU Guest Agent installation local script
  * Refactor cloud-init support
  * Other fixes and improvements

### Coriolis Provider Proxmox

  * Fix clone template not retrying on some recoverable errors.
  * Add disk extra attachment properties
  * Improve list_storage by fetching the storage directly from the Proxmox client
  * Other fixes and improvements

### Coriolis Provider VMware

  * Add VLAN ID detection for standard vSwitch port groups
  * Uninstall the VMware Tools when migrating off from VMware
  * Other fixes and improvements

## Version 2506.2

### Changes and improvements

  * Global cloud-init configuration improvements;
  * RPC client leak fix;
  * Fix Windows user scripts when attempting custom script injection;
  * Enables Alma Linux migrations using CentOS OSMorphing tools;
  * Log rotation improvements;
  * Removed support for Oracle VM platform;
  * Other fixes and improvements regarding Windows osmount and file permission issues.

### Coriolis web UI

  * Fix user role assignment;
  * Fix VM information fetch;
  * Increase default VM list page to 100.

### Coriolis Provider Kubevirt

  * added support for WaitForFirstConsumer storage class types;
  * other PVC related fixes.

### Coriolis Provider Openstack

  * Fix Debian and Ubuntu osmorphing (bootloader and initramfs rebuilding);
  * Volume snapshot race condition fix (when using minion pools with auto-deploy).

### Coriolis Provider oVirt

  * Add support for Virtio Drivers version 2.2+.

### Coriolis Provider Proxmox

  * Fix VM disk extension (on Proxmox 9);
  * Default to virtio model when scsi bus is being used, and also switch to using SATA bus for cloud-init drive;
  * Port VLAN tag to migrated VM NICs, when using VLAN-aware Proxmox networks;
  * Fixes network listing;
  * Port virtualization type of migrated VM (KVM hardware virtualization is enabled if the VM had nested virtualization enabled on the source);
  * Fix final instance name.

### Coriolis Provider VMWare

  * Fix source VM poweroff;
  * Add final disk controller option;
  * Fix ESXi source hosts connection validation;
  * Install native VMWare Tools when migrating Windows VMs;
  * Fix migrations with multiple disks;
  * Optimize VM listing (including backend caching capability);
  * Uninstall VMWare Tools when exporting Windows VMs;
  * Add InstanceUuid VM identification scheme.

## Version 2506.1

### Changes and improvements

  * Fixed an issue with handling EOL in user scripts
  * Improved policy handling for RBAC rules.
  * Other fixes and improvements in multiple plugins - oVirt (OLVM & RHEV), MicroCloud, Proxmox VE and KubeVirt / SUSE Virtualization

### Coriolis web UI

  * Add a pagination count selector for the number of instances (and other objects) to display in one view.
  * Fixed a regression in the OpenStack endpoint creation and validation in regards to the Allow untrusted/self-signed SSL certificate for the OpenStack services.

## Version 2506.0

*Note* This release contained a regression in the OpenStack endpoint creation in regards to the Allow untrusted/self-signed SSL certificate for the OpenStack services. This has been addressed in 2506.1.

### New features

  * Added [VHI](https://www.virtuozzo.com/hybrid-infrastructure/) provider
  * Added [SUSE Virtualization](https://www.suse.com/products/rancher/virtualization/) provider

### Changes and improvements

  * Fixes and improvements to the network preservation logic
  * Fix osmorphing debian permission denied while reading file
  * Improve the deployer operations
  * Move internal RabbitMQ to use TLS by default

### Coriolis web UI

  * Bumped Node.js to version 22, as well as upgrading all dependencies
  * Fixed a bug in the OpenStack endpoint - Allow Untrusted toggle option

### Coriolis Provider for oVirt - OLVM and RHEV

  * Snapshot Transfer Disks when not cloning disks for deployment
  * Request consistent snapshots when exporting VMs
  * Other fixes and improvements

### Coriolis Provider for Proxmox VE

  * Add Proxmox VE SDN support
  * Filter final VM localhost subnets when detecting IP addresses
  * Fix vm disk naming convention

## Version 2412.3

### Changes and improvements

  * VMware to OpenStack migrations now preserve the VM hostname from the source platform

## Version 2412.1

### New features

  * Migrations have been redesigned to allow transfers (data replication), with controlled switch-over on when the VM is to be created on target 
    * In addition, the **Auto Deploy** option allows setting an incremental sync, followed by automatically completing the migration.

### Changes and improvements

  * The Coriolis version is now tracked in the diagnostics.log file
  * **Coriolis Web UI:** the interface has been updated to reflect the new **Transfers** and **Deployments** sections
  * SCVMM plugin has been deprecated as is no longer supported

### Coriolis Provider for OLVM / oVirt

  * New option was added to control the disk allocation
  * Switch to Oracle VirtIO drivers for Windows OS Morphing

### Coriolis Provider for OCI

  * Windows OS Morphing is now using OCI VirtIO drivers v2.2

### Coriolis Provider for OpenStack

  * Disable cloud-init networking with `set_dhcp=false`
  * Add `disk_bus` import option
  * Better handling of the security group used by Coriolis

### Coriolis Provider for VMware

  * Improvements for VM schema validation due to inconsistencies in VM configuration
  * Exposing the vixdisklib log for better VMware troubleshooting
  * Improved VMware endpoint validation checks
  * Added support for VMware deployments using **NSX**
  * Add cloudbase-init for writing static IP

* * *

## Version 2407.1

This version is a fix-release, addressing an issue with adding an OpenStack endpoint.

* * *

## Version 2407.0

### New features

  * Introducing **KubeVirt** (including**Harvester)** as new target platforms
  * Added TLS certificate support for the Coriolis REST API

### Changes and improvements

  * Better handling of disk mounting operations in the OS Morphing stage
  * Various fixes and improvements in the Coriolis licensing mechanism

### Coriolis Provider for OLVM / oVirt

  * Switch to Oracle virtIO drivers
  * Update VM disk(s) naming convention
  * Switch minion disk attachment interface to virtio-scsi
  * Other fixes and improvements
  * Handle fixed CDROM device in OLVM/oVirt for migrated Windows VM for drive letter consistency
  * 

### Coriolis Provider for OCI

  * Fix predictable NIC naming disablement
  * Fix driver enablement for RHEL-based guest OSes
  * Other fixes and improvements

* * *

## Version 2403.1

This is a minor release to address several bugs and to bring several improvements:

  * fix a web UI issue that caused the loss of defined settings and fields when using the Recreate Migration option
  * For OpenStack provider: Add guest_os_type_override source environment option
  * OpenStack: prevent instance listing skip if the source image is not found
  * OpenStack: Add retries logic for Linux minion SSH connection
  * oVirt/OLVM: fixed several issues
  * LXD/MicroCloud: added support for LXD 5.21.0 LTS

* * *

## Version 2403.0

### New features

  * Introducing **Proxmox** as a new destination platform
  * Added support for Amazon Linux 2 (AL2) in OSMorphing
  * Improvements in the Windows OSMorphing process 

### Coriolis Provider for MicroCloud / LXD

  * Set and identify VM OS type
  * Various fixes and improvements

* * *

## Version 2309.1

### Changes and fixes

  * Overall fixes and improvements
  * Improve Windows OSMorphing speed
  * Refactor grub2 console setting for Linux machines
  * Improve dpkg option for no prompt

### Coriolis Provider for VMware

  * Upgraded vixdisklib library to version 8.0.2
  * Install Windows drivers for VMware from the official VMware repository
  * Various improvements and fixes

### Coriolis Provider for OCI

  * Add Oracle Compute Cloud@Customer provider
  * Improve multi-NIC instance migrations
  * Various improvements and fixes

### Coriolis Provider for MicroCloud / LXD

  * Setup LXD Agent in OSMorphing
  * Disable EDD on RHEL-based machines
  * Various improvements and fixes

* * *

## Version 2309.0

### New features

  * Introducing a new supported destination platform - **Canonical MicroCloud | LXD**
  * Added support for Ubuntu 22.04 LTS
  * Added support for RedHat 9.x, including community-driven distributions 
    * Added support for Rocky Linux 8.x and 9.x
  * Expanded migration support for UEFI-based instances 
    * including better handling for Secure Boot feature migration
    * automated handling of q35 machine type under OpenStack with KVM

### Coriolis Provider for VMware

  * Upgraded vixdisklib library to the latest 7.0 series, which is compatible with all VMware 6.x to 8.x products
  * Fixed a bug in incremental backup corruption when detecting a large delta
  * Various small improvements and fixes

### Coriolis web UI

  * Improve the license module layout for a simplified summary of used/remaining licenses
  * Overall web UI improvements
  * Updated libraries to address multiple vulnerabilities

### Changes and fixes

  * Regenerate initrd for all kernels where applicable
  * Updated Coriolis virtual appliance with the latest security updates and patches
  * Make the HTTPS backup writer more resilient on SELinux-enforced worker machines
  * Added an option in the console menu to configure the proxy settings

* * *

## Version 2210.1

### New features

  * Introducing a new supported destination platform - **Oracle Private Cloud Appliance (PCA) X9-2**
  * Backup writer improvements 
    * improved support for SELinux-enabled temporary worker machines
    * added support for nftables
  * Deprecated OPC target provider

### Coriolis Provider for VMware

  * Fixed an issue for vSAN backends

### Bare Metal Agent

  * Coriolis Bare Metal Agent version 1.1.1 has been released and is available [here](https://github.com/cloudbase/coriolis-snapshot-agent/releases/tag/1.1.1)
  * Fixed an issue handling swap disks
  * Various fixes and improvements

### Coriolis web UI

  * Added option to download an archive of all Coriolis logs
  * Improvements to the Metal Hub Servers page
  * Show OS type in the migration wizard
  * Overall web UI improvements
  * Updated libraries to address multiple vulnerabilities

* * *

## Version 2210.0

### New features

  * Introducing **Coriolis Bare Metal Agent** - migrating p2v 
    * This can also be used for v2v where platform access is limited
    * Linux Agent only is currently available
    * More details can be found at [Coriolis Bare Metal Hub Plugin - Cloudbase Solutions](../plugins/coriolis-bare-metal-hub-plugin.md)
  * Introducing support for **OLVM - Oracle Linux Virtualization Manager** - as a destination platform 
    * This is backed by oVirt and KVM nodes
    * **RedHat Virtualization (RHV/RHEV)** is also supported as a destination platform
  * Added support for **Ubuntu 22.04** in OSMorphing
  * Added support for **flexible shapes on OCI**
  * Defaulting Data Transfer Mechanism to HTTPS 
    * HTTPS-based transfers are faster when compared with SSH-based ones, choice between options is still available

### Changes and fixes

  * Better handle yum repositories in OSMorphing
  * Fix an issue with drive letters when mounting disks on Windows minions
  * Logging messages improvements
  * Updated Coriolis virtual appliance with the latest security updates and patches
  * Fixed an issue between Windows and Linux minion pool setup
  * Small improvements and fixes for the Coriolis Azure / AzureStack provider

### Coriolis Provider for OpenStack

  * Multiple fixes and improvements
  * Fixed an issue with the Glance API version selection

### Coriolis Provider for VMware

  * Updated built-in vixdisklib version to 6.7

### Coriolis Provider for OCI

  * Added support for flexible shapes
  * Added support for Dedicated VM Hosts
  * Multiple OCI shapes-related fixes and improvements
  * Added field in web UI for the Windows virtIO drivers
  * Fix an issue with secondary vNIC attachment

### Coriolis Provider for OVM

  * Reduce public IP address wait time when finalizing the migration
  * Attempt to gracefully stop the worker VM instead of powering off
  * Fetching OS labels from OVM API

### Coriolis Provider for AWS

  * Updated options for AWS configuration
  * Fixed an issue with the region parameter for AWS endpoint configuration

### Coriolis web UI

  * Updated all web components to fix security vulnerabilities
  * Added EULA and Privacy consent OOBE screen
  * Overall web UI improvements
  * Fixed multiple issues

* * *

## Version 2111.0

### New features

  * Coriolis virtual appliance console menu 
    * This new feature allows configuring and managing the Coriolis settings directly from the appliance. Coriolis information can also be obtained from here.
  * Support for short UUID filesystems
  * Disable compression in the default configuration 
    * As the general recommendation is for the Coriolis virtual appliance to be hosted on the destination cloud, compressing transfer is disabled. This should be used when the Coriolis worker process is hosted on the source cloud and can be controlled from the Coriolis configuration file.

### Changes and fixes

  * Faster web UI
  * Various performance fixes
  * Improved API access policies
  * Reduce memory footprint during job executions
  * Security fixes for the Coriolis virtual appliance

### Coriolis Provider for OpenStack

  * Fix snapshot cleanup for cloned source disks
  * Other fixes and improvements

### Coriolis Provider for VMWare

  * Add Windows guest OSMorphing tools
  * Fix a memory leak during large disks transfers
  * Other fixes and improvements

* * *

## Version 2102.3

### New and enhanced features

  * **Coriolis OVM Exporter**

Coriolis OVM Exporter brings incremental backups to OVM for more efficient migrations. The new feature is explained in detail here: [Coriolis OVM exporter - Cloudbase Solutions](../platform-notes/coriolis-ovm-exporter.md)

  * **Add OCI provider minion pool support**

Alongside OpenStack, Minion Pools are now supported in OCI as well. Refer to this page for more details: [Coriolis Minion Pools operations and usage - Cloudbase Solutions](../features/coriolis-minion-pools-operations-and-usage.md)

  * **Improved operations for RedHat/Oracle Linux/CentOS**

Better handling of the yum repositories and network configuration, along with full support for RedHat 8 based distributions.

  * **Resolved an issue with the Replica Schedule**
  * **Improved support for SUSE repositories configuration**
  * **Better handling of Windows disks in OSMorphing**

Fix an issue with WinRM and PowerShell 4.0 and improve disk servicing during OSMorphing of Windows instances disks.

### Other improvements

### Coriolis web UI

  * Security fixes for dependencies
  * Add a link to Coriolis Help page
  * Minor bug fixes

### Coriolis Provider for OpenStack

  * Improved logic to prevent volume device misidentifications caused by non-standard nova configuration.

### Coriolis Provider for VMWare

  * Add SCSI drivers to RHEL-based OSMorphing tools
  * Resolved an issue when listing resources for faulty VMs

### Coriolis Provider for OVM

  * Improved cleanup of temporary worker
  * Added OS label for latest releases of Linux / RedHat and Windows Server
  * Fixed RHEL6-based OSMorphing
  * Minor bug fixes

### Coriolis Provider for OCI

  * Fix NSG listing
  * Added support for the new OCI-generated private key data decoding
  * Other bug fixes

* * *

## Version 2102.2

### Coriolis web UI

  * Multiple bug fixes

* * *

## Version 2102.1

### Coriolis Provider for VMWare

  * Add VMware as a Target Platform
