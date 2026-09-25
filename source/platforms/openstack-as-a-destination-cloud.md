---
title: "OpenStack as a destination cloud"
wp_id: 38996
---

# OpenStack as a destination cloud

### Migrating (CMaaS) to OpenStack

Transfer Migrations to OpenStack operate in the same way Transfer Replicas do and thus entail the same requirements and steps described below.

### Replicating (DRaaS) to OpenStack

#### Replica executions:

#### Steps performed by Coriolis

  1. if this is the first replica execution for the VM, create empty Cinder volumes on the destination cloud, each matching the specifications of a disk the VM had on the source. If this is a later replica execution, the previously created Cinder volumes are used
  2. if this is the first replica execution of the VM, create a new live snapshot of the disks of the VM on the source cloud (handled by whatever source cloud plugin we are using). If this is a later replica execution, create a new live snapshot based on the one from the last successful replica execution
  3. create a temporary Linux worker VM in Nova (the "disk copy worker") on the destination cloud and attach the Cinder volumes from Step 1 to it
  4. read the contents of the snapshot created at step 2 via the source platform's snapshot/backup APIs (handled by whatever source cloud plugin we are using), transferring the written chunks to the temporary VM created in step 3, which then writes the chunks at the appropriate index/offset of the disks created at step 1
  5. once the contents of all the disks have been synced to the Cinder volumes created in Step 1, detach the Cinder volumes and delete the disk copy worker created in Step 3

#### Replica deployments:

#### Steps performed by Coriolis

  1. create snapshots of the replicated Cinder volumes on the destination cloud to be able to roll back any changes. By default, new volumes are created from these snapshots, leaving the original replica volumes intact for future replica executions
  2. depending on the OS of the VM whose replica is being deployed, boot a temporary worker VM ("the OSMorphing worker") with the same OS type on the destination cloud, and attach the Cinder volumes from step 1 to it
  3. perform the "OSMorphing process", where Coriolis commands the OSMorphing worker created in step 2 to scan all attached disks for the OS installation of the VM we are migrating, mount, and perform the steps needed to prepare the installation for the new platform (ex: uninstalling the VMWare guest tools and installing VirtIO drivers if deploying a replica of a Windows VM from vSphere to a KVM-based OpenStack)
  4. detach the Cinder volumes created at step 1 from the OSMorphing worker created at step 2 and delete the temporary worker VM 
  5. create and boot the migrated VM on the destination cloud with the specifications of the original VM on the source cloud (which have been noted during the particular replica execution we are deploying), creating and attaching any necessary Neutron ports and Cinder volumes.

### Configuration Options

#### Advanced Target options for OpenStack target destination

In the case of Replicating or Migrating to OpenStack, there will need to be images that the worker will use to create temporary VMs to perform the tasks, for both Linux and Windows machines.

The template OS version must be at least the same as the OS of the VM that needs to be migrated.

**NOTE!** When Replicating/Migrating a **Windows VM** , both **Linux and Windows templates**  have to be specified, as **Disk cloning**  is performed using the Linux template and **OSMorphing**  is performed using the Windows template.

In case a Floating IP Pool network is not visible to be selected, it can mean that the network resides under another tenant project. To overcome this, you must enable the "**List All Destination Networks**".

The Floating IP Pool network must also carry the "router:external" property set, on the OpenStack side.

