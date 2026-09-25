---
title: "OpenStack known issues"
wp_id: 39003
---

# OpenStack known issues

### **On some Cinder-volume backends, the lifecycle of volumes created from snapshots is linked to that of the parent snapshot.**

This leads to an issue where Coriolis is unable to delete temporary disk snapshots, resulting in residual snapshots.

The following warning message can be seen within Cinder's logs when this occurs:

**Cinder Snapshot deletion error**

```text
2019-07-15 11:29:13.834 42138 ERROR cinder.volume.manager [req-6f579f0c-8cc5-46b0-af2d-44ef91a4891e a713228be21c49b5bf65c5b3693f71a9 56bb931fb1374b8183f63add82855619 - bcf26315012b4044886bc9e628d6004a bcf26315012b4044886bc9e628d6004a] Delete snapshot failed, due to snapshot busy.: cinder.exception.SnapshotIsBusy: deleting snapshot snapshot-7f5ce196-dfe0-49e7-b721-423d55ead6b9 that has dependent volumes
```
  
Should this happen, Coriolis will also log the event with the following message:

**Coriolis Snapshot deletion failure warning**

```text
2019-07-15 11:29:13.834 42138 DEBUG: Cinder volume snapshot '<ID>' became 'available' while waiting for its deletion. This may be the behavior of the Cinder driver being used, so no further deletion attempts will be made.
```
  
Workaround:

On Ceph-based Cinders, the following Cinder-volume configuration option will allow for snapshots to be cleaned up regardless of child volumes:

The `**rbd_flatten_volume_from_snapshot**` flag will make new Cinder volumes independent of the snapshot. As documented [here](http://docs.ceph.com/docs/master/man/8/rbd/?highlight=format#commands), the **flatten** action will do the following:

  Copy all shared blocks from the parent snapshot and make the child independent of the parent, severing the link between parent snap and child. 

### **Coriolis** **metadata not available over the network**

While migrating from VMWare to OpenStack if no metadata for the networks and storage is available in Coriolis, error messages will be received when starting the process: **" No networks were found"** and **" No storage backends were found" **

To have it fixed, use config drive to send metadata to the temporary disk copy/OSMorphing worker VMs in case Neutron metadata is not available.

The parameter for the above example is **migr_worker_use_config_drive** , and it is part of the OpenStack destination environment parameters.

Please refer to the JSON file example mentioned under Openstack destination environment parameters on **[OpenStack main documentation page.](https://cloudbase.it/openstack-as-a-destination-cloud/)**
