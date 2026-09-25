---
title: "VMWare Plugin Known Issues"
wp_id: 39345
---

# VMWare Plugin Known Issues

### Backup fails when the source Endpoint is set for the VCenter

**Error message** : _"The ESXi host performing the CBT export refused connection. The host is chosen automatically by Center, so please ensure that the Coriolis deployment can dial TCP/902 on all the ESXi hosts of a vSphere, and that DNS name resolution firewalls are setup to facilitate this.Alternatively, try connecting Coriolis directly to the specific ESXi host which is running the VM(s) to be migrated by creating a Coriolis endpoint using the DNS name/IP address of the host itself."_

If the above error message occurs in a multi ESXi hosts situation where vCenter is used in the Coriolis endpoint configuration, we recommend adding as Coriolis Endpoint the ESXi hosts IP or Hostname rather than the vCenter'. This way, we are making sure that Coriolis will send the commands directly to the ESXi host.

The error message will point to port 443 which vCenter will use to communicate with the ESXi hosts, but Coriolis will not be able to confirm the connection.

In the case where the **ESXi Host** is connected to vCenter using its **hostname** and the **Coriolis Endpoint** is created using vCenter details, the **vixdisklib** will look to resolve the hostnames.

If the above situation applies, following one of the two steps below will allow Coriolis to correctly communicate with the ESXi host:

  * add ESXi Hosts mappings in **/etc/hosts** file on Coriolis Appliance 
    * restart **systemd-hostnamed** service, which is a system service that may be used to change the system's hostname and related machine metadata from user programs.
  * add in **/etc/resolv.conf** on Coriolis Appliance a secondary DNS server that can resolve the Hostname of the ESXi servers. 
    * The Coriolis Appliance network must have access to the DNS server IP used.

This can be avoided if the **Coriolis Endpoint** is created using the **IP** of the **ESXi host**.

* * *

### Replica/Migration fails due to corrupt CBT data

**Error message:** "Error caused by file /vmfs/volumes/xxxxxx/xxxxx.vmdk".

If the above message occurs, it is an internal VMWare type of error that causes CBT data to be corrupted and thus, unexportable. This is a VMware software issue, and Coriolis is merely passing further to the user the error it receives from the hypervisor.

