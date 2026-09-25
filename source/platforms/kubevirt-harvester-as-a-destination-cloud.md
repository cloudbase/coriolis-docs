---
title: "KubeVirt/Harvester as a destination cloud"
wp_id: 43149
---

# KubeVirt/Harvester as a destination cloud

## Migrating (CMaaS) to KubeVirt

Migrations to KubeVirt operate in the same way Replicas do and thus entail the same requirements and steps described below.

[![](_static/images/Untitled.png)](https://i0.wp.com/cloudbase.it/wp-content/uploads/2024/07/Untitled.png?ssl=1)

## Replicating (DRaaS) to Kubevirt

### Replica executions

Steps performed by Coriolis:

  1. If this is the first replica execution, create empty volumes on the destination cloud, each matching the specifications of a disk the VM had on the source. If this is a later replica execution, the previously created volumes are used;
  2. if this is the first replica execution of the VM, create a new live snapshot of the disks of the VM on the source cloud (handled by whatever source cloud plugin we are using). If this is a later replica execution, create a new live snapshot based on the last successful replica execution;
  3. create a temporary Linux worker VM in Kubevirt (the “disk copy worker”) and attach the volumes from Step 1 to it;
  4. read the contents of the snapshot created in Step 2, transfer the written/changed chunks to the temporary VM created in Step 3, which then writes the chunks at the appropriate index/offset of the disks created in Step 1;
  5. once the contents of all the disks have been synced to the volumes created in Step 1, detach the volumes and delete the disk copy worker created in Step 3.



### Replica deployments

Steps performed by Coriolis:

  1. create snapshots of the replicated volumes on the destination cloud to be able to roll back any changes. By default, new volumes are created from these snapshots, leaving the original replica volumes intact for future replica executions. As a fallback, a direct volume clone is created if the destination Kubevirt does not support volume snapshots.
  2. depending on the OS of the VM whose replica is being deployed, boot a temporary worker VM (“the OSMorphing worker”) with the same OS type on the destination cloud, and attach the volumes from Step 1 to it;
  3. perform the “OSMorphing process”, where Coriolis commands the OSMorphing worker created in step 2 to scan all attached disks for the OS installation of the VM we are migrating, mount, and perform the steps needed to prepare the installation for the new platform (i.e. installing VirtIO drivers if deploying a replica of a Windows VM);
  4. detach the volumes created in step 1 from the OSMorphing worker created in step 2, and delete the temporary worker VM;
  5. create and boot the migrated VM in the destination cloud with the specifications of the original VM in the source cloud (as noted during the replica execution we are deploying), and create and attach any necessary network ports and volumes.



### Temporary worker image for Replica/Migration

When choosing to run a transfer task to Kubevirt, Coriolis will detect whether the destination cloud has support for local VM images (generally on Harvester) and list those as worker image options. If VM images are not supported, any PVC or container disk-type image can act as a worker image, but must be configured in the configuration options beforehand.

Two worker images are required for Coriolis migrations, and those are one for Linux OS type and one for Windows migrations.

For transfer operations involving both Windows and Linux systems, as well as for the OS Morphing stage during Linux VM migrations, we recommend using the **OpenSUSE Leap 16.0** cloud server image, which can be downloaded from [here](https://download.opensuse.org/distribution/leap/16.0/appliances/Leap-16.0-Minimal-VM.x86_64-Cloud.qcow2). The image works out of the box and requires no additional configuration.

For Windows, an image with VirtIO drivers and Cloudbase-init installed should be used.

The instructions below describe the process of setting up the Windows worker image:

  * Fresh install Windows from official ISO image;
  * Update Windows Server machine until no more updates appear after reboot;
  * Install the **VirtIO drivers** and the **Qemu-guest-agent** for Windows by using the [**VMDP package**](https://github.com/SUSE/vmdp/releases);
  * Download and Install [**Cloudbase-Init**](https://cloudbase.it/downloads/CloudbaseInitSetup_Stable_x64.msi), without running sysprep from the installation wizard;
  * edit the Cloudbase-Init configuration files (usually under **C:\Program Files\Cloudbase Solutions\Cloudbase-Init\conf\cloudbase-init.conf** and **C:\Program Files\Cloudbase Solutions\Cloudbase-Init\conf\cloudbase-init-unattended.conf**) to match the one below:




```ini
##### cloudbase-init.conf
[DEFAULT]
username=Admin
groups=Administrators
inject_user_password=true
config_drive_cdrom=true
config_drive_vfat=true
bsdtar_path=C:\Program Files\Cloudbase Solutions\Cloudbase-Init\bin\bsdtar.exe
mtools_path=C:\Program Files\Cloudbase Solutions\Cloudbase-Init\bin\
verbose=true
debug=true
log_dir=C:\Program Files\Cloudbase Solutions\Cloudbase-Init\log\
log_file=cloudbase-init.log
default_log_levels=comtypes=INFO,suds=INFO,iso8601=WARN,requests=WARN
logging_serial_port_settings=COM1,115200,N,8
mtu_use_dhcp_config=true
ntp_use_dhcp_config=true
local_scripts_path=C:\Program Files\Cloudbase Solutions\Cloudbase-Init\LocalScripts\
check_latest_version=false
metadata_services=cloudbaseinit.metadata.services.nocloudservice.NoCloudConfigDriveService
plugins=cloudbaseinit.plugins.common.mtu.MTUPlugin,cloudbaseinit.plugins.windows.ntpclient.NTPClientPlugin,cloudbaseinit.plugins.common.sethostname.SetHostNamePlugin,cloudbaseinit.plugins.windows.extendvolumes.ExtendVolumesPlugin,cloudbaseinit.plugins.windows.winrmlistener.ConfigWinRMListenerPlugin,cloudbaseinit.plugins.common.userdata.UserDataPlugin

[config_drive]
raw_hdd=true

##### cloudbase-init-unattended.conf
[DEFAULT]
username=Admin
groups=Administrators
inject_user_password=true
config_drive_cdrom=true
config_drive_vfat=true
bsdtar_path=C:\Program Files\Cloudbase Solutions\Cloudbase-Init\bin\bsdtar.exe
mtools_path=C:\Program Files\Cloudbase Solutions\Cloudbase-Init\bin\
verbose=true
debug=true
log_dir=C:\Program Files\Cloudbase Solutions\Cloudbase-Init\log\
log_file=cloudbase-init-unattend.log
default_log_levels=comtypes=INFO,suds=INFO,iso8601=WARN,requests=WARN
logging_serial_port_settings=
mtu_use_dhcp_config=true
ntp_use_dhcp_config=true
local_scripts_path=C:\Program Files\Cloudbase Solutions\Cloudbase-Init\LocalScripts\
check_latest_version=false
metadata_services=cloudbaseinit.metadata.services.nocloudservice.NoCloudConfigDriveService,cloudbaseinit.metadata.services.configdrive.ConfigDriveService,cloudbaseinit.metadata.services.httpservice.HttpService,cloudbaseinit.metadata.services.ec2service.EC2Service,cloudbaseinit.metadata.services.maasservice.MaaSHttpService
plugins=cloudbaseinit.plugins.common.mtu.MTUPlugin,cloudbaseinit.plugins.common.sethostname.SetHostNamePlugin,cloudbaseinit.plugins.windows.extendvolumes.ExtendVolumesPlugin
allow_reboot=false
stop_service_on_exit=false

[config_drive]
raw_hdd=true
```
  
  * Save the configuration and shutdown the VM;
  * Delete the Kubevirt VM, but keep the root PVC;
  * Considerations: 
    * If VM images are supported, export the PVC as an image. Add the following image label for Coriolis to be able to detect it as a Windows image: 
      * **harvesterhci.io/os-type : windows**
      * If it's an EFI image, the following **annotation** must be also added to the VMImage object (under **metadata.annotations**): **vm.boot/firmware** : **uefi**
    * If VM images are not supported, set this PVC as a Windows image in the Kubevirt configuration options: 
      * **[kubevirt_migration_provider] migr_image_map = linux: quay.io/containerdisks/ubuntu:22.04, windows: my-namespace/my-windows-pvc**



## OSMorphing steps taken when migrating to KubeVirt

Depending on the OS release that is being migrated, the following notable steps will be performed as part of the OSMorphing process:

### Linux

  * installing cloud-init
  * where supported, installing the guest agent (qemu-guest-agent)
  * where required, rebuilding initrd to enable the VirtIO drivers



### Windows

  * installing the VirtIO drivers
  * installing cloudbase-init



## Configuration Options

Below is a listing of the configuration section needed when migrating/replicating to KubeVirt/Harvester:

```json
[kubevirt_migration_provider]
# Default storage class to use
# default_storage_class = 

# Default snapshot storage class to use
# snapshot_storage_class = 

# The OS migration image map to use. This mapping will be used to spin up the OSMorphing worker
migr_image_map = linux: quay.io/containerdisks/ubuntu:22.04, windows:

# Namespace in which migrations should happen
namespace = default

# The maximum number of CPU cores to allocate to instances. This is a hard cap to default to when
# migrating huge instances.
# max_cpu_cores = 

# The maximum memory to allocate to instances. This is a hard cap to default to when migrating huge
# instances.
# max_memory_mb = 

# On some storage backends, restoring PVCs from snapshots do not work as intended, therefore, for
# migrations, volume snapshots can be disabled by enabling this option.
disable_volume_snapshots = false

# VM network used to deploy the worker VM on. Must be reachable by the Coriolis appliance. If multiple
# networks are not supported, the default pod network is used.
# migr_network = 

# What mechanism to use when sending disk data from the Coriolis installation to the temporary VMs on
# the target KubeVirt to be written to their respective disk. The HTTPS-based transfer mechanism
# (TCP/5566) is faster but might not work if there are firewalls in the way. The SSH-based transfer
# mechanism (TCP/22) is more costly but will be allowed by most firewalls since SSH access from the
# Coriolis installation to the temporary worker VM is always required. Default is HTTPS.
data_transfer_mechanism = HTTPS

# Whether or not Coriolis should reconfigure the Migrated VMs to use DHCP on all network interfaces
# during the OSMorphing process.
set_dhcp = true

# CPU core limit to be set to the worker VMs
migr_worker_cpu_limit = 2

# Memory limit (in GiB) to be set to the worker VMs
migr_worker_memory_limit = 4

# Worker Root Disk size (in GiB) to be created when deploying a worker machine from a VM Image.
migr_worker_disk_size = 15

# Location of the virtio-win ISO
windows_virtio_iso_url = https://github.com/SUSE/vmdp/releases/download/2.5.4.2/VMDP-WIN-2.5.4.2-Community.iso

# Location of the Cloudbase-Init ZIP for amd64 systems
cloudbaseinit_x64_url = https://www.cloudbase.it/downloads/CloudbaseInitSetup_x64.zip

# Location of the Cloudbase-Init ZIP for x86 systems
cloudbaseinit_x86_url = https://www.cloudbase.it/downloads/CloudbaseInitSetup_x86.zip

# Type of disk device to emulate on the migrated instance. Currently supported values are:
# virtio, sata, scsi, usb
disk_bus = virtio

# Network interface card model to emulate on the migrated instance. Currently supported values
# are: e1000, e1000e, ne2k_pci, pcnet, rtl8139, virtio
nic_model = virtio
```
  
## Harvester 1.2

When migrating to a **Harvester version 1.2** environment, the volume snapshots created as Replica backups by Coriolis might fail to provision.

As a solution, volume snapshot backups can be disabled, and Coriolis will use full PVC clones as Replica disk backups. Volume snapshots can be disabled by using the **disable_volume_snapshots** option in the Coriolis configuration file, under the [kubevirt_migration_provider] option group.
