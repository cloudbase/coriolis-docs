---
title: "oVirt as a source cloud"
wp_id: 43569
---

# oVirt as a source cloud

**NOTE: Both OLVM and RHEV are considered oVirt platforms in the Coriolis documentation pages, and therefore all notes about the oVirt platform will apply to both the OLVM and RHEV providers.**

### Migrating (CMaaS) from oVirt

Migrations from oVirt operate in the same way Replicas do and thus entail the same requirements and steps described below.

### Replicating (DRaaS) from oVirt

In the process of replicating from oVirt, Coriolis will use Incremental Backups to live-snapshot the disks of the VM and fetch their contents. Thus, the following requirements must be met:

  * the oVirt must have Incremental Backups available to the user whose credentials were given to Coriolis
  * the oVirt user whose credentials are given to Coriolis must be able to access VM information and image transfer data, and it should be able to create backups and snapshots on the VM
  * the VM to be replicated has all the storage elements hosted on Incremental-compatible storage domains (network and LUN-based domains are NOT supported)  
Coriolis can automatically enable the incremental backup for a virtual disk on OLVM / SUSE Virtualization - oVirt-based. The technical reference for this functionality can be found here: [Incremental Backup | oVirt](https://www.ovirt.org/develop/incremental-backup-guide/incremental-backup-guide.html#disk-format)
  * the VM to be replicated must have Incremental Backups enabled on all of its disks
  * Coriolis can optionally be configured to enable Incremental Backups on the VM automatically



Consider reviewing the general steps recommended before creating and executing a replica for an instance from oVirt.

**Steps performed by Coriolis:**

  1. read the instance configuration on the source oVirt (hardware information, disks, etc.)
  2. if configured to enable Incremental Backups itself, Coriolis will make sure to snapshot the VM in case it has RAW formatted disks (in order to provide a CoW layer on top of it, so it can be incrementally backed up), and will enable incremental backups on all disks
  3. creates crash-consistent backups of the instance. If this is not the first replica execution, incremental backups are performed
  4. fetches backup data via the ImageIO API



After the above steps are completed, the written blocks of the backup will be transferred and written to disks on the destination via the destination cloud plugin.

**NOTE:** During a Replica/Migration process from oVirt, if the option to keep the static IP address for the machine is selected, QEMU Guest Agent must be available, and the machine must have been powered on during at least one of the replica syncs.

**IMPORTANT!** Any 3rd party backup software that creates VM backups will interfere with Coriolis' replication process, as in the process of a VM backup, all the disks are locked, thus only one VM backup can exist at a time.

### oVirt source environment parameters

[![](_static/images/image-2.png)](https://i0.wp.com/cloudbase.it/wp-content/uploads/2025/05/image-2.png?ssl=1)

The source environment parameters are a set of source-cloud-specific parameters that offer some extra options to the migration/replication process on a per-VM basis.

Below is a listing of the source environment parameters the oVirt plugin supports when migrating/replicating a VM from oVirt:

#### Example of source environment JSON to be passed to oVirt plugin

```json
{
    "automatically_enable_incremental_backups": true
}
```
  
  * **automatically_enable_incremental_backups** (boolean) - Whether or not Coriolis should attempt to automatically enable incremental backups on the VM before Replication.



### OSMorphing steps taken when migrating/replicating from oVirt

The following notable steps will be performed as part of the OSMorphing process when migrating/replicating an instance away from oVirt:

**Linux:**

  * if not needed on the destination, the following packages will be uninstalled: cloud-init, qemu-guest-agent (or its legacy counterpart, ovirt-guest-agent)



For more information regarding the Coriolis Worker template, please check the **[Coriolis Temporary Migraiton Worker](https://cloudbase.it/coriolis-temporary-migration-worker)** page.

### Configuration Options

Below is a listing of the configuration section needed when migrating from oVirt:

**Configuration options for oVirt as a source**

```json
[ovirt_migration_provider]
# Whether or not Coriolis should attempt to automatically enable incremental
# backups on the VM before data replication.
auto_enable_incremental_backups = false
```
