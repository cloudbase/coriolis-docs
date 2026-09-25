---
title: "Coriolis Replica/Migration CLI parameters"
wp_id: 40128
---

# Coriolis Replica/Migration CLI parameters

## VMWare source environment parameters

The source environment parameters are a set of source-cloud-specific parameters that offer some extra options to the migration/replication process on a per-VM basis.

Below is a listing of the source environment parameters the VMWare plugin supports when migrating/replicating a VM from vSphere/ESXi:

### Example of source environment JSON to be passed to VMWAre plugin

```json
{"vixdisklib_compatibility_version": "6.7","automatically_enable_cbt": false}
```
  
  * **vixdisklib_compatibility_version** - The vSphere version for which to initialize vixDiskLib.
  * **automatically_enable_cbt** - Whether or not Coriolis should attempt to automatically enable CBT on the VM before Replication.



## OpenStack source environment parameters

The source environment parameters are a set of source-cloud-specific parameters that offer some extra options and configurability to the migration/replication process on a per-VM basis.

Below is a listing of the source environment parameters the OpenStack plugin supports when migrating/replicating a VM from OpenStack:

### Source environment for Openstack plugin

```json
{"custom_os_type_map": { "redhat": "linux" },"replica_export_mechanism": "swift_backups","swift_backups_options": {"volume_backups_container": "coriolis"},"coriolis_backups_options": {"export_interim_volume_type": "default-volume-type","export_image": "bionic","export_worker_use_config_drive": true,"export_network": "admin-net","export_flavor_name": "m1.small","export_worker_use_fip": true,"export_fip_pool_name": "floating-ip-net","export_worker_boot_from_volume": false,"export_worker_volume_type": "default-volume-type","export_worker_volume_size": 20,}}
```
  
  * **custom_os_type_map** - Custom mapping between the 'os_type' or 'os_distro' of Glance images on the source OpenStack. Mapping values must be one of the supported OS types in Coriolis.
  * **replica_export_mechanism** - Replica export mechanism to use. Available mechanisms are "swift_backups", "ceph_backups", "ceph_snapshots", "coriolis_backups"
  * **swift_backups_options** - Custom options for the "swift_backups" replica export mechanism
  * **volume_backups_container** - Name of the Swift container to store volume backups. Only available "swift_backups" is chosen as the replica mechanism.
  * **coriolis_backups_options** - Custom options for the "coriolis_backups" replica export mechanism.
  * **export_interim_volume_type** - Name of pre-existing Cinder volume type on the source to use for the temporary volumes Coriolis will be creating for exporting instance Glance images. In the case of secondary volumes, the storage type already used by the individual volumes will be used to avoid a cross-backend volume transfer while the clone is occurring.
  * **export_image** - Name or ID of a pre-existing Glance image of an Ubuntu 18.04 on the source OpenStack to be used for the temporary export worker VM on the source. The image must be available to the project/tenant provided in the Coriolis Endpoint. The image must have cloud-init installed and configured for first boot.
  * **export_worker_use_config_drive** - Whether or not to use config drive to send metadata to the temporary disk export worker VMs in case Neutron metadata is not available.
  * **export_network** - Name or ID of an existing Neutron network on the source OpenStack where to attach the Neutron port of the temporary disk export worker VMs. The selected network must either be in the same project/tenant as set in the Coriolis endpoint or be a shared/external network and thus available to said project. If 'export_worker_use_fip' is set to false, the Coriolis installation must be able to route to addresses allocated from this network.
  * **export_flavor_name** - Name of an existing Nova flavor which to boot the temporary disk export worker VMs. The flavor must be compatible with the selected 'export_image'.
  * **export_worker_use_fip** - Whether or not to allocate floating IPs from 'Export Floating IP Pool Name' for the temporary disk export worker VMs.
  * **export_fip_pool_name** - Name of an external Neutron network from which to allocate floating IPs for the temporary worker VMs Coriolis boots up during the disk export process. The Coriolis installation must be able to route to addresses allocated from this network.
  * **export_worker_boot_from_volume** - Whether or not to download the temporary disk export worker VM image to a Cinder volume and boot the worker from that.
  * **export_worker_volume_type** - Name of pre-existing Cinder volume type to be used for the root disk of temporary disk export VMs. Only effective in 'export_worker_boot_from_volume' is set.
  * **export_worker_volume_size** - The integer size (in GBs) of the Cinder volume to boot temporary worker VMs from. This option is only effective if 'export_worker_boot_from_volume' is set. If not set, Coriolis will use the disk size set the selected 'export_flavor_name'.



