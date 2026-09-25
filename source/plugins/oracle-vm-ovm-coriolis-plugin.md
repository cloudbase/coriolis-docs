---
title: "Oracle VM (OVM) Coriolis Plugin"
wp_id: 38466
---

# Oracle VM (OVM) Coriolis Plugin

**Coriolis** integrates the platform Plugin on the Appliance itself, this way there is no need for agents to be deployed on platforms to establish the communication between the platform and the Coriolis components. Using this type of architecture, Coriolis guarantees the connection to the supported platform set up to be used as either Source or Destination, as long as the requirements are met.

This section describes the functionality available via Coriolis' Oracle VM (OVM) plugin, which enables Coriolis to migrate (CMaaS) instances from OVM, as well as both migrate and replicate to OVM.

[![](_static/images/ovm-dest-1.jpg)](https://i0.wp.com/cloudbase.it/wp-content/uploads/2022/04/ovm-dest-1.jpg?ssl=1)[![](_static/images/ovm-source.jpg)](https://i0.wp.com/cloudbase.it/wp-content/uploads/2022/04/ovm-source.jpg?ssl=1)

### Deployment requirements

#### Deployment requirements

The worker components of Coriolis need network access to the OVM APIs.

Additionally, network access from the Coriolis worker components to the external network of the OVM deployment is required in order to reach temporary VMs Coriolis will be spawning on OVM during the migration/replication operations.

Alternatively, one may deploy the Coriolis worker components on OVM directly and thus avoid any API/VM network access limitations.

OVM Coriolis plugin does not support replicate/migrate UEFI instances (not supported by OVM platforms).

### Oracle PV-drivers

Coriolis will require access to Oracle PV-drivers in order to have the Migrated VM properly set up for the destination environment.

For more information on how to download and have Coriolis use **[Oracle PV-drivers](https://cloudbase.it/oracle-paravirtual-drivers)** , please check the documentation page.

### Coriolis OVM Exporter

The Coriolis OVM Exporter service has been integrated with Coriolis to efficiently and safely move the virtual machines from OVM to any of the supported destinations, without any kind of interruption to business continuity on the source.

For more information regarding **Coriolis OVM Exporter** , please check **[OVM Exporter](https://cloudbase.it/coriolis-ovm-exporter)** page.

### OVM as a source cloud

Coriolis' OVM plugin supports both migrating (CMaaS) and replicating (DRaaS) from OVM.

For more information regarding **[OVM as a source cloud](https://cloudbase.it/ovm-as-a-source-cloud)** , please check its documentation page.

### OVM as a destination cloud

NOTE! Support for OVM as a target platform has been deprecated in Coriolis. Please contact us for more details.

#### Disk copy worker templates

During the migration process to/from OVM, Coriolis creates a temporary worker VM to which it attaches snapshots of the original instance's disks to read them through it.

The disk reading process involves transmission over an SSH channel, so both security and transfer efficiency should be maximized, though at the cost of the disk copy worker having to do some compression itself, which is why it is recommended that the Worker VM template be configured to be more compute-capable (CPU/RAM).

The images do **NOT** require any special Coriolis agent running in them and can be images already available on OVM, granted the following requirements:

  * image is recommended to be an Oracle Linux 7+
  * image must have OVMd installed and configured for an initial run on OVM (required for querying the guest IP address)



For each instance it is migrating, Coriolis will create a dedicated disk copy worker on OVM to fetch its storage.

The template must be pre-configured with a NIC on a network that is reachable from the Coriolis installation. Additionally, the template should be pre-configured to use DHCP for each worker VM to be allocated to its own IP.

For more information regarding the Coriolis Worker template, please check the **[Coriolis Temporary Migration Worker](https://cloudbase.it/coriolis-temporary-migration-worker) **page.

### OVM connection parameters

In order to connect to OVM to perform a migration from it, the following connection parameters are required:

#### Example of connection info JSON to be passed to the OVM plugin

```json
 {
     "host": "10.7.1.2",
     "port": "443",
     "username": "admin",
     "password": "SuperS3kre7",
     "allow_untrusted": true
 } 
```

Each parameter represents:

  * **host (string)** - the IP address or hostname of the OVM API server
  * **port (integer)** - the port the OVM server is listening on
  * **username (string)** - the username to login as
  * **password (string)** - the password for the given username
  * **allow_untrusted (boolean)** - whether or not to accept connecting to OVM hosts with self-signed certificates



### OVM platform specifics

Supported Actions: | Migration Source/Destination - Replica Source/Destination| Comments  
---|---|---  
Plugin identifier| **oracle_vm**|  Identifies the plugin. Used for the **- provider** CLI parameter  
Credentials needed| Standard OVM user/pass credentials| Necessary credentials to give to Coriolis  
Deployment requirements| Coriolis worker component(s) need network access to the OVM APIs| Coriolis deployment and environment connectivity requirements  
Source disk export requirements| OVM is supported as a DRaaS source only through Coriolis' in-build data replication engine| Requirements to use the replica export (DRaaS source) features  
Instance identification scheme| VM names| How instances to migrate/replicate are identified on a source cloud handled by this plugin  
Network identification scheme| Names of OVM Networks| How networks are identified by the plugin. Required for the **network_map** field of the **- destination-environment**  
Storage identification scheme| Names of OVM storage pools| How storage backends are identified by the plugin. Required for the **storage_map** field of the **- destination-environment**
