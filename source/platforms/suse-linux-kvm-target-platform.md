---
title: "SUSE Linux (KVM) as a destination cloud"
wp_id: 43972
---

# SUSE Linux (KVM) as a destination cloud

## Migrating to SUSE Linux (KVM)

When using SUSE Linux as a KVM-based virtualization platform, Coriolis integrates with each KVM host through **libvirt** , which is the management library and API used to control KVM/QEMU environments.

Coriolis connects to the libvirt service through **SSH**(TCP/22) on each SUSE Linux KVM host to perform the operations required during migration workflows. In this design, each SUSE Linux KVM host must expose a functional libvirt endpoint that Coriolis can reach and authenticate against.

**Note:** Migration to SUSE Linux on KVM applies to standard virtual machines only. SAP HANA workloads require a separate licensing model and endpoint, which provide SAP HANA-specific configuration options needed to meet performance, support, and compliance requirements.

### Endpoint connection parameters

A valid SSH private key is required for authentication when configuring the Coriolis endpoint. The corresponding public key must already be configured and authorized on the target Libvirt host **before** the endpoint can be used.

> **Note:** It is recommended to use a dedicated service account for Libvirt endpoint access instead of the root account. The account should have sufficient **permissions** to access and manage Libvirt resources on the target host. On systems using group-based access control, this typically includes membership in the **libvirt and kvm groups**.

The SSH private key must be provided as part of the endpoint configuration and must be **base64-encoded** before submission. Only the SSH private key content should be encoded and passed to the endpoint.

If an SSH private key is provided in the connection info, it must be base64-encoded, and then the resulting string must be used as the value in the endpoint configuration.

> base64 -w0 <path-to-private-key>

![](_static/images/suse-linux-endpoint.png)

#### Transfer executions

![](_static/images/target-options.png)

#### Steps performed by Coriolis

  1. If this is the first execution of the VM transfer, create empty storage volumes on the destination Libvirt host, each matching the size of a disk the VM had on the source. If this is a later replica execution, update the existing volumes — resizing any that have grown on the source and deleting any that no longer exist.
  2. Create a temporary worker VM (minion machine) on the destination Libvirt host, booting from the worker image specified. The worker VM receives its SSH key and metadata via a cloud-init config drive using the no-cloud metadata format.
  3. Once the worker VM is running and reachable, hot-attach the replica volumes to it.
  4. Read disk data from the source and stream it to the worker VM's backup writer service, which writes the data to the replica volumes at the correct offsets.
  5. Once all disk contents have been transferred, stop and delete the worker VM.

#### Transfer deployment

#### Steps performed by Coriolis

  1. Optionally, clone the transferred volumes to produce a clean set of volumes as the starting point for deployment, leaving the originals intact in case of a rerun.
  2. Create a temporary worker VM (OS morphing minion) and hot-attach the replica volumes to it.
  3. Perform the OS morphing process: the morphing worker scans the attached disks for the OS installation of the VM being migrated, mounts it, and applies the steps needed to integrate it for the KVM/Libvirt platform.
  4. Detach the migrated volumes and delete the OS morphing worker VM.
  5. Create the final VM in Libvirt using a generated domain XML built using the settings specified during the migration.

## Temporary worker image for migration

When running a migration to Libvirt, Coriolis uses temporary worker VMs to receive disk data and perform OS morphing. The images for these worker VMs must be pre-staged as volumes in a dir-type Libvirt storage pool on the destination host, and referenced by volume name in the Temporary worker target environment option.

Worker images must have a standard initialisation agent installed and configured for first boot:

  * **Linux** – cloud-init and qemu-guest-agent
  * **Windows** – cloudbase-init, virtIO drivers, and the qemu guest agent

The instructions below describe the process of setting up the Windows worker image:

Freshly install Windows in a KVM virtual machine.

Install Cloudbase-Init, without running sysprep from the installation wizard.

Edit the Cloudbase-Init configuration file (typically C:\\\Program Files\\\Cloudbase Solutions\\\Cloudbase-Init\\\conf\\\cloudbase-init.conf) to match the following:

