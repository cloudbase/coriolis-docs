---
title: "Coriolis Openstack Ceph integration"
wp_id: 41363
---

# Coriolis Openstack Ceph integration

Ceph is an open-source software-defined storage solution designed to address modern enterprises' block, file, and object storage needs.

**Ceph-based snapshots** are a recommended option if supported by your platform configuration, as in comparison with the **Coriolis Backups** , where Coriolis spawns temporary resources to perform the disk replication, or **Swift Backups** where Coriolis creates Cinder backups for every replicated VM and then fetches the objects from Swift.

**Ceph-based snapshots** using either option of **Ceph Backups** of **Ceph Snapshots** will perform the disk replication by fetching the chunks located on Openstack's Ceph following the snapshot creation.

### Coriolis Ceph integration prerequisites

  * Coriolis can use Ceph storage only if the deployed Coriolis Appliance will have access to the Ceph monitor hosts.
  * Coriolis must be provided with **Ceph-monitor** IP/hostname and credentials, where the easiest way is to provide a ceph.conf from one of the** 'cinder-volume' service host** found under **/etc/ceph/ceph.conf**
  * for Ceph snapshots usage, Coriolis only needs read-only access to Ceph
  * for Ceph backups usage, Coriolis will need snapshot-creation-permissions as it will have to perform an interim snapshot for running the diff.

NOTE: In a real-world situation when '**cinder-backups** ' are used with Ceph, most likely '**cinder-volume** ' will be available on Ceph, so in this situation, the option of **Ceph Snapshots** is recommended instead of **Ceph Backups**. As long as the environment used supports the feature, **Ceph Snapshots** will be preferred over **Ceph Backups** as it will be less time-consuming in order to have the disk cloning complete and require fewer permissions.

### Using Ceph with Coriolis

Ceph can be used in Coriolis Replica/Migration tasks as backend storage for OpenStack, but this will require specifying its connection requirements upon adding the Openstack Endpoint.

[![](_static/images/ceph-endpoint.jpg)](https://i0.wp.com/cloudbase.it/wp-content/uploads/2022/06/ceph-endpoint.jpg?ssl=1)

In order to have the Ceph options available when adding the OpenStack Endpoint, the "**Advanced** " configuration mode must be used, and "**Show Ceph Options** " must be enabled from the current menu.

### Ceph Options

The Ceph configuration file and credentials for a user with read-only access to the Ceph pool used by Cinder backups/snapshots must be provided. Coriolis must be able to connect to the source OpenStack’s Ceph RADOS cluster by being able to reach at least one Ceph-monitor host. For the easiest setup possible, simply using the same credentials used by the Cinder service(s) will work.

**Ceph Configuration File - **Contents of the ceph.conf configuration file containing the list of monitor hosts to connect to. Ideally, this should be the same ceph.conf as used by the Cinder volume/backup service(s). The ‘[mon] keyring’ path options are irrelevant, as the keyring which is passed through the ‘Ceph Keyring File’ option will be used.

**Ceph Keyring File -** Ceph keyring file with the access key(s) for the user given as the ‘Ceph Username’ for the cluster described in the given ‘Ceph Configuration File’. Ideally, this should be the same keyring file as used by the Cinder service(s). The default path for the**Keyring file** is **/etc/ceph/$cluster.$name.keyring** found on Ceph units.

**Ceph Username - **Ceph user to use when connecting to the source OpenStack’s Ceph cluster. The user must have read-only access to the Ceph pool(s) used by the Cinder-backup and Cinder-volume service(s). Ideally, this should be the same user that the Cinder services themselves are using

**Ceph Clustername - **Name of the Ceph cluster in which Cinder volume snapshots/backups are stored

**Ceph Pool Name - **Name of the Ceph pool in which Cinder volume snapshots/backups are stored

**Ceph Connection Timeout - **Integer number of seconds to wait on Ceph connections before timing out.

## Ceph Source Options

Using **Ceph Storage** when running a Replica/Migration tasks from a source OpenStack endpoint, will require using either **Ceph Backups** or **Ceph Snapshots** as **Replica Export Mechanism** for the **Source Options**.

### Ceph Backups

Selecting **Ceph Backups** will offer the option of **' Ceph Backups Diff Hash Algorithm'** which will give the option of choosing the algorithm in Python's hashlib to use for hashing disk chunks to compare them. If the option is unset, the diff will be compared directly instead of hashing them. Ceph Backups requires that the Coriolis-Worker component have network access to the source Openstack's Ceph through librbd/librados.

[![](_static/images/ceph-backups.jpg)](https://i0.wp.com/cloudbase.it/wp-content/uploads/2022/06/ceph-backups.jpg?ssl=1)

### Ceph Snapshots

Selecting **Ceph Snapshots** will not offer any further options. Using Ceph Snapshots, Coriolis will create Cinder snapshots for each disk and fetch the disk chunks from the source OpenStack's Ceph.

Ceph Snapshots, as Ceph Backups require that the Coriolis-Worker component have network access to the source Openstack's Ceph through librbd/librados.

[![](_static/images/ceph-snapshots.jpg)](https://i0.wp.com/cloudbase.it/wp-content/uploads/2022/06/ceph-snapshots.jpg?ssl=1)
