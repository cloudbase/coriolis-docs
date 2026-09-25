---
title: "Coriolis Troubleshooting"
wp_id: 40662
---

# Coriolis Troubleshooting

This page outlines different situations that a user might encounter when using Coriolis.

### No matching migration image type found for OS type 'windows'

When Replicating/Migrating a **Windows VM** , the above error can be seen if a Windows template has not been specified for the Temporary migration worker. in the Target options menu, under the Advanced screen, both **Linux and Windows templates**  have to be specified. This is required as **Disk cloning**  is performed using the Linux template and **OSMorphing**  is performed using the Windows template.

* * *

### Troubleshooting OSMorphing on the Docker-based Coriolis appliance

The OSMorphing process is the procedure undergone by the guest OS being migrated to ensure it will boot on the destination platform.

OSMorphing always occurs on the destination platform, where Coriolis will create a temporary VM (either Linux or Windows, depending on the guest OS being migrated) to perform the OSMorphing steps on the already-synced disks.

Considering that OSMorphing errors may be a direct result of an incompatibility between the specific setup of the guest OS and Coriolis or the destination platform, they are relatively more common during a Migration, and the only concrete way to debug the issues would be to login to the temporary OSMorphing VM Coriolis is controlling to see exactly what Coriolis sees.

#### Configuration

There is a dedicated 'debug_os_morphing_errors' flag in the '[conductor]' section of /etc/coriolis/coriolis.conf:

#### debug_os_morphing_errors example

```ini
# NOTE: this option must be appended within the '[conductor]' section:
[conductor]
debug_os_morphing_errors = false
```

If set to 'true', the Coriolis Conductor will skip performing the cleanup steps on the temporary resources on the destination platform and will log out the connection info for the temporary VM in the Coriolis-conductor.log.

NOTE please remember to run a `docker restart Coriolis-conductor` for any changes to `debug_os_morphing_errors` to take effect.

* * *

### Accessing the Coriolis temporary worker VM

Below is a sample of the connection info for the temporary worker VM as seen in `Coriolis-conductor.log`:

#### debug_os_morphing_errors log output example

```text
# NOTE: the private keys for the worker VMs may have the passphrase
# configured in coriolis.conf set to them:
$ grep "temp_keypair_password" /etc/coriolis/coriolis.conf
temp_keypair_password = qJDxLBbdFCvRKP3J8qTxcvuh
# NOTE: the IP and connection info the temp VM will be logged in the Conductor logs:
$ grep "have been cancelled to allow for OSMorphing debugging." /var/log/coriolis/coriolis-conductor.log
2019-10-16 21:53:53.007 WARNING coriolis.conductor.rpc.server [req-05f6b9fa-6d78-45fc-9bee-a1e4de05ac49 ] All subtasks for Migration 'ece4b02d-4ab8-405c-b33e-c36c63a20993' have been cancelled to allow for OSMorphing debugging. The connection info for the worker VM is: {'ip': '138.91.73.150', 'port': 22, 'username': 'coriolis', 'password': None, 'pkey': '<pkey_data>'}
```

WARNING if 'debug_os_morphing_errors' is set, the lifecycle of the temporary OSMorphing worker VM and all of its associated resources (disks, NICs, public IPs, etc…) will no longer be managed by Coriolis. **All the temporary OSMorphing resources on the destination platform will need to be manually cleaned up after investigations have concluded.**