```ini
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
metadata_services=cloudbaseinit.metadata.services.configdrive.ConfigDriveService,cloudbaseinit.metadata.services.httpservice.HttpService
plugins=cloudbaseinit.plugins.common.mtu.MTUPlugin,cloudbaseinit.plugins.windows.ntpclient.NTPClientPlugin,cloudbaseinit.plugins.common.sethostname.SetHostNamePlugin,cloudbaseinit.plugins.windows.extendvolumes.ExtendVolumesPlugin,cloudbaseinit.plugins.windows.winrmlistener.ConfigWinRMListenerPlugin,cloudbaseinit.plugins.common.userdata.UserDataPlugin
```

Save the configuration and start a sysprep process, then shut down the Windows VM.

Place the resulting QCOW2 disk image in a dir-type Libvirt storage pool on the destination host.

For more information regarding the Coriolis Worker image, please check the [_Coriolis Temporary Migration Worker_](../reference/coriolis-temporary-migration-worker.md) page.

## OSMorphing steps

Depending on the OS being migrated, the following notable steps are performed as part of the OSMorphing process:

### Linux

  * Installing cloud-init
  * Installing qemu-guest-agent (where supported by the distribution)
  * Rebuilding initramfs to include VirtIO drivers (update-initramfs on Debian/Ubuntu; dracut on RedHat-based distributions)
  * Configuring network interfaces for DHCP (where set_dhcp = true)
  * Setting SELinux autorelabel flag (RedHat-based distributions)

### Windows

  * Downloading the VirtIO driver ISO and injecting the drivers.
  * Downloading and installing Cloudbase-Init

## Configuration options

Below is a listing of the configuration section needed when migrating to SUSE Linux (KVM):

```ini
[libvirt_migration_provider]

# Name of the Libvirt storage pool to be used for volumes with unspecified
# storage backing option from the source or which could not be mapped in
# the "storage_mappings".
default_storage_pool =

# Default image paths used for worker instances during migrations.
# Format: key:value,key2:value2
migr_image_map =

# The integer size (in GBs) of the volume to boot temporary worker VMs from.
migr_worker_volume_size = 25

# The amount of memory (in MBs) to allocate to temporary worker VMs.
migr_worker_memory = 4096

# The amount of vcpus to allocate to temporary worker VMs.
migr_worker_vcpus = 2

# The name of an existing Libvirt network used for worker VMs.
migr_worker_network =

# What mechanism to use when sending disk data to the temporary VMs.
# Choices: https, ssh
data_transfer_mechanism = https

# Write the VM serial console output to a file.
enable_vm_console_log = true

# The directory used to store console log files on the Libvirt host.
vm_console_log_dir = /var/log/libvirt/qemu

# Attach a VNC console to the VM. Port is selected automatically.
enable_vm_vnc_console = false

# The VNC listen address.
vnc_listen_address = 0.0.0.0

# URL to a .iso file containing the Windows VirtIO drivers.
windows_virtio_iso_url = https://fedorapeople.org/groups/virt/virtio-win/direct-downloads/stable-virtio/virtio-win.iso

# Whether or not to configure the VM to use DHCP during OSMorphing.
set_dhcp = true

# Whether or not to use config drive to send metadata to the migrated instance.
use_config_drive = false

# Whether or not Coriolis should reconfigure cloud-init during OSMorphing
# to preserve existing user credentials, SSH auth, and keypairs.
retain_user_credentials = true

# CPU mode to use for Libvirt domains (e.g. 'host-passthrough', 'host-model').
# When empty, Libvirt's default behaviour is used.
cpu_mode = host-passthrough

# Disable CPU features that would prevent the VM from being live migrated.
cpu_migratable = true

# Optional list of CPU feature names to require on created domains.
cpu_features = rdtscp,invtsc,x2apic

# Source used to retrieve IP addresses from the migration worker VM.
# Choices: agent, lease, arp
migr_worker_iface_addr_src = agent

# The path of the SSH key used when connecting to Libvirt hosts.
ssh_key_path =

# The location of the SQLite database file for backend-specific data.
sqlite_database_file = /opt/coriolis/libvirt_provider_db.sqlite

# Attach a persistent TPM device to replica instances.
add_tpm_device = true
```