## OpenStack destination environment parameters

The destination environment parameters are a set of destination-cloud-specific parameters that offer some extra options and configurability to the migration/replication process on a per-VM basis.

Below is a listing of the destination environment parameters the OpenStack plugin supports when migrating/replicating a VM to OpenStack:

### Example of destination environment JSON to be passed to the OpenStack plugin

```json
{"network_map": {"source network name": "name or ID of existing Neutron network in destination OpenStack",},"storage_mappings": {"default": "cinder-volume-type-0","backend_mappings": [{"source": "datastor1", "destination": "cinder-volume-type-1"}],"disk_mappings": [{"disk_id": "<ID of disk>", "destination": "cinder-volume-type-2"}]},"hypervisor_type": "kvm","flavor_name": "m1.small","keypair_name": "new-key","delete_disks_on_vm_termination": false,"security_groups": ["name of existing secgroup on destination OpenStack", "and another one"],// parameters relating to the temporary worker instances, used in both migrations and replicas:"migr_image_map": {"linux": "Linux migration worker Image name/ID","windows": "63d8f1a4-3192-4edc-b113-0d099b4bc458"},"migr_network": "private","migr_worker_use_fip": true,"migr_fip_pool_name": "external_network/external_subnet","migr_flavor_name": "m1.small","migr_worker_boot_from_volume": true,"migr_worker_volume_size": 1,"migr_worker_volume_type": "cinder-voltype","list_all_destination_networks": true,"migr_worker_use_config_drive": true,// parameters relating to the migration process:"port_reuse_policy": "keep_mac","volumes_are_zeroed": true,"preserve_fixed_ips": true,"server_group": "name or ID of Nova server group","use_floating_ip": true,"floating_ip_pool": "external_network/external_subnet",// parameters relating to the OSMorphing process, used in both migrations and replica deployments:"set_dhcp": true,"instance_tags": {"tag1": "value1","tag2": "value2"}}
```
  
  * **network_map**  (string-string mapping) - a mapping between the names of networks on the source cloud and names or IDs of corresponding pre-existing networks on the destination Openstack. For each NIC of the instance on the source cloud, Coriolis will lookup the mapped network on the destination OpenStack and ensure the Neutron port corresponding to that NIC is attached to that Neutron network
  * **storage_mappings  **(object) - storage-related options such as how to map each disk or storage type on the source to Cinder volume types on OpenStack
  * **hypervisor_type**  (string) - the type of hypervisor the destination OpenStack features, supported options being "hyperv", "qemu" or "kvm"
  * **flavor_name**  (string) - name of pre-existing Nova flavor on the destination OpenStack for the migrated/replicated instance to be booted as
  * **keypair_name**  (string) - name of a pre-existing Nova keypair to be injected into the migrated/replicated instance on the destination cloud
  * **delete_disks_on_vm_termination**  (boolean) - whether or not to set the Cinder volumes as ephemeral (to be deleted when the VM is deleted) on the newly migrated/replicated instance on the destination OpenStack.
  * **security_groups  **(list of strings) - list of names or IDs of pre-existing security groups on the destination OpenStack to be applied to the migrated/replicated instance
  * **migr_image**  (string) - name or ID of the pre-existing Glance image to be used for the disk copy and/or OSMorphing workers. The name must be unique in the destination cloud. Overrides the settings in 'migr_image_map'
  * **migr_image_map**  (string-string mapping) - if migrating/replicating a heterogeneous workload with both Linux and Windows instances, separate image names/IDs will need to be provided for the temporary OSMorphing workers for each OS. Only accepted keys are 'linux' and 'windows'. Please review the "OSMorphing worker images" section for exact details on the requirements of the worker images for each OS type
  * **migr_network**  (string) - name of an existing Neutron network one the destination OpenStack to which to attach the Neutron port of the temporary disk copy/OSMorphing worker VMs
  * **migr_worker_use_fip  **(bool) - whether or not to allocate floating IP addresses from the "migr_fip_pool_name" for the temporary disk copy/OSMorphing worker VMs
  * **migr_fip_pool_name**  (string) - name of an existing Neutron network and an associated subnet(optional) on the destination OpenStack which serves as external and may have floating IPs allocated from it. These floating IPs will be associated to the temporary disk copy/OSMorphing worker VMs Coriolis will be creating during the migration/replication process
  * **migr_flavor_name  **(string) - name of an existing Nova flavor which to boot the temporary disk copy/OSMorphing worker VMs as
  * **migr_worker_boot_from_volume**  (boolean) - Whether or not to download the worker image to a Cinder volume and boot the worker from that.
  * **migr_worker_volume_size**  (integer) - The integer size (in GBs) of the Cinder volume to boot temporary worker VMs from. This option is only effective if 'migr_worker_boot_from_volume' is set. If not set, Coriolis will use the disk size set the selected 'migr_flavor_name'.
  * **migr_worker_volume_type**  (string) - Name of the pre-created Cinder volume type to use when creating temporary worker volumes. This option is only effective if 'Migration Worker Boot From Volume' is set.
  * **migr_worker_use_config_drive  **(boolean) - whether or not to use config drive to send metadata to the temporary disk copy/OSMorphing worker VMs in case Neutron metadata is not available
  * **port_reuse_policy  **(valid values are "keep_mac", "replace_mac" and "reuse_ports") - sets what Coriolis should do if it encounters an existing Neutron port with a MAC address needed for the instance it is migrating/replicating. If set to 'keep_mac', Coriolis will delete the existing ports and recreate them with the same MAC address for the new VM. If set to "replace_mac", Coriolis will create new Neutron ports with different MAC addresses. If set to 'reuse_ports', Coriolis will try to reuse the existing ports it has found for the new migrated/replicated instance.
  * **list_all_destination_networks**  (boolean) - whether or not to list all networks. By default, Coriolis will only list the networks which are in the same tenant as the one set in the Coriolis endpoint.
  * **volumes_are_zeroed**  (boolean) - whether unallocated blocks on Cinder target volumes contain zeros on creation. This is controlled by the "volume_clear" option in Cinder's configuration file
  * **set_dhcp**  (boolean) - whether or not to reconfigure the internal network settings of each interface of the instance being migrated/replicated during the OSMorphing process to have the VM perform DHCP on first boot inside the new environment.
  * **preserve_fixed_ips**  (boolean) - Whether or not to preserve the fixed IPs of the migrated instances' Neutron ports.
  * **server_group**  (string) - Name or ID of the Nova Server Group to use when recreating the final VMs on OpenStack.
  * **use_floating_ip**  (boolean) - Whether or not to attach a floating IP to the already migrated VM.
  * **floating_ip_pool**  (string) - Name of the floating IP pool and an associated subnet(optional) to be used for the creation and attachment of floating IPs to the migrated VMs.
  * **instance_tags**  (object) - Dictionary with arbitrary key-value pairs to set as tags on the migrated/replicated VMs.