The following steps have been observed to solve this error. Further assistance can be found on the CBT Reset **[documentation page](https://cloudbase.it/vmware-vm-cbt-reset-guide)** if the problem remains.

  * disable and then re-enable **CBT** on the**VM** (while the VM is powered off).

  * create a Coriolis **endpoint** using the **IP/hostname** of the **ESXi host** the **VM** is currently running on instead of the IP/hostname of the vCenter server. This will force Coriolis to export from that host instead of a random host within the cluster. 

  * **move** the **VM** using **vMotion** to a different **ESXi host** , and retry with the above step to also change Coriolis's endpoint to the new ESXi host.

* * *

### "Error caused by file </path/to/vmdk/file>" Error

#### Description:

This error occurs as Coriolis calls the QueryDiskChangedAreas method of a VM while performing a CBT-based Migration/Replica.

The error message should be formatted with the exact path (on the VMWare datastore) of the VMDK causing issues.

Possible causes are speculated to be:

  * a power failure and hard shutdown were performed on the VM
  * a power failure during a Storage vMotion operation on the VM, in which case existing CBT data may be cleared completely
  * VMs that have been upgraded from hardware version <= 5 may have CBT data reset, leading to the issue
  * in vSphere < 5.0, reverting a VM to an earlier snapshot may cause the issue, in which case disabling and re-enabling is recommended

Further details can be found at the following links:

  * manifestation of an error on VMs with pre-existing snapshots: <https://kb.vmware.com/s/article/1033816>
  * manifestation of error, the apparent cause is an I/O error on a disk used as a vmfs datastore: <https://communities.vmware.com/thread/588337>
  * manifestation of error during a cross-datastore move using vMotion due to block sizes on two datastores do not match: <https://kb.vmware.com/s/article/2009097>
  * manifestation of error for a VM which has been reverted to a previous snapshot on VMWare < 5.0: <https://kb.vmware.com/s/article/1021607>

#### Troubleshooting:

Double-check that the file is indeed a VMDK file correctly located on the datastore.

It is also worth asking the VMWare platform admin to check the logs of both the vCenter server as well as the ESXi host the VM being replicated is running on.

NOTE: the ESXi host from which the export is performed is **not** necessarily the same one the VM is on. If exporting from a vSphere, any ESXi host in the cluster could hypothetically do the export

#### Workarounds:

There is no clear solution, but using vMotion to migrate the VM to another ESXi host and Datastore might bypass the issue.

Suggested workarounds (in order of likelihood):

  * **Perform a CBT reset for the instance. Instructions are available on the CBT Reset page below:**
    * CBT Reset **[documentation page](https://cloudbase.it/vmware-vm-cbt-reset-guide)**.
  * using vMotion to move the VM to a different ESXi host
  * using vMotion to move the VM to a different datastore
  * manually delete the CTK data off of the datastore with the VM powered off (there should be a file named "*-ctk.vmdk" within the same directory as the VMDK file in the error report)
  * as a last resort, one may export an OVF of the VM, and re-import it (making sure to select another host or datastore)

* * *

### Windows updates and incremental replica runs

Due to a bug in VMware 6.x (such as VMware ESXi 6.5 and 6.7), running Replica syncs after a Windows guest OS system update might lead to inconsistent data on the destination platform.

This is a bug in VMware when interacting with the Microsoft Volume Shadow Copy Service (VSS) and the Windows system files that get updated during the installation of Windows Updates. The problem is no longer observed in ESXi 7.0, and given that the VMware 6.x series are End of Life, the recommendation is to move to ESXi 7.0 or newer.

This applies to all supported Windows Server editions and does not affect the running guest OS on the source.

VMware 6.x series is EOL and should not be used in production.

* * *

### Migration job enters a Cancelled state

**Error message** : This task was user-cancelled. Additional cancellation info from worker service: "Task was canceled."

Please follow the VMware plugin documentation for the proper setup and configuration to ensure a smooth integration with your VMware environment.

The above error usually occurs when Coriolis is in one of the following situations:

  * Coriolis appliance is not able to resolve the FQDN hostnames of *all* the ESXi nodes.
  * Coriolis appliance cannot reach *all* the ESXi nodes over TCP port 902.

Due to VMware vSphere functionality, snapshot creation/read events can be executed through *any* of the ESXi hosts, and not bound to the ESXi host on which the VM is running. Thus, you should ensure that all ESXi hosts have a proper FQDN / network connectivity that the Coriolis appliance can use.

After the above has been fixed, you can recreate the migration task.

In case the error remains, you can check the vixdisklib log file located under the **/var/log/coriolis/vmware-root** folder on the Coriolis appliance. This is a VMware log file from the connection to the VMware environment and contains verbose messaging.

* * *

### Migration job fails with "A specified parameter was not correct: deviceKey"

This usually occurs when Change Block Tracking (CBT) is not enabled for the VM being backed up. CBT is required for Coriolis to be able to perform a live snapshot of the running source VM.

To fix this issue,**** perform a CBT reset for the source VM. Instructions are available on the [CBT Reset page](https://cloudbase.it/vmware-vm-cbt-reset-guide) or by following VMware's official documentation.

* * *

### Unable to take quiesced snapshot of a Windows Server virtual machine

Creating a quiesced snapshot (or running a backup job with quiescing) can fail due to a conflict between the Windows VSS and the VMware Tools Snapshot provider.

The VMware recommendation in such cases is to:

Step 1. Do not use the "VMWare Snapshot Provider" service by disabling it, or uninstalling that component from VMware Tools.

Step 2. Set the Microsoft VSS service to Automatic startup.

Once these steps are carried out on the source VM, a new migration job can be created in Coriolis.

* * *

### T _he guest ID of the VM is: otherGuest "_

The following migration error can be observed:

_"The OS type of VM 'Datacenter/Discovered virtual machine/VMNAME' ('other') is either not supported or unrecognized by Coriolis or the version of pyVmomi which Coriolis is currently using. The guest ID of the VM is: otherGuest"_

This occurs when the source VM on the VMware side has a generic or incorrect guest OS. Coriolis requires an accurate value matching the source VM guest OS for the scope of migration.

To resolve this issue, please edit the VM .vmx configuration file and modify the **guestOS** field to a correct value. This can be for example "oraclelinux8-64." for an Oracle Linux 8 VM. Please refer to the VMware documentation for the proper fields.
