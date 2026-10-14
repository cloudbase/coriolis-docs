---
title: "Coriolis Disk Verification"
---

# Coriolis Disk Verification

Disk verification checks that the data written on the destination matches the data read from the source. When it is enabled, Coriolis computes a checksum of each source disk during transfer execution and compares it with a checksum of the corresponding destination disk.

The option is disabled by default. Set **Verify Disk Integrity** (`verify_disk_integrity`) on the source environment of the Replica or Migration to enable it. There is no matching option on the destination.

**Source platforms** are the platforms that implement this option and compute the source checksum:

  * VMware
  * OpenStack
  * Nutanix

**Target platforms** are the destinations that can compute the checksum Coriolis compares against that source checksum. Any supported source can be verified to any of these targets:

  * Amazon Web Services (AWS)
  * Microsoft Azure / AzureStack
  * Oracle Cloud Infrastructure (OCI)
  * OpenStack
  * StackIT
  * VMware
  * oVirt
  * Oracle Linux Virtualization Manager
  * Proxmox
  * KubeVirt/Harvester
  * MicroCloud (LXD)
  * SUSE Linux KVM (Libvirt)
  * SUSE Linux KVM (SAP HANA)

Other source or destination platforms are not currently supported for disk verification, but might be added in future releases.

The destination checksum is computed by the HTTPS backup writer. On the target platforms above, **Data Transfer Mechanism** defaults to **HTTPS**. See the destination platform page for where that setting is exposed.

## How it works

At a high level, a transfer with disk verification enabled follows this sequence:

  1. Create a **Replica** or **Migration** from a supported source platform to a supported target platform.
  2. Enable **Verify Disk Integrity** on the source environment options.
  3. Keep the destination **Data Transfer Mechanism** set to **HTTPS**.
  4. During Transfer Execution, Coriolis reads each source disk, writes the disk data to the destination, and computes a checksum of the source disk.
  5. After the disk data is written, Coriolis asks the destination writer for a checksum of the same disk and compares the two values.
  6. A matching checksum is recorded in the transfer logs. A mismatch fails the transfer execution.

```{note}
For source options, see [**VMware as a source cloud**](../platforms/vmware-as-a-source-cloud.md#example-of-source-environment-json-to-be-passed-to-the-vmware-plugin), [**OpenStack as a source cloud**](../platforms/openstack-as-a-source-cloud.md#openstack-source-environment-parameters), and [**Nutanix as a source cloud**](../platforms/nutanix-as-a-source-cloud.md#nutanix-source-environment-parameters).
```

## Enabling disk verification

Typical flow from the Coriolis Dashboard (or CLI):

  1. Select a supported **source** and **destination** endpoint from the lists above.
  2. Create a new Replica or Migration.
  3. On the source environment options, set **Verify Disk Integrity** to **true**.
  4. On the destination, set **Data Transfer Mechanism** to **HTTPS** when the destination exposes that option.
  5. For an OpenStack source, set **Replica Export Mechanism** to **Coriolis Backups**. Disk verification is ignored for the Swift and Ceph export mechanisms.
  6. Run the transfer. After the execution, the logs report either a verified checksum or a checksum mismatch.

## Limitations and requirements

  * **Disabled by default:** `verify_disk_integrity` is **false** until it is set on the source environment of the transfer.
  * **HTTPS data transfer required for comparison:** the destination checksum is computed by the HTTPS backup writer. When the destination uses **SSH**, or when the destination writer cannot return a checksum, Coriolis skips the comparison and the execution continues.
  * **Checksum mismatch fails the execution:** if both checksums are computed and they differ, or if the algorithms do not match, the transfer execution fails for that disk.
  * **Full-disk checksum on every execution:** verification checksums the whole disk, including on incremental Replica executions. Changed-block replication still writes only the changed ranges.
  * **OpenStack source mechanism:** on OpenStack, verification applies only when **Replica Export Mechanism** is **Coriolis Backups**.
  * **VMware source reads the full disk:** with verification enabled, Coriolis reads every sector of the VMware disk in order to compute the SHA-256 checksum, then writes the changed ranges to the destination.