## AWS source environment parameters

The source environment parameters are a set of source-cloud-specific parameters which offer some extra options and configurability to the migration/replication process on a per-VM basis.

Below is a listing of the destination environment parameters the AWS plugin supports when migrating/replicating a VM from AWS:

### Example of source environment JSON to be passed to the AWS plugin

```json
{"migr_image_map": {"linux": "ami-50946030", "windows": "ami-50946031"},"worker_instance_type": "t2.medium","shutdown_migrated_instance": false}
```
  
  * **migr_image_map**  (string-string mapping) - a mapping specifying the ID of an AMI to use for temporary worker VMs. Supported keys are linux and windows.
  * **worker_instance_type**  (string) - name of the instance type to use for the temporary worker VMs. Default is t2.medium.
  * **shutdown_migrated_instance**  (string) - Indicate whether or not to shut the VM down during the migration process in order to ensure data consitency.



## Hyper-V source environment parameters

The source environment parameters are a set of source-cloud-specific parameters which offer some extra options and configurability to the migration/replication process on a per-VM basis.

### Example of source environment JSON to be passed to the Hyper-V plugin

```json
{"fallback_to_crash_consistent_snapshots": true,"verify_rct_server": false}
```
  
  * **fallback_to_crash_consistent_snapshots**  (string) - Use crash-consistent snapshots if Hyper-V enablement is not installed in the guest VM
  * **verify_rct_server**  (string) - Verify the SSL certificate for RCT service. Set to No if using a self-signed certificate.



