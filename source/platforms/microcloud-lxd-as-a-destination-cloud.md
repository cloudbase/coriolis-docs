---
title: "MicroCloud (LXD) as a Destination Cloud"
wp_id: 42661
---

# MicroCloud (LXD) as a Destination Cloud

## Migrating (CMaaS) to LXD

Migrations to LXD operate in the same way Replicas do and thus entail the same requirements and steps described below.

## Replicating (DRaaS) to LXD

### Replica executions

Steps performed by Coriolis:

  1. if this is the first replica execution of the VM, create an empty Replica VM, which will contain the replicated root disk, and create empty storage volumes, each matching the specifications of a disk the VM had on the source. If this is a later replica execution, the previously created volumes are used
  2. if this is the first replica execution of the VM, create a new live snapshot of the disks of the VM on the source cloud (handled by whatever source cloud plugin we are using). If this is a later replica execution, create a new live snapshot based on the one from the last successful replica execution
  3. if inexistent, create a disk copy worker volume on the destination LXD, used as template for future worker processes. This template will get cloned every time a new execution gets created and used as disk copy worker. Attach the worker disk along with the replicated data disks to the Replica VM, set the worker disk as top boot priority, and launch the Replica VM, it should boot into the disk copy worker OS and wait for replication data.
  4. read the contents of the snapshot created at step 2 via the source platform’s snapshot/backup APIs (handled by whatever source cloud plugin we are using), transferring the written chunks to the disk copy worker launched in step 3, which then writes the chunks at the appropriate index/offset of the disks made at step 1.
  5. once the contents of all the disks have been synced to the volumes created in step 1, stop the Replica VM, detach the volumes (including the worker volume), and delete the worker volume created in step 3.



### Replica deployments

Steps performed by Coriolis:

  1. create snapshots of the previously replicated volumes on the LXD (including the Replica VM which includes the replicated root volume) to roll back any changes. By default, new volumes are made from these snapshots, leaving the original replica volumes intact for future replica executions, either clone or rename the Replica VM, to use as OSMorphing VM.
  2. depending on the OS of the VM whose replica is being deployed, create a temporary worker disk (“the OSMorphing worker”) from the worker template volume, with the same OS type on the destination cloud, and attach it to the OSMorphing VM along with the data volumes from step 1 to it, set top boot priority to the OSMorphing worker disk.
  3. perform the “OSMorphing process”, where Coriolis commands the OSMorphing worker created at step 2 to scan all attached disks for the OS installation of the VM we are migrating, mount, and perform the steps needed to prepare the installation for the new platform (ex: uninstalling the VMWare guest tools and installing VirtIO drivers)
  4. detach the volumes created at step 1 and 2 from the OSMorphing VM and delete the OSMorphing worker disk.
  5. boot the migrated VM on LXD with the specifications of the original VM on the source cloud (noted during the replica execution we are deploying), creating and attaching any necessary NICs and volumes.



### Temporary worker image for Replica/Migration

When choosing to run a task of **Replica/Migration** to **LXD** , Coriolis lists images available locally on the destination MicroCloud/LXD, and also from Ubuntu’s official releases remote. Images listed are filtered by **amd64** architecture and **virtual-machine** type. Also, from the Ubuntu remote, only supported LTS images are listed. If an image from a different custom remote needs to be used, we recommend copying it to the local image remote. This is because Coriolis can only access local images via LXD API, parsing and filtering remote images directly from the**simplestreams** image server. We chose the Ubuntu releases remote because it’s static on any destination LXD, therefore it cannot be changed/deleted from the platform.

The instructions below describe the process of setting up the Windows worker image:

  1. follow the [official tutorial](https://ubuntu.com/tutorials/how-to-install-a-windows-11-vm-using-lxd#1-overview) to freshly install Windows from ISO image;
  2. install Cloudbase-Init, without running sysprep from the installation wizard;
  3. edit the Cloudbase-Init configuration file (usually under **C:\Program Files\Cloudbase Solutions\Cloudbase-Init\conf\cloudbase-init.conf**) to match the one below:



```json
[DEFAULT]
username=Admin
groups=Administrators
inject_user_password=true
config_drive_raw_hhd=true
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
```
  
  4. Save the configuration and start a sysprep process, shutdown the Windows VM afterward
  5. Save the LXD VM as an image using the publish command:  




```text
lxc publish <vm_name> --alias windows-worker --reuse description="Windows Worker Image" release="<Windows release version>" type=disk os=windows
```
  
## Configuration Options

[![](_static/images/lxc-options.png)](https://i0.wp.com/cloudbase.it/wp-content/uploads/2023/08/lxc-options.png?ssl=1)

Below is a listing of the configuration section needed when migrating/replicating to MicroCloud/LXD:

#### Configuration options for LXD as destination

```json
[lxd_migration_provider]

# Default network name used for worker instances during migrations.
# migr_network =

# Images used for worker instances during migrations
# migr_image_map = linux: <fingerprint>, windows: <fingerprint>

# Default storage pool used for replica disks.
# default_storage_pool =

# CPU limit of the replica VM
# migr_worker_cpu_limit = 2

# Memory limit (in GiB) of the replica VM
# migr_worker_memory_limit = 4

# Whether or not Coriolis should reconfigure cloud-init during OSMorphing to prevent
# it from creating a new system user or disabling the root user and other existing users,
# including by disabling password-based SSH authentication, or locking the user by
# changing/removing its password completely.
# retain_user_credentials = false

# What mechanism to use when sending disk data from the Coriolis installation to the
# temporary VMs on the target OCI to be written to their respective disk.
# The HTTPS-based transfer mechanism (TCP/5566) is faster but might not work if there
# are firewalls in the way. The SSH-based transfer mechanism (TCP/22) is more costly but
# will be allowed by most firewalls since SSH access from the Coriolis installation to the
# temporary worker VM is always required. Coriolis automatically sets security groups rules
# for the temporary VMs accordingly. Default is HTTPS. Accepted values are: HTTPS, SSH
# data_transfer_mechanism = HTTPS

# Use network forward address on the worker's interface, for Coriolis to externally gain access.
# The address is randomly chosen from the selected migration network's uplink.
# Only available on bridged networks.
# use_network_forwarding = false  
```
  
## OSMorphing steps taken when migrating to LXD

Depending on the OS release we are migrating, the following notable steps will be performed as part of the OSMorphing process:

### Linux

  * installing cloud-init
  * where supported, installing guest agent (lxd-agent)
  * where required, rebuilding initrd to add the VirtIO drivers



### Windows

  * installing the VirtIO drivers
  * installing cloudbase-init and enabling cloudbase-init service



For more information regarding the Coriolis Worker template, please check the [Coriolis Temporary Migration Worker](https://cloudbase.it/coriolis-temporary-migration-worker) page.
