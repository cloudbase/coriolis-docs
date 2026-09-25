---
title: "oVirt Coriolis Plugin"
wp_id: 40789
---

# oVirt Coriolis Plugin

**NOTE: Both OLVM and RHEV are considered oVirt platforms in the Coriolis documentation pages and therefore all notes about the oVirt platform will apply to both the OLVM and RHEV providers.**

**Coriolis** integrates the platform Plugin on the Appliance itself, this way there is no need for agents to be deployed on platforms to establish the communication between the platform and the Coriolis components. Using this type of architecture, Coriolis guarantees the connection to the supported platform set up to be used as either Source or Destination, as long as the requirements are met.

**Coriolis** connects to the oVirt management interface REST API to collect information about the VMs and to handle backup creation and data replication.

NOTE! The QEMU Guest Agent must be installed and updated to the latest version available on the VMs, as well as on the Coriolis temporary workers.

Coriolis supports environments running the oVirt engine starting from version 4.3 and is compatible with newer releases up to 4.5.4.

### oVirt as a source cloud

For more information on using oVirt as a **source cloud** for Replica/Migration, please check the **[oVirt as a source cloud](https://cloudbase.it/ovirt-as-a-source-cloud)** page.

### oVirt as a destination cloud

For more information on using oVirt as a **destination cloud** for Replica/Migration, please check the **[oVirt as a destination cloud](https://cloudbase.it/oracle-linux-virtualization-manager-as-a-destination-cloud/) **page.

### Deployment requirements and supported oVirt engine versions

The Coriolis worker components require network access to the oVirt engine host's API endpoint. (usually HTTPS/443)

For Incremental Backups-enabled Coriolis Migrations, as well as Coriolis Replicas (DSaaS), the Coriolis worker components will need TCP/54322 network access to the ImageIO service.

If performing Coriolis Replicas (DRaaS), the VMs being replicated must have their storage hosted on an Incremental Backup-compatible storage domain (network and lun-based storage types are not supported), and should ideally be of qcow2 format. If the replicated disks are in raw format, Coriolis can attempt to snapshot the disks in order to add a qcow layer on top of them, thus enabling incremental backup capabilities.

### oVirt platform specifics

Supported Actions: | Migration Destination - Replica Destination| Comments  
---|---|---  
Plugin identifier| **olvm** (or **rhev**)| Identifies the plugin. Used for the **- provider** CLI parameter  
Credentials needed| Username and password| Necessary credentials to give to Coriolis  
Deployment requirements| Coriolis worker component(s) need network access to the oVirt APIs.| Coriolis deployment and environment connectivity requirements  
DRaaS source requirements| All VM disks must be normal virtual disks located on a block or file-based storage domain. Incremental Backups must be available for use and enabled on all disks of the VMs that will be replicated. Coriolis can be optionally configured to automatically enable Incremental Backups itself. Network and LUN-based disks cannot have Incremental Backups enabled on them, so they are not supported.| Requirements to use the replica export (DRaaS source) features  
Instance identification scheme| Names must be unique| How instances to migrate/replicate are identified on a source cloud handled by this plugin  
Network identification scheme| IDs of VM Networks| How the plugin identifies networks. Required for the **network_map** field of the **- destination-environment**  
Storage identification scheme| Names of storage domains hosting the virtual disk(s)| How the plugin identifies storage backends. Required for the **storage_map** field of the **- destination-environment**  

### oVirt Endpoint Connection Parameters

To connect to oVirt to perform a migration from it, the following connection parameters are required:

#### Example of connection info JSON to be passed to the oVirt plugin

```json
{     "url": "https://manager.olvm.local/ovirt-engine/api",     "username": "admin",     "password": "Password",     "allow_untrusted": true } 
```

Each parameter represents:

  * **url (string)** - the full URL (including protocol, port number and endpoint subpath (e.g. /ovirt-engine/api))
  * **username (string)** - the username to login as
  * **password  (string) **- the password for the given username
  * **allow_untrusted (boolean)** - whether or not to accept connecting to oVirt hosts with self-signed certificates