## Azure source environment parameters

The source environment parameters are a set of destination-cloud-specific parameters that offer some extra options and configurability to the migration/replication process on a per-VM basis.

Below is a listing of the destination environment parameters the Azure plugin supports when migrating/replicating a VM from Azure:

### Example of source environment JSON to be passed to the Azure plugin

```json
{"location": "westus","resource_group": "coriolis-testgroup","export_worker_size": "Standard_A1","export_worker_image": {"publisher": "Canonical","offer": "UbuntuServer","sku": "16.04.0-LTS","version": "latest"},// Below options are for Blob storage-based scenarios:"storage_account_name": "storage-account","storage_container_name": "coriolis"}
```
  
  * **location**  (string) - the Azure location where to search for the VM to migrate/replicate (ex: westus, eastus, etc…)
  * **resource_group**  (string) - the name of the resource group in which the VMs to migrate/replicate are in
  * **export_worker_size**  (string) - the size to use for the temporary disk replication worker VM
  * **export_worker_image**  (object) - the parameters of the image to use for the temporary worker VM
  * **storage_account_name**  (string) - If configured to Migrate/Replicate to Blob storage, the name of an Azure Blob storage account must be provided. The Storage account must reside within the selected 'Resource Group'
  * **storage_container_name**  (string) - If configured to Migrate/Replicate to Blob storage, the name of an Azure storage container must be provided. The container must reside within the Azure storage account provided using 'Storage Account Name'. The container will be automatically created during the Migration/Replication process if it doesn't exist.



## Azure destination environment parameters

The destination environment parameters are a set of destination-cloud-specific parameters that offer some extra options and configurability to the migration/replication process on a per-VM basis.

Below is a listing of the destination environment parameters the Azure plugin supports when migrating/replicating a VM to Azure:

### Example of destination environment JSON to be passed to the Azure plugin

