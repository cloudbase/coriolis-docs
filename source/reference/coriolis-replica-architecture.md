---
title: "Coriolis Replica/Migration Architecture"
wp_id: 38724
---

# Coriolis Replica/Migration Architecture

This document describes the two broader feature sets offered by Coriolis Transfers, and namely:  
  
  * Disaster Recovery as a Service (**DRaaS**) through **Coriolis Replicas**
  * Cloud Migration as a Service (**CMaaS**) through **Coriolis Migrations**



Both modes of operation use the same underlying Coriolis mechanisms to achieve their goals. This document will focus on Coriolis Replicas, as they represent a more granular separation of Coriolis' methods than Coriolis Migrations.

### Replicas (DRaaS)

**Scenario addressed** : continuous background sync of a running workload's storage from a source cloud directly to a destination cloud ("executing a Replica"), and the ability to create a new VM on the destination cloud using the previously-synced storage elements should disaster strike on the source ("deploying a Replica")

#### Architectural overview

[![](_static/images/Diagram0.png)](https://i0.wp.com/cloudbase.it/wp-content/uploads/2020/05/Diagram0.png?ssl=1)

#### Replica executions:

The replica execution process consists of a single sync between the workload's storage on the source cloud to storage elements on the destination cloud.

#### Inputs

  * non-privileged user credentials for both the source and destination platforms
  * [optional] a mechanism available on the source platform to live-snapshot/live-backup a running instance's storage (ex: CBT on VMWare, or Cinder-backup if replicating a VM from OpenStack). The system may optionally support guest filesystem quiescing. For the exact requirements of replica a source/destination platform, please review the documentation for that particular platform.
  * a name/identifier of the existing instance on the source cloud which needs migrating. The instance may need explicit enabling of the live-snapshot mechanism (ex: enabling CBT on all disks if performing DRaaS for a VM from VMWare)
  * a set of cloud-specific parameters relating to the destination cloud (referred to as the "destination environment" in Coriolis' API) which offer some extra options and configurability to the replication process (ex: a 'network_map' parameter for selecting the right network for each of the migrated instance's NICs on the destination cloud)



If no disk diff-ing/export mechanism is available on the source platform, Coriolis can make use of source-side temporary VM to perform the diff operation itself. This process is considerably less efficient than native implementations like CBT/RCT, as time scales with the sizes of disks involved, as well as the read throughput possible within the source environment.

#### Result

  * first replica execution for an instance: new disks on the destination cloud with the exact state of the original instance's disks during the last live-snapshot (the original instance may have a slightly more advanced state due to it having been running while the replica process has been executing in the background)
  * later replica executions for the same instance: only the differences between the previous live-snapshot and a new one are applied to the disks on the destination cloud
  * a new VM may be booted on the destination platform at any time from the last successfully synced storage by going through the "replica deployment" process detailed separately in the next section



#### Steps performed by Coriolis

  1. read the configuration of the instance on the source cloud (CPU, RAM, attached NICs, disks, etc…)
  2. if this is the first replica execution for the VM, create empty disks on the destination cloud, each matching the specifications of a disk the VM had on the source.  
If this is a later replica execution, the previously-created disks are used (with necessary updates such as resizing, reordering and so on applied to them)
  3. [configurable] turn off the source VM before doing the sync to ensure consistency
  4. if this is the first replica execution of the VM, create a new live-snapshot of the disks of the VM on the source cloud.  
If this is a later replica execution, create a new live-snapshot based on the one from the last successful replica execution (also referred to as an "incremental snapshot" on some source platforms)
  5. [optional] if the source platform does not offer a mechanism to query disk areas that have changed between live-snapshots, Coriolis will deploy a temporary Linux worker VM (the "disk replication worker") on the source platform.  
This temporary VM will then run Coriolis' disk Replication engine in order to compute the disk change areas between syncs itself.
  6. create a temporary Linux worker VM (the "disk writer worker") on the destination cloud and attach the disks from step 2 to it
  7. read the contents of the snapshot created at step 4 (either via the source platform's snapshot/backup APIs, or the disk replication worker from step 5), transferring the written chunks to the disk writer VM created in step 6, which then writes the chunks at the appropriate index/offset of the disks created at step 2
  8. once the contents of all the disks have been synced, detach the disks created at step 2 and delete the disk writer worker VM created at step 6, as well as the disk replication worker from step 5.



[![](_static/images/Diagram1.png)](https://i0.wp.com/cloudbase.it/wp-content/uploads/2020/05/Diagram1.png?ssl=1)

#### Observations

  * during a replica execution, the VM on the source is left running and whatever workload it was hosting will be unaffected by the process
  * changes to the VM's configuration on the source cloud (increased compute resources, new disks/NICs were attached, size increases of existing disks, etc…) are properly handled by Coriolis. The state changes are registered during the immediately following replica execution.
  * Coriolis can ensure filesystem consistency for a replica if the backup system supports guest filesystem quiescing via an integration agent (ex: the VMWare guest tools when snapshotting an instance with CBT enabled on VMware)
  * later replica executions are much faster than the initial one, and thus the difference in the state from the running instance on the source and the disks on the destination (also known as recovery point objective, or RPO) is much smaller the more often a replica is executed for the particular VM
  * in case of brief network interruptions during data replication, Coriolis will attempt to automatically recover and resume the transfer. Extended network outages or other infrastructure issues will cause the replication job to stop, allowing the operator to run the replication job once the platforms are in a healthy status.



The above describes the steps Coriolis takes in general terms. If you would like to know exactly how the replica execution process works for a particular platform, please review the documentation for that specific platform

#### Replica deployments:

#### Inputs

  * an existing Coriolis replica with one or more executions successfully completed
  * the source platform may suffer a complete outage and be unreachable while a replica deployment process is being run



**Result:** a new instance on the destination cloud booted with the state of the instance during the last successful replica execution

#### Steps performed by Coriolis

  1. [optional] create snapshots and clones-from-snapshots of the replicated disks on the destination cloud in order to be able to rollback any changes. By default, new disks are created from these snapshots, leaving the original replica disks intact for future replica executions
  2. depending on the OS of the VM whose replica is being deployed, boot a temporary worker VM (the "OSMorphing worker") with the same OS type on the destination cloud, and attach the disks from step 1 to it
  3. perform the "OSMorphing process", where Coriolis commands the OSMorphing worker created at step 2 to scan all attached disks for the OS installation of the VM we are migrating, mount and perform the steps needed to prepare the installation for the new platform (ex: uninstalling the VMWare guest tools and installing VirtIO drivers if deploying a replica of a Windows VM from vSphere to a KVM-based OpenStack)
  4. detach the disks created at step 1 from the OSMorphing worker created at step 2 and delete the temporary worker VM 
  5. create and boot the migrated VM on the destination cloud with the specifications of the original VM on the source cloud (which have been noted by Coriolis during the latest replica execution which has completed successfully), creating and attaching any necessary NICs and disks.



[![](_static/images/Diagram2.1.png)](https://i0.wp.com/cloudbase.it/wp-content/uploads/2020/05/Diagram2.1.png?ssl=1)

#### Observations

  * the resulting VM's state is not identical to the VM on the source, but merely identical to the source VM's state during the last replica execution (which, considering replicas are user-scheduled, should be as often as possible to have closest possible state the source VM had when the platform went down)
  * should the source and destination platforms be identical (ex: if replicating between two KVM-based OpenStack systems), the OSMorphing process (steps 2 through 4) is redundant and may be skipped entirely



The above describes the steps Coriolis takes in general terms. If you would like to know exactly how the replica deployment process works for a particular platform, please review the documentation for that specific platform

### Migrations (CMaaS)

**Scenario addressed** : "lift-and-shift" type migrations, where the goal is to move the storage of an existing instance on the source cloud to the destination cloud and boot a new instance with identical settings 

#### Inputs

  * [optional] a mechanism available on the source platform to live-snapshot/live-backup a running instance's storage (ex: CBT on VMWare, or Cinder-backup if replicating a VM from OpenStack). The system may optionally support guest filesystem quiescing. For the exact requirements of replica a source/destination platform, please review the documentation for that particular platform.
  * a name/identifier of the existing instance on the source cloud which needs migrating. The instance may need explicit enabling of the live-snapshot mechanism (ex: enabling CBT on all disks if performing DRaaS for a VM from VMWare)
  * a set of cloud-specific parameters relating to the destination cloud (referred to as the "destination environment" in Coriolis' API) which offer some extra options and configurability to the replication process (ex: a 'network_map' parameter for selecting the right network for each of the migrated instance's NICs on the destination cloud)



#### Steps performed by Coriolis

  * the steps performed by Coriolis during a one-off Migration are the same as performing a Replica execution and deployment
  * the number of sync executions is configurable so as to minimize RPO (the default number is 2, the maximum is 10)
  * Coriolis can optionally be instructed to power off the source VM before the final incremental execution, ensuring the consistency of the guest OS



**Result:** a migrated instance on the destination cloud with the same storage elements as the original instance and booted with the same configuration

#### Observations

  * the images used by Coriolis for the temporary worker VMs (the disk copy and OSMorphing workers) can be standard cloud images already available in the destination cloud. In most cases, should the environment support user-specified metadata, they may have to have the cloud initialization tool particular to the platform in question installed (ex: cloud-init for Linux workers if migrating to OpenStack). Please review the documentation of the particular destination cloud you are migrating to for the exact specifications of the worker images
  * at step 6, only the written chunks of a disk are transferred to the destination cloud, making the process as fast as possible for VMs with large but mostly unused disk space
  * should the source and destination platforms be identical (ex: if migrating between two KVM-based OpenStack systems), the OSMorphing process is redundant and may be skipped entirely



The above describes the steps Coriolis takes in general terms. If you would like to know exactly how the migration export/import process works for a particular platform, please review the documentation for that specific platform.