[![](_static/images/openstack-target-new-1.jpg)](https://i0.wp.com/cloudbase.it/wp-content/uploads/2021/04/openstack-target-new-1.jpg?ssl=1)

### OSMorphing steps taken when migrating/replicating to OpenStack

Depending on the virtualization technology used and the OS release we are migrating/replicating, the following notable steps will be performed as part of the OSMorphing process:

#### Linux

  * installing cloud-init
  * installing Hyper-V integration tools, if destination OpenStack is based on Hyper-V
  * where required, rebuilding initrd to add the virtIO drivers

#### Windows

  * installing cloudbase-init and enabling cloudbase-init service
  * installing the VirtIO drivers if OpenStack is KVM-based

For more information regarding the Coriolis Worker template, please check the **[Coriolis Temporary Migration Worker](https://cloudbase.it/coriolis-temporary-migration-worker) **page.

### Preserve network settings for migrated VM

When migrating to OpenStack, Coriolis features the capability to preserve the network configuration of the migrated VM(s). This applies to scenarios such as statically assigned IPs and stretched networks for the source and target clouds.

OpenStack's networking model relies on the VMs being internally configured to use DHCP, thus the following set of options are to be used when creating the Migration/Replica:

- **"Set DHCP" = True** -- will have Coriolis reconfigure the VM internally to use DHCP on all interfaces

- **"Preserve Fixed IPs" = True** -- will have Coriolis set the same IP address the source VM had on the Neutron port(s) of the final target VM on OpenStack

In combination, the above two options will lead to Coriolis setting the same IP address(es) the VM had on the source vSphere to the Neutron ports of the migrated VM on the target OpenStack, which Neutron will in turn set via DHCP in the final migrated VM, leading to the effect of "static IPs being preserved" when it's handled via DHCP behind the scenes.

In the case of VMware as a source platform, the to-be migrated VM(s) must have the VMware guest tools installed and the VMware agent running, so that Coriolis can identify the network settings / IPs on the source VM.

Note that the "Preserve Fixed IPs" option requires that the subnet(s) on the Neutron network(s) you set in the "Network Mapping" screen have the following properties:

- the Neutron network(s) you select must contain a Neutron subnet whose IP range includes the IP address(es) of the source VM

- said Neutron subnet which includes the IPs needs to have the "dhcp" flag enabled on it

#### Configuration options for OpenStack as a destination

Below is a listing of the configuration section needed when migrating/replicating to an OpenStack:

```ini
 [openstack_migration_provider]
...
### Import parameters:

# Name of a pre-created availability zone where resources migrated by Coriolis
# will be created in. Note that Coriolis will need to also create any
# temporary resources (such as disk transfer and OSMorphing worker VMs)
# within the same availability zone, so all of the other
# temporary-resource-related options must be compatible with the selected AZ.
# Default is None (Nova will choose the default one for Coriolis)
# availability_zone =

# If migrating/replicating a heterogeneous workload with both Linux and
# Windows instances, separate image names or IDs will need to be provided
# for the temporary OSMorphing workers for each OS type.
# The 'linux' image will be used for the disk copy worker during the replica
# execution process as well
# Only accepted keys are 'linux' and 'windows'
# migr_image_map = linux: 283bdce4-112c-4758-b06a-7e5985a9cd15, windows: Windows Server 2012 R2 Std Eval

# Boolean flag indicating whether or not to list all Neutron networks.
# By default, Coriolis will only list the networks which are in the
# same tenant as the one set in the Coriolis endpoint in use.
list_all_destination_networks = False

# Whether or not unallocated blocks on Cinder target volumes contain
# zeros. This is controlled by the "volume_clear" Cinder configuration
# options. (boolean value)
volumes_are_zeroed = True

# Default hypervisor type. (string value)
# The type of hypervisor the destination OpenStack features,
# supported options being "hyperv", "qemu" or "kvm"
# Default is None, meaning no extra hypervisor-specific actions will be taken
# during the OSMorphing process
hypervisor_type = kvm

# Whether or not to download the worker image to a Cinder volume and boot the
# worker from that. The root disk size on the configured 'migr_flavor_name'
# will be used for the worker VM volume, 'migr_flavor_name' will be used for
# the worker VM volume unless explicitly specified using 'migr_worker_volume_size'.
migr_worker_boot_from_volume = False

# The integer size (in GBs) of the Cinder volume to boot temporary worker VMs
# from. This option is only effective if "migr_worker_boot_from_volume" is set.
# If not set, Coriolis will use the disk size set the selected "migr_flavor_name".
# migr_worker_volume_size =

# Name of the precreated Cinder volume type to use when creating temporary worker volumes.
# This option is only effective if "migr_worker_boot_from_volume" is set.
# migr_worker_volume_type =

# Name of the Cinder volume type to be used for
# volumes with unspecified storage backing option from the
# source or which could not be mapped in the "storage_map".
# Default is "" (Cinder scheduler will
# use default volume type)
# default_cinder_volume_type =

# Whether or not to set the Cinder volumes as ephemeral (to be deleted when
# the VM is deleted) on the newly migrated/replicated instance on the
# destination OpenStack. Default is False.
delete_disks_on_vm_termination = True

# List of names or IDs of pre-existing security groups on the destination
# OpenStack to be applied to the migrated/replicated instance.
# Note that the below set will be joined with the list specified via the
# 'security_groups' parameter from the set of destination environment parameters
# (list value)
# default_security_groups = secgroup1, secgroup2

# Name or ID of an existing Neutron network on the destination
# OpenStack where to attach the Neutron port of the temporary disk
# copy/OSMorphing worker VMs. (string value)
# migr_network = private

# Whether or not to allocate floating IPs from the "migr_fip_pool_name"
# for the temporary disk copy/OSMorphing worker VMs.
# Default is True
migr_worker_use_fip = True

# Name of an existing Neutron network on the destination OpenStack which
# serves as external and may have floating IPs allocated from it.
# These floating IPs will be associated to the temporary disk copy/OSMorphing
# worker VMs.
# Default is "public"
# migr_fip_pool_name = public

# Name of an existing Nova flavor which to boot the temporary
# disk copy/OSMorphing worker VMs as.
# Default is "m1.small"
# (string value)
# migr_flavor_name = m1.small

# Whether or not to use config drive to send metadata to the temporary
# disk copy/OSMorphing worker VMs in case Neutron metadata is not available
# Default is False
migr_worker_use_config_drive = False

# Whether or not to reconfigure the internal network settings of each
# interface of the instance being migrated/replicated during the OSMorphing
# process to have the VM perform DHCP on first boot inside the new environment.
# Default is True
set_dhcp = True

# If set to "reuse_ports", Coriolis will reuse any Neutron ports found with
# the MAC addresses needed for the new VM. If set to "keep_mac", Coriolis
# will delete any ports with the MAC addresses the VM needs and recreate them
# with the same MAC address. If set to "replace_mac", Coriolis will always
# create new ports with new MAC addresses.
port_reuse_policy = keep_mac

# Dictionary with arbitrary key-value pairs to set as tags on the
# migrated/replicated VMs.
# instance_tags =

# Whether or not to preserve the fixed IPs of the migrated instances' Neutron
# ports. When this is set to 'True', the target Openstack cloud will attempt
# to create ports containing fixed IPs collected from the source VM. A subnet
# with the right CIDR is required in the mapped network for the VM's first NIC.
preserve_fixed_ips = False

# If set, Coriolis will attempt to identify a suitable subnet from the provided
# 'floating_ip_pool' on the target OpenStack in which to create a floating IP
# with the same address the VM had on the source.
preserve_floating_ip = False

# Whether or not to attach a floating IP to the already migrated VM. This
# option must be set to 'True' if the migrated VM is intended to have a public
# IP attached. The floating IP will be allocated from the 'floating_ip_pool'
# option.
use_floating_ip = False

# use these flags for uefi with secure boot
#default_custom_boot_volume_image_metadata = os_secure_boot: required,hw_machine_type: q35

# What mechanism to use when sending disk data from the Coriolis installation
# to the temporary VMs on the target OpenStack to be written to their
# respective disk. The HTTPS-based transfer mechanism (TCP/5566) is faster but
# might not work if there are firewalls in the way. The SSH-based transfer
# mechanism (TCP/22) is more costly but will be allowed by most firewalls since
# SSH access from the Coriolis installation to the temporary worker VM is always
# required. Coriolis automatically sets security groups rules for the temporary
# VMs accordingly.
# Choices are 'SSH' or 'HTTPS'. Default is 'HTTPS'.
data_transfer_mechanism = HTTPS

# Parameters related to the OSMorphing process for Windows instances:
windows_virtio_iso_url = https://fedorapeople.org/groups/virt/virtio-win/direct-downloads/stable-virtio/virtio-win.iso
cloudbaseinit_x64_url = https://www.cloudbase.it/downloads/CloudbaseInitSetup_x64.zip
cloudbaseinit_x86_url = https://www.cloudbase.it/downloads/CloudbaseInitSetup_x86.zip
```

### OpenStack destination environment parameters

The destination environment parameters are a set of destination-cloud-specific parameters that offer additional options to the migration/replication process on a per-VM basis.

Below is a listing of the destination environment parameters the OpenStack plugin supports when migrating/replicating a VM to OpenStack:

#### Example of destination environment JSON to be passed to the OpenStack plugin

```json
{
         
         "network_map": {
                "source network name": "name or ID of existing Neutron network in destination OpenStack"
         },
         "storage_mappings": {
                "default": "cinder-volume-type-0",
                "backend_mappings": [{"source": "datastor1", "destination": "cinder-volume-type-1"}],
                "disk_mappings": [{"disk_id": "", "destination": "cinder-volume-type-2"}]
         },
         "hypervisor_type": "kvm",
         "flavor_name": "m1.small",
         "keypair_name": "new-key",
         "delete_disks_on_vm_termination": false,
         "security_groups": ["name of existing secgroup on destination OpenStack", "and another one"],
         
         "migr_image_map": {
                "linux": "Linux migration worker Image name/ID",
                "windows": "63d8f1a4-3192-4edc-b113-0d099b4bc458"
         },
         "migr_network": "private",
         "migr_worker_use_fip": true,
         "migr_fip_pool_name": "external_network/external_subnet",
         "migr_flavor_name": "m1.small",
     "migr_worker_boot_from_volume": true,
     "migr_worker_volume_size": 1,
         "migr_worker_volume_type": "cinder-voltype",
     "list_all_destination_networks": true,
         "migr_worker_use_config_drive": true,
         
         "port_reuse_policy": "keep_mac",
         "volumes_are_zeroed": true,
         "preserve_fixed_ips": true,
         "server_group": "name or ID of Nova server group",
         "use_floating_ip": true,
         "floating_ip_pool": "external_network/external_subnet",
         
         "set_dhcp": true,
         "instance_tags": {
                "tag1": "value1",
                "tag2": "value2"
         }
 }
```

Each parameter represents:

  * **network_map (string-string mapping)** - a mapping between the names of networks on the source cloud and names or IDs of corresponding pre-existing networks on the destination Openstack. For each NIC of the instance on the source cloud, Coriolis will look at the mapped network on the destination OpenStack and ensure the Neutron port corresponding to that NIC is attached to that Neutron network
  * **storage_mappings (object)** - storage-related options such as how to map each disk or storage type on the source to Cinder volume types on OpenStack
  * **hypervisor_type (string)** - the type of hypervisor the destination OpenStack features, supported options being "hyperv", "qemu" or "kvm"
  * **flavor_name (string)** - name of pre-existing Nova flavor on the destination OpenStack for the migrated/replicated instance to be booted as
  * **keypair_name (string)** - name of a pre-existing Nova keypair to be injected into the migrated/replicated instance on the destination cloud
  * **delete_disks_on_vm_termination (boolean)** - whether or not to set the Cinder volumes as ephemeral (to be deleted when the VM is deleted) on the newly migrated/replicated instance on the destination OpenStack.
  * **security_groups (list of strings)** - list of names or IDs of pre-existing security groups on the destination OpenStack to be applied to the migrated/replicated instance
  * **migr_image  (string)** - name or ID of the pre-existing Glance image to be used for the disk copy and/or OSMorphing workers. The name must be unique in the destination cloud. Overrides the settings in 'migr_image_map'
  * **migr_image_map (string-string mapping)** - if migrating/replicating a heterogeneous workload with both Linux and Windows instances, separate image names/IDs will need to be provided for the temporary OSMorphing workers for each OS. The only accepted keys are 'linux' and 'windows'. Please review the "OSMorphing worker images" section for exact details on the requirements of the worker images for each OS type
  * **migr_network  (string)** - name of an existing Neutron network one the destination OpenStack to which to attach the Neutron port of the temporary disk copy/OSMorphing worker VMs
  * **migr_worker_use_fip (boolean)** - whether or not to allocate floating IP addresses from the "migr_fip_pool_name" for the temporary disk copy/OSMorphing worker VMs
  * **migr_fip_pool_name (string)** - name of an existing Neutron network and an associated subnet(optional) on the destination OpenStack which serves as external and may have floating IPs allocated from it. These floating IPs will be associated with the temporary disk copy/OSMorphing worker VMs Coriolis will be creating during the migration/replication process
  * **migr_flavor_name (string)** - name of an existing Nova flavor to boot the temporary disk copy/OSMorphing worker VMs as
  * **migr_worker_boot_from_volume  (boolean)** - Whether or not to download the worker image to a Cinder volume and boot the worker from that.
  * **migr_worker_volume_size (integer)** - The integer size (in GBs) of the Cinder volume to boot temporary worker VMs from. This option is only effective if 'migr_worker_boot_from_volume' is set. If not set, Coriolis will use the disk size set for the selected 'migr_flavor_name'.
  * **migr_worker_volume_type (string)** - Name of the pre-created Cinder volume type to use when creating temporary worker volumes. This option is only effective if the 'Migration Worker Boot From Volume' is set.
  * **migr_worker_use_config_drive (boolean)** - whether or not to use config drive to send metadata to the temporary disk copy/OSMorphing worker VMs in case Neutron metadata is not available
  * **port_reuse_policy (string, valid values are "keep_mac", "replace_mac" and "reuse_ports")** - sets what Coriolis should do if it encounters an existing Neutron port with a MAC address needed for the instance it is migrating/replicating. If set to 'keep_mac', Coriolis will delete the existing ports and recreate them with the same MAC address for the new VM. If set to "replace_mac", Coriolis will create new Neutron ports with different MAC addresses. If set to 'reuse_ports', Coriolis will try to reuse the existing ports it has found for the new migrated/replicated instance.
  * **list_all_destination_networks (boolean)** - whether or not to list all networks. By default, Coriolis will only list the networks that are in the same tenant as the one set in the Coriolis endpoint.
  * **volumes_are_zeroed  (boolean)** - whether unallocated blocks on Cinder target volumes contain zeros on creation. This is controlled by the "volume_clear" option in Cinder's configuration file
  * **set_dhcp (boolean)** - whether or not to reconfigure the internal network settings of each interface of the instance being migrated/replicated during the OSMorphing process to have the VM perform DHCP on first boot inside the new environment.
  * **preserve_fixed_ips (boolean)** - Whether or not to preserve the fixed IPs of the migrated instances' Neutron ports.
  * **server_group (string)** - Name or ID of the Nova Server Group to use when recreating the final VMs on OpenStack.
  * **use_floating_ip (boolean)** - Whether or not to attach a floating IP to the already migrated VM.
  * **floating_ip_pool (string)** - Name of the floating IP pool and an associated subnet(optional) to be used for the creation and attachment of floating IPs to the migrated VMs.
  * **instance_tags (object)** - Dictionary with arbitrary key-value pairs to set as tags on the migrated/replicated VMs.

Most destination environment parameters can also be found in the global configuration section, in which case they may be overridden on a per-migration/replica basis by setting them in the destination environment as well.