```json
{"location": "westus","resource_group": "Migrations","network_map":{"source network name": "azure-network-name/test-subnet-name"},"storage_map": {"default": "Standard_LRS","backend_mappings": [{"source": "source_backend", "destination": "Premium_LRS"}],"disk_mappings": [{"disk_id": "source_disk_id", "destination": "Premium_SSD"}]},"vm_size": "Standard_D1",// parameters relating to the temporary worker instances, used in both migrations and replicas:"worker_size": "Standard_D1","linux_migr_image": {"publisher": "Canonical","offer": "UbuntuServer","sku": "16.04.0-LTS","version": "latest"},"windows_migr_image": {"publisher": "MicrosoftWindowsServer","offer": "WindowsServer","sku": "2016-Datacenter-Server-Core","version": "latest"},// Below options are for Blob storage-based scenarios:"storage_account_name": "storage-account","storage_container_name": "coriolis","preserve_nic_ips": false}
```
  
  * **location**  (string) - the Azure location to which to migrate/replicate (ex: westus, eastus, etc…)
  * **resource_group**  (string) - the name of a pre-existing resource group in which to migrate/replicate to and must exist in the specified location
  * **network_map**  (string-string mapping) - a mapping between the names of networks on the source cloud and a corresponding pre-existing network in the configured resource_group on Azure as well as its subnet name separated by a slash (ex: "testing-network/default" for the "default" subnet of the "testing-network" Azure network) For each NIC of the instance on the source cloud, Coriolis will lookup the mapped network on Azure, and ensure the NIC corresponding to each interface on the source is attached to the right Azure network
  * **storage_map**  (string-string mapping) - a mapping between identifiers of storage backends on the source cloud and the corresponding Azure storage account types. For each disk of the instance on the source cloud, Coriolis will lookup the Azure storage account type on Azure
  * **storage_account_name**  (string) - Name of the Azure storage account to create VHD Page blobs on
  * **storage_container_name**  (string) - Name of the Azure storage container to create VHD Page blobs on
  * **vm_size**  (string) - the size of the new VM on Azure, please ensure that the size allows for the number of disks the instance had on the source to be attached to the VM
  * **worker_size**  (string) - the size of the temporary replication/OSMorphing workers to use during the migration/replication process
  * **linux_migr_image**  (object) - the parameters of a Linux Azure image to use during replication/Linux OSMorphing, default is the 16.04 image exemplified in the listing above
  * **windows_migr_image**  (object) - the parameters of a Windows Azure image to use during Windows OSMorphing, default is the Server 2016 image exemplified in the listing above
  * **preserve_nic_ips**  (boolean) - Whether or not to set the same IP address on migrated VM NICs if the mapped network/subnet combination includes the IP address(es) the NICs had on the source within their IP range.



## OCI destination environment parameters

The destination environment parameters are a set of key-value pairs (some may have nested key value pairs of their own), that allow you to overwrite default values set in the provider. For example, you may configure the OCI provider to behave in a certain way, but for some migrations of replicas, you would like to overwrite that behaviour with a different set of settings.

Below is a listing of the destination environment parameters the OCI plugin supports when migrating/replicating a VM to OCI:

### Example of destination environment JSON to be passed to the OCI plugin

```json
{"network_map": {"source_network_1": {"id": "<ID of destination OCI subnet>","security_groups": ["network_secgroup_id_1", ...]},"storage_mapping": {"default": "emulated","backend_mappings": [{"source": "datastor1", "destination": "iscsi"}],"disk_mappings": [{"disk_id": "<ID of disk>", "destination": "paravirtualized"}]},"use_pv_mode": true,"availability_domain": "<availability_domain>","compartment": "<compartment_ID>","vcn_compartment": "<compartment_ID>","set_public_ip": true,"migr_subnet_id": "<migrsubnet>","migr_image_map": {"linux": "<linux_image_id>","windows": "<windows image ID>"}"migr_shape_name": "VM.Standard1.2","shape_name": "VM.Standard2.2"}
```
  
  * **availability_domain**  (string) - ID of the availability domain on OCI 
  * **network_map**  (string-object mapping) - a mapping between the names of networks on the source cloud and a corresponding pre-existing network on OCI, in addition to an optional list of security groups
  * **storage_mappings**  (string-object mapping) - a mapping between source storage backend names and OCI volume attachment types (not compatible with root disks).
  * **use_pv_mode**  (boolean) - Whether or not to use paravirtualized mode for instances running on BIOS firmware.
  * **migr_image_map**  (string-string mapping) - a mapping between os types (accepted keys being either 'linux' or 'windows') and image IDs on OCI
  * **migr_subnet_id**  (string) - ID of the subnet where worker VMs will have nics attached
  * **migr_shape_name**  (string) - Name of the OCI shape to be used for the worker instance.
  * **compartment**  (string) - name of the OCI compartment to boot the use for the Migration/Replica 
  * **vcn_compartment**  (string) - This option allows the selection of VCNs from a different compartment
  * **set_public_ip  **(boolean) - whether or not to set a public IP address for the migrated VM
  * **shape_name**  (string) - Name of the OCI shape used when creating the final migrated instance.