After logging into the temp VM, the following things to check may be of importance:

  * if all of the disks of the migrated VM are visible in the temp VM
  * if all of the disks are mountable within the temp VM (reviewing `**dmesg**` output for new mounts is recommended)
  * if the order of the disks is the same as the order reported by the destination platform's UI/API
  * if the disks are using any non-standard partitioning layouts/formats (ex: BitLocker/dm-crypt, Dynamic Disks on Windows, etc…)
  * if Coriolis properly identified and mounted the guest OS being migrated (there should be some non-root mount points on the worker)
  * try to run the `chroot` command attempted by Coriolis which leads to the OSMorphing error (can be seen in Coriolis' error logs)

* * *

### AWS - 500 Server Error: Internal Server Error for url: https://IP:5566/api/v1/dev/xvdf/acquire

Some AWS instance types use SSD-backing storage, and although the guest OS internally has the disks named `/dev/nvmeX`, the AWS API returns the disk labels as `/dev/xvdf`.

To overcome this, if the error is encountered when using AWS as a Destination Cloud, consider changing the **Instance Type** for the Migration Mapping used for the Coriolis Temporary worker.

For example, if the error is seen when using t3.medium, try to use c5.large instead, or other types available, depending on the region.

* * *

### Change the admin password

The following command can be used to change the password for the admin user:

```bash
 $ openstack user set --password-prompt admin 
```

Once done, consider setting also the corresponding password in **/etc/kolla/admin-openrc.sh** :

```bash
 $ export OS_PASSWORD=YourNewPassword 
```

For multi-tenant configurations, the following command can be used to change the password for any user:

```bash
 $ openstack user set --name admin --domain Default --project admin --project-domain Default --password "new password" admin 
```

### Migrated guest VM fails to boot with a message that root volume or partition not found

A guest VM with the root partition using LABEL paths in /etc/fstab**** might fail to migrate under Coriolis.

Please refer to the steps to verify and prepare on the source VM before running a migration task, as detailed here: [Preparing a VM for migration/replication](../guides/preparing-a-vm-for-migration-replication.md#recommended-storage-steps-for-linux-vms)

Once /etc/fstab has been updated on the source VM to use filesystem UUIDs, create a new migration task or an incremental replica.

* * *

### Windows Server 2012/2012R2 guest OS support

Microsoft Windows Server 2012 and 2012R2 reached End-Of-Life support in October 2023. If upgrading to a newer version before migration is not possible, migrating these versions is subject to best effort.

Coriolis will still handle OS Morphing for these versions, one user consideration is that the older stable such as **virtIO drivers 0.1.189** must be used.

* * *

### Set a static IP for the Coriolis appliance

The Coriolis virtual appliance system is based on the Ubuntu Server, so a typical netplan configuration will apply.

From the console menu, go to the option to edit the network settings.

#vim /etc/netplan/50-cloud-init.yaml

You can set a static IP in this format:

> network:
>   version: 2
>   ethernets:
>     enp0s3:
>       dhcp4: no
>       addresses: [192.168.0.123/24]
>       gateway4: 192.168.1.1
>       nameservers:
>         addresses: [8.8.8.8,8.8.4.4]

Once the configuration file is saved, exit the Coriolis console edit session by typing "exit", which will prompt to restart the network services in order to apply the configuration change.

### VM migrated to OLVM is not able to start

After a successful migration of a VM to OLVM that has TPM module enabled, Coriolis may fail to power it on. If the ovirt-engine logs mention that swtpm binary could not be executed, it could be because it is blocked by SELinux enforced on the ovirt engine server.

To overcome this, log onto the ovirt server, and run the following command, so that SELinux context changes for the ovirt engine service:

```bash
semodule -i swtpm_local.pp
```

This usually happens on OLVM versions older than 4.5. Newer versions may have this issue resolved. After setting this, Coriolis should be able to power on migrated machines when finalizing the migration process. The previously-migrated machines will also be able to be powered on.

## Troubleshooting LUKS-encrypted migrations

### " No key available with this passphrase"

**Command "sudo cryptsetup luksOpen -disable-keyring -key-file /tmp/coriolis_sdb3.key /dev/sdb3 coriolis_sdb3" failed on host '10.8.29.225:22' with exit code: 2 stdout: No key available with this passphrase.**

Make sure you have provided the correct passphrase in Coriolis, and that you re-synced the transfer in case it was previously executed _before_ the new keyslot was added on the source VM.

* * *

### VM never reboots itself after first boot

An issue might have occurred during the first VM boot: either the LUKS device did not auto-unlock (and thus, the first boot script could not launch), or an error occurred during the first boot script. If the LUKS device did not auto-unlock, it may be possible to unlock it manually using the migration passphrase, but this issue should still be reported to your Coriolis provider in order to be properly fixed. Check the VM's own console / serial log for that specific boot attempt and report this issue, along with the console log.

* * *

### VM reboots but doesn 't come back up

If the VM was rebooted, it means that the LUKS first boot script has completed, meaning that the TPM2 keyslot has been updated and the migration passphrase keyslot has been removed (and thus, the passphrase is no longer usable to unlock the LUKS devices). However, on reboot, the LUKS device could not be auto-unlocked using the attached TPM2 device.

The only useful diagnostic here is the VM's own console / serial log for that specific boot attempt. Look for the guest's boot-time LUKS / TPM2 unlock step (**systemd-cryptsetup** or **clevis**) failing, e.g. because the vTPM state wasn't preserved across the reboot on that destination platform. Report this along with the console log.

* * *

### " The VM has encrypted disks (…), which require a TPM device"

**The VM has encrypted disks ( 'encrypted_disks_passphrase' given), which require a TPM device. The add_tpm_device config option is False.**

This is not a first-boot failure, it's a pre-flight validation check, and it runs when a deployment is executed, before the destination VM is created.

Just creating the transfer via the API / WebUI, without executing a deployment, does not trigger this check by itself. It means you supplied an Encrypted Disks Passphrase, but the destination provider's **add_tpm_device** config option is disabled for the provider involved (see "Make sure the destination platform has a TPM device enabled" above). This check exists specifically so you find out _before_ VM creation happens, rather than after first boot fails to re-enroll the new TPM device.

Fix: set the proper configuration options in coriolis-worker's **coriolis.conf** file (as shown in the section "Make sure the destination platform has a TPM device enabled") and restart the **coriolis-worker** service. Then, execute a new deployment.

* * *

### " \<device\> is LUKS-encrypted, but no passphrase is provided"

The deployment / migration fails outright with this error if Coriolis detects a LUKS container on a source disk but no **Encrypted Disks Passphrase** was set on the transfer's target options. Add the migration passphrase (see Prerequisites above) and re-run.

* * *

### " No initramfs tool found in OS at '\<path\>'"

Raised when neither **update-initramfs** nor **dracut** can be found inside the guest OS being migrated. This means either the guest distro isn't one of the supported families, or its filesystem wasn't fully mounted / detected before this check ran. This is not something you can fix from the client side, report the source OS distro / version to your Coriolis provider.

* * *

### " No /etc/crypttab entries matched LUKS UUIDs in '\<path\>'; cannot configure initramfs auto-unlock"

Coriolis matches LUKS devices to **/etc/crypttab** entries by UUID (**UUID= …** or **/dev/disk/by-uuid/ …**). If the source VM's **/etc/crypttab** references the encrypted device some other way (e.g. a raw **/dev/sdaX** path, an LVM path, or a missing entry entirely), Coriolis cannot determine which keyfile / options to wire up and fails instead of guessing. Fix the source VM's **/etc/crypttab** to reference the device by UUID before migrating, or report the case to your Coriolis provider if UUID-based crypttab entries should be supported but aren't being recognized.
