---
title: "AWS as a destination cloud"
wp_id: 41166
---

# AWS as a destination cloud

### Migrating (CMaaS) to AWS

Migrations to AWS operate in the same way Replicas do, and thus entail the same requirements and steps described below.

### Replicating (DRaaS) to AWS

#### Replica executions:

#### Steps performed by Coriolis

  1. if this is the first replica execution for the VM, create empty EBS volumes on the destination cloud, each matching the specifications of a disk the VM had on the source If this is a later replica execution, the previously-created EBS volumes are used
  2. if this is the first replica execution of the VM, create a new live-snapshot the disks of the VM on the source cloud (handled by whatever source cloud plugin we are using) If this is a later replica execution, create a new live snapshot based on the one from the last successful replica execution
  3. create a temporary Linux worker VM (the "disk copy worker") on AWS cloud and attach the EBSvolumes from step 1 to it
  4. read the contents of the snapshot created at step 2 via the source platform's snapshot/backup APIs (handled by whatever source cloud plugin we are using), transferring the written chunks to the temporary VM created in step 3, which then writes the chunks at the appropriate index/offset of the disks created at step 1
  5. once the contents of all the disks have been synced to the EBS volumes created during step 1, detach the volumes and delete the disk copy worker created at step 3

#### Replica deployments:

#### Steps performed by Coriolis

  1. [optional] create snapshots of the replicated EBS volumes on the destination cloud in order to be able to roll back any changes. By default, new volumes are created from these snapshots, leaving the original replica volumes intact for future replica executions
  2. depending on the OS of the VM whose replica is being deployed, boot a temporary worker VM ("the OSMorphing worker") with the same OS type on the destination cloud, and attach the EBS volumes from step 1 to it
  3. perform the "OSMorphing process", where Coriolis commands the OSMorphing worker created during step 2 to scan all attached disks for the OS installation of the VM we are migrating, mount and perform the steps needed to prepare the installation for the new platform (ex: uninstalling the VMWare guest tools if migrating away from VMWare)
  4. detach the EBS volumes created at step 1 from the OSMorphing worker created at step 2 and delete the temporary worker VM 
  5. create and boot the migrated VM on the destination cloud with the specifications of the original VM on the source cloud (which have been noted during the particular replica execution we are deploying), creating and attaching any necessary network interfaces and EBS volumes.

### Configuration Options

Below is a listing of the configuration section needed when migrating from AWS:

#### Configuration options for AWS as a destination

[![](_static/images/ASW-destination.jpg)](https://i0.wp.com/cloudbase.it/wp-content/uploads/2022/04/ASW-destination.jpg?ssl=1)

```ini
[aws_migration_provider]
# Whether or not to attempt to retain the IP addresses the VM had on the
# source. This requires that the mapped subnets on AWS include the respective
# IP address(es) in their ranges.
# Default is False.
retain_source_ip = false

# The OS migration image map to use. This mapping will be used to spin up
# the OS morphing worker needed to morph the OS being migrated.
migr_image_map = linux: ami-50946030, windows: ami-50946031

# A map similar with migr_image_map, where we specify the username for each OS
# image. On EC2, various linux distributions, have different usernames.
# Default is 'ubuntu' for Linux and 'coriolis' for Windows.
migr_image_username_map = linux: ubuntu, windows: coriolis

# The storage type to default to for the disks of Migrated VMs if an explicit
# storage mapping was not supplied during the Replica/Migration creation.
# Default is 'standard'
default_storage_type = standard

# Default AD to use when creating resources for Migrated/Replicated VMs.
# Must be in the same region as specified within the connection info.
# availability_zone = az1

# Default instance type used for final migrated instances.
# instance_type = t2.medium
```

### OSMorphing steps taken when migrating to AWS

For HVM guests, Coriolis will take the following OSMorphing steps as part of the migration process to AWS:

Linux:

  * installing cloud-init

Windows:

  * installing AWS Windows agent(s)

### OSMorphing and temporary worker VM images

During the disk export and OSMorphing processes, Coriolis will create temporary VMs in order to facilitate the Migration process.

The images do **NOT** require any special Coriolis agent running in them and can be images already available in the AWS marketplace, granted the following requirements:

#### Linux

  * needs to be Ubuntu 18.04 or later (using official Canonical 18.04 images is recommended)
  * AMI must have only one disk (regardless if instance storage or EBS-backed)
  * cloud-init must be installed and running in order for the initial setup/login and key injection to succeed

#### Windows

  * for OSMorphing, must be of at least the same version as the guest of the VM being migrated
  * the Windows image should have the AWS Windows agent tools configured for the first boot

### AWS destination environment parameters

The destination environment parameters are a set of destination-cloud-specific parameters which offer some extra options and configurability to the migration/replication process on a per-VM basis.

Below is a listing of the destination environment parameters the AWS plugin supports when migrating/replicating a VM to AWS:****

#### Example of destination environment JSON to be passed to the AWS plugin

```json
{
	"network_map": {
		"source network name": "ID of existing VPC."
	},
	"storage_mappings": {
		"default": "standard",
		"backend_mappings": [{"source": "datastor1", "destination": "gp2"}],
		"disk_mappings": [{"disk_id": "<ID of disk>", "destination": "io1"}]
	},
	"migr_image_map": {"linux": "ami-50946030", "windows": "ami-50946031"},
	"worker_instance_type": "t2.medium",
	"instance_type": "t2.medium",
	"availability_zone": "az1",
	"retain_source_ip": true
}
```

Each parameter represents:

  * **network_map** - a mapping between the names of networks on the source cloud and names or IDs of corresponding pre-existing networks on AWS. For each NIC of the instance on the source cloud, Coriolis will lookup the mapped network on the destination and ensure the NIC will be attached to the mapped network
  * **storage_mappings** - storage-related options such as how to map each disk or storage type on the source to storage types on AWS
  * **migr_image_map** - a mapping specifying the ID of an AMI to use for temporary worker VMs. Supported keys are Linux and windows.
  * **worker_instance_type** - name of the instance type to use for the temporary worker VMs. Default is t2.medium.
  * **instance_type** - name of the instance type to be used for the final VM. If not set, Coriolis will automatically pick the smallest instance size which satisfies the VM's requirements
  * **availability_zone** -  AD to use when creating resources for Migrated/Replicated VMs. Must be in the same region as specified within the connection info.
  * **retain_source_ip** - whether or not to attempt to retain the IP addresses the VM had on the source. This requires that the mapped subnets on AWS include the respective IP address(es) in their ranges.

### Troubleshooting

For more information regarding Coriolis Troubleshooting, check the **[Troubleshooting page](https://cloudbase.it/coriolis-troubleshooting)**.