## OCI-C source environment parameters

The source environment parameters are a set of source-cloud-specific parameters which offer some extra options and configurability to the migration/replication process on a per-VM basis.

Below is a listing of the source environment parameters the OCI-C plugin supports when migrating/replicating a VM from OCI:

### Example of source environment JSON to be passed to the OCI-C plugin

```json
{"export_image_name": "/oracle/public/OL_7.2_UEKR4_x86_64","export_img_username": "cloud-user","export_shape_name": "oc3","export_root_disk_size": 20}
```
  
  * **export_image_name  **(string) - name of a Linux image on OCI-C to use for the temporary VMs which will be exporting disk data from OCI-C
  * **export_img_username**  (string) - username to use when connection to the temporary disk copy worker
  * **export_shape_name**  (string) - name of the shape to use for the temporary VMs which will be exporting disk data from OCI-C
  * **export_root_disk_size**  (integer) - size (in GBs) of the root disk of temporary worker VMs. This is only affected by the selected image as the Coriolis Replica export process from OCI bears no extra storage requirements



## OCI-C destination environment parameters

The destination environment parameters are a set of destination-cloud-specific parameters which offer some extra options and configurability to the migration/replication process on a per-VM basis.

Below is a listing of the destination environment parameters the OCI-C plugin supports when migrating/replicating a VM to OCI-C:

### Example of destination environment JSON to be passed to the OCI-C plugin

```json
{"network_map": {"source network name": "name of an existing IP network on destination OPC"},"storage_mappings": {"default": ""/oracle/public/storage/default"","backend_mappings": [{"source": "datastor1", "destination": "/oracle/public/storage/default"}],"disk_mappings": [{"disk_id": "<ID of disk>", "destination": "/oracle/public/storage/latency"}]},"migr_image_map": {"linux": "/oracle/public/OL_7.2_UEKR4_x86_64",// NOTE: syntax for custom images:"windows": "/Compute-a488347/user@mail.com/Windows_2012_R2"},"migr_shape_name": "oc3","shape_name": "oc3","default_volume_pool": "/oracle/public/storage/default","keypair_name": "key1","set_public_ip": true}
```
  
  * **network_map**  (string-object mapping) - a mapping between the names of networks on the source cloud and names of corresponding pre-existing IP networks on the destination OPC
  * **storage_mappings**  (string-object mapping) - storage-related options such as how to map each disk or storage type on the source to OPC storage pools.
  * **migr_image_map**  (string-string mapping) - if migrating/replicating a heterogeneous workload with both Linux and Windows instances, separate image names/IDs will need to be provided for the temporary OSMorphing workers for each OS. Only accepted keys are 'linux' and 'windows'. Please review the "OSMorphing worker images" section for exact details on the requirements of the worker images for each OS type
  * **migr_shape_name**  (string) - name of the shape to use for temporary OCI-C worker VMs
  * **shape_name**  (string) - name of the shape to use for migrated VM(s) on OCI-C (can be omitted, in which case Coriolis will pick the minimum viable shape in your stead)
  * **default_volume_pool**  (string) - name of the default OPC storage pool if none is selected for a source disk or backend.
  * **keypair_name**  (string) - name of the pre-created keypair of the account to use when creating the final migrated instance.
  * **set_public_ip**  (boolean) - Whether or not the migrated instance will have a public IP attached to its first vNIC.



