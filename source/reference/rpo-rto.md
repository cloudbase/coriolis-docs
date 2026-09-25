---
title: "Coriolis Recovery Point Objective &#038; Recovery Time Objective"
wp_id: 39009
---

# Coriolis Recovery Point Objective &#038; Recovery Time Objective

## Recovery Point Objective  
  
**RPO** (Recovery Point Objective) refers to the amount of data at risk. It is determined by the amount of time between data protection events and reflects the amount of data that potentially could be lost during disaster recovery. The metric is an indication of the amount of data at risk of being lost. 

The recovery point objective (RPO) is the age of files that must be recovered from backup storage for normal operations to resume if a computer, system, or network goes down as a result of a hardware, program, or communications failure. The RPO is expressed backward in time (that is, into the past) from the instant at which the failure occurs, and can be specified in seconds, minutes, hours, or days. It is an important consideration in disaster recovery planning (DRP)

### Factors involved in RPO calculations

The RPO of a Coriolis Replica is determined by the last snapshot of the VM on the source platform which was successfully synced on the destination during a Coriolis Replica Execution (i.e. sync between the disks of the VM in the source to disks on the destination platform)

For keeping RPO to an absolute minimum, it is recommended that a Coriolis Replica always have a Replica Execution running for it. 

The overall efficiency of a singular Replica Execution directly affects RPO by preventing a Replica to be synced at a higher frequency.

The following factors external to Coriolis directly affect a Replica's execution efficiency:

  1. The speed with which the source/destination platforms spin up the temporary resources Coriolis needs.  
Examples of temporary resources Coriolis uses include temporary networks/subnets, VMs and associated resources (disks, NICs, public IPs, etc…), disk snapshots, and more  
Note that in all cases Coriolis only uses these resources during the actual syncing process itself, and they are cleaned up afterward.
  2. The speed at which the source platform can compute the differencing chunks from the last successful sync.  
Some source platforms offer in-built mechanisms (ex: CBT on VMWare, Ceph on Openstack, or RCT on Hyper-V) which allow for querying of diff chunks to be done in constant time (O(1))  
However, source platforms which do not offer such disk diff-ing mechanisms will mean that Coriolis will be performing the disk chunk differencing itself, which is a linear-time operation (O(n))
  3. The amount of differential data from the last successful sync which needs to be transferred over.  
Executing a Replica more often leads to an obvious reduction in the number of changed disk blocks.
  4. The disk IOPS on the source/destination platforms.  
This affects the speed at which the differential data can be read from the source and written to the destination.
  5. The available bandwidth between Coriolis and the source/destination platforms.  
This determines the time it takes to transfer the differential data from the source platform to Coriolis, and Coriolis to the destination platform.
  6. The speed at which the source/destination platforms can tear down the temporary resources mentioned in point 1)



## Recovery Time Objective

**RTO** (Recovery Time Objective) is related to downtime. The metric refers to the amount of time it takes to recover from a data loss event and how long it takes to return to service. RTO refers then to the amount of time the system's data is unavailable or inaccessible preventing normal service. 

**Coriolis** provides replication to storage in the DR site, that being the only resource consumed and eliminating the compute, memory, and other costs of a running workload. Only at the time of fail-over or cut-over - switching to the DR site, Coriolis will provision the workload with all the required compute, memory, network resources, and attach the disks it has been syncing.

### Factors involved in RTO calculations

In the event of a disaster striking on the source platform, Coriolis can be asked to create a Replica Deployment from a Replica which has been previously executed successfully at least once.

In the case of Replicating between platforms backed by different hypervisors, a Replica deployment also includes the OSMorphing process, where a temporary VM is created in order to "adapt" the image of the previously-synced VM to the destination (by installing drivers and integration tools for the new platform, applying any necessary configuration changes, and so on)

As such, RTO is equal to the time a Coriolis Replica Deployment takes until it reaches the stage of booting the final VM on the destination platform.

The following factors external to Coriolis effect a Replica Deployment's total runtime:

  1. The speed with which the source/destination platforms spin up any temporary resources Coriolis may need, as well as start the recovered VM on the destination platform.  
Examples of temporary resources Coriolis uses include temporary networks/subnets, the VMs used for OSMorphing and associated resources (disks, NICs, public IPs, etc…), disk snapshots, and more  
Note that in all cases Coriolis only uses these resources during the actual syncing process itself, and they are cleaned up afterward.
  2. The time required to clone the Replica disks (should Coriolis be configured to clone the disks it is been syncing to) 
  3. If OSMorphing is required, then there is added overhead from the OSMount/OSMorphing processes, whose complexity depends on the guest OS installed in the VM being Replicated