## OVM source environment parameters

The source environment parameters are a set of source-cloud-specific parameters that offer some extra options and configurability to the migration/replication process on a per-VM basis.

Below is a listing of the source environment parameters the OVM plugin supports when migrating/replicating a VM from OVM:

### Example of source environment JSON to be passed to the OVM plugin

```json
{"repository_name": "<name of the repository to create temporary worker VMs in>","export_template_name": "<name of Linux template to use for the temporary disk export VMs>","export_template_username": "<username to the temporary VM template>","export_template_password": "<password to the temporary VM template>","virtual_disk_clone_types": "THIN_CLONE"}
```
  
  * **repository_name**  (string) - name of the repository to create temporary worker VMs in
  * **export_template_name**  (string) - name of Linux template to use for the temporary disk export VMs. The template must be configured with a NIC attached to a network that is both reach-able from the Coriolis installation and has a DHCP server available to allocate a new IP to the temporary VM.
  * **export_template_username**  (string) - username for the temporary VM template
  * **export_template_password**  (string) - password for the temporary VM template
  * **virtual_disk_clone_type**  (string) - What cloning method to use when cloning the source disks to be migrated. The 'Thin Clone' option is recommended, though it may not be supported by all OVM storage repository types.



## OVM destination environment parameters

The destination environment parameters are a set of destination-cloud-specific parameters that offer some extra options and configurability to the migration/replication process on a per-VM basis.

Below is a listing of the destination environment parameters the OVM plugin supports when migrating/replicating a VM to OVM:

### Example of destination environment JSON to be passed to the OVM plugin

```json
{"network_map": {"source network name": "name or ID of existing network on destination OVM",},"storage_mappings": {"default": "default_repository","backend_mappings": [{"source": "datastor1", "destination": "Main"}],"disk_mappings": [{"disk_id": "<ID of disk>", "destination": "Local"}]},"server_pool_name": "<name of server pool>","repository_name": "<name of storage repository>","migr_template_name_map": {"linux": "OracleLinux7_template","windows": "Windows2012R2_template"},"migr_template_username_map": { "linux": "root", "windows": "Administrator" },"migr_template_password_map": { "linux": "<root password>", "windows": "<Administrator password" },"leave_migrated_vm_off": false,"os_label": "coriolis-migrated","virtual_disk_clone_type": "THIN_CLONE"}
```
  
  * **network_map**  (string-string mapping) - a mapping between the names of networks on the source cloud and names or of corresponding pre-existing networks on the destination OVM
  * **storage_mappings**  (string-object mapping) - storage-related options such as how to map each disk or storage type on the source to repositories on OVM
  * **server_pool_name**  (string) - name of the server pool to create migrated/replicated VMs, as well as temporary worker VMs
  * **repository_name**  (string) - name of the storage repository to store migrated/replicated VMs in
  * **migr_template_map**  (string-string mapping) - if migrating/replicating a heterogeneous workload with both Linux and Windows instances, separate template names will need to be provided for the temporary OSMorphing workers for each OS. Only accepted keys are 'linux' and 'windows'. Please review the "OSMorphing worker images" section for exact details on the requirements of the worker images for each OS type
  * **migr_template_username_map**  (string) - Mapping between OS types and the pre-created usernames of the corresponding template set in the 'migr_template_name_map' to be used for the temporary worker VMs.
  * **migr_template_password_map**  (string) - Mapping between OS types and the pre-set password of the corresponding template set in the 'migr_template_name_map' to be used for the temporary worker VMs.
  * **leave_migrated_vm_off**  (boolean) - whether or not to just create VMs but skip powering them on
  * **os_label**  (string) - Label for the new OS on OVM
  * **virtual_disk_clone_type**  (string) - What cloning method to use when creating migrated disks. The 'Thin Clone' option is recommended, though it may not be supported by all OVM storage repository types.


