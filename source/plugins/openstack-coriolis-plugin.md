---
title: "OpenStack Coriolis Plugin"
wp_id: 38472
---

# OpenStack Coriolis Plugin

**Coriolis** integrates the platform Plugin on the Appliance itself, this way there is no need for agents to be deployed on platforms to establish communication between the platform and the Coriolis components. Using this type of architecture, Coriolis guarantees the connection to the supported platform set up to be used as either Source or Destination, as long as the requirements are met.

This section describes the functionality available via Coriolis' OpenStack plugin, enabling Coriolis to migrate and replicate to/from an OpenStack cloud.

For a typical VMware to OpenStack migration scenario, here is a representation of the steps involved:

[![](_static/images/image-2.png)](https://i0.wp.com/cloudbase.it/wp-content/uploads/2026/08/image-2.png?ssl=1)

### Deployment requirements and supported OpenStack versions

Coriolis needs network access to the API endpoints (either **public** , **internal,** or **admin** interfaces) of all the core services of the source/destination OpenStack in question.

Coriolis can also be hosted on the OpenStack cloud, to which it will be transferring to or from.

Refer to the [Network Ports Requirements page](https://cloudbase.it/coriolis-network-ports-requirements/) for the full list of OpenStack services that Coriolis must be able to connect to.

#### OpenStack as a Source (Ceph-snapshot-based exports)

The source VM(s) must be booted from a Cinder volume.

Cinder-backup must be configured to use Ceph as a volume storage backend.

Direct access to the Ceph pool used by Cinder-volume is also required.

Read-only access to the Ceph pool used by Cinder-volume is required. (ideally, the credentials used by Cinder volume should be shared with Coriolis to guarantee compatibility)

#### OpenStack as a Source (Coriolis-based exports)

The source VM(s) can be booted from either a Cinder volume or directly from a Glance image.

The Coriolis worker component(s) will need access to the external network used for allocating floating IPs to the temporary worker VMs (the disk export workers)

Alternatively, Coriolis may be deployed directly within the source OpenStack, in which case the floating IP requirement is dropped.

#### OpenStack as a Destination

The Coriolis worker component(s) will need access to the external network used for allocating floating IPs to the temporary worker VMs (the disk copy and OSMorphing workers)

Alternatively, Coriolis may be deployed directly within the destination OpenStack, in which case the floating IP requirement is dropped.

### Supported OpenStack versions

Coriolis supports OpenStack environments starting from the Ussuri release and is compatible with newer releases up to Epoxy.

Coriolis' support for OpenStack is not tied directly to the standard OpenStack release cycle but to the versions of the APIs of each service it interacts with, namely:

  * Keystone: v2 or v3
  * Glance: v1 or v2
  * Nova: v2
  * Neutron: v2.0
  * Cinder: v2
  * Swift (only used when performing Swift-based Replicas from a source OpenStack): v1
  * Ceph (only used when performing Ceph-based Replicas from a source OpenStack):  >= 11 "Kraken"



If an OpenStack offers the above API endpoints, it should be supported regardless of version, vendor, hypervisor (QEMU/KVM or Microsoft Hyper-V), or underlying storage system.

Setups where the source OpenStack's Cinder-backup is configured to use RADOS Gateway as a Swift-like storage backend are also feasible, in which one may perform Swift-based Replicas from the source OpenStack.

Coriolis will by default connect to the public endpoint URL of the above OpenStack services, this can be defined in the endpoint configuration in the Advanced section.

### OpenStack source and destination cloud

For detailed information regarding OpenStack capabilities and performed steps while using it as a source or destination cloud, please check the following pages:

[**OpenStack as a source cloud**](https://cloudbase.it/openstack-as-a-source-cloud/)

[**OpenStack as a destination cloud**](https://cloudbase.it/openstack-as-a-destination-cloud/)

### OSMorphing worker images

During the OSMorphing process, Coriolis will create a temporary VM to scan the Cinder volumes it has just migrated/replicated for the OS installation of the VM it is migrating and perform the necessary changes to ensure it will boot on the destination OpenStack. Because the OSMorphing process is OS-specific, Coriolis will need to be configured with the IDs of two Glance images (one Linux, another one Windows) to boot the temporary OSMorphing workers.

The images do **NOT** require any special Coriolis agent running in them and can be images already available in the destination OpenStack, granted the following requirements:

**Linux** : the Linux image should have cloud-init installed and configured for the first boot. Coriolis will create a unique key pair for each migration/replication and add it as authorized via metadata.

**Windows** : the Windows image should have cloudbase-init installed and configured for the first boot. Coriolis will create a unique key pair for each migration/replication and use it to decrypt the unique password generated by cloudbase-init during the worker's boot.

For more information regarding the Coriolis Worker template, please check the **[Coriolis Temporary Migration Worker](https://cloudbase.it/coriolis-temporary-migration-worker) **page.

### Installing Coriolis as part of an existing OpenStack

Having been built on the same core technologies that power OpenStack's components (Keystone for identity, RabbitMQ for inter-component communications, and so on), Coriolis may be easily integrated into an existing OpenStack deployment by adding the Coriolis endpoint with the 'migration' endpoint type to the Keystone's service catalog and editing Coriolis' configuration to set the appropriate MySQL, Rabbit and Keystone credentials for the Coriolis service.

### Supported instances

#### Coriolis-based exports

The source VM(s) can be booted from either a Cinder volume or directly from a Glance image.

#### Swift/Ceph-based exports

The source VM(s) must be booted from a Cinder volume. VMs booted from a Glance image can not be exported through Swift/Ceph.

NOTE UEFI is supported in certain situations:

  * Microsoft Hyper-V is used. UEFI is supported if the glance image has the following property set:



```text
--property hw_machine_type=hyperv-gen2
```

  * KVM is used. UEFI is supported if the glance image has the following property set:



```text
--property hw_firmware_type=uefi
```

### Coriolis OpenStack Ceph integration

Coriolis also offers the option of Ceph backend storage to be used with the two features of **Ceph Snapshots** and **Ceph Backups** for **Replica and Migration** tasks. For more information on this option, please go to **[Coriolis OpenStack Ceph integration](https://cloudbase.it/openstack-ceph-integration)** page.

### OpenStack platform specifics

**Supported Actions:  ** |  **Migration Source/Destination - Replica Source/Destination**| **Comments**  
---|---|---  
Plugin identifier |  **openstack** |  Identifies the plugin. Used for the **- provider** CLI parameter   
Credentials needed |  Standard Keystone user credentials, not necessarily with administrative rights. If replicating directly from Ceph, the Ceph credentials used by Cinder are also required. |  Necessary credentials to give to Coriolis   
Deployment requirements |  Coriolis worker component(s) need network access to public API endpoints of all core OpenStack services. If replicating directly from Ceph, network access to a Ceph monitor host is required. It can be installed as a service directly into a source/destination OpenStack. |  Coriolis deployment and environment connectivity requirements   
Source disk export requirements |  Through Swift (instances booted from a Cinder volume only): Cinder-backup installed and configured to use Swift as the storage backend ('backup_swift_auth' must be set to 'same_user') OR Through Ceph (instances booted from a Cinder volume only): Either Cinder-volume or Cinder-backup configured to use Ceph (this requires direct Ceph cluster access) OR Through Coriolis (instances can be booted either from a Cinder volume or from a Glance image): Network access to source OpenStack's Floating IP ranges |  Requirements to use the replica export (CMaaS/DRaaS source) features   
Instance identification scheme |  Names (must be unique within the tenant) or IDs |  How instances to migrate/replicate are identified on a source cloud handled by this plugin   
Network identification scheme |  Names or IDs of desired Neutron networks |  How networks are identified by the plugin. Required for the **network_map** field of the **- destination-environment**  
Storage identification scheme |  Names or IDs of Cinder volume types |  How storage backends are identified by the plugin. Required for the **storage_map** field of the **- destination-environment **  

### OpenStack connection parameters

To connect to an OpenStack cloud to perform a migration/replica to/from that cloud, the following connection parameters are required:

#### Example of connection info JSON to be passed to the OpenStack plugin

```json
 {
         "identity_api_version": 3,
         "auth_url": "http://openstack.awesome.our:5000/v3",
         "username": "my username",
         "password": "Sekr3T",
         "project_name": "coriolis",
         "user_domain_name": "domain",
         "project_domain_name": "domain",
         "glance_api_version": 2,
         "allow_untrusted": true,
         "allow_untrusted_swift": true,
         "region_name": "RegionOne",
         "nova_region_name": "RegionOne",
         "neutron_region_name": "RegionOne",
         "glance_region_name": "RegionOne",
         "cinder_region_name": "RegionOne",
         "swift_region_name": "RegionOne"
     "interface_name": "public",
     "nova_interface_name": "public",
     "neutron_interface_name": "public",
     "glance_interface_name": "public",
     "cinder_interface_name": "public",
     "swift_interface_name": "admin",
         "ceph_options": {
                "ceph_conf_file": "config_file_contents",
                "ceph_username": "admin",
                "ceph_keyring_file": "keyring_file_path",
                "ceph_pool_name": "coriolis",
                "ceph_cluster_name: "coriolis_cluster",
                "ceph_connection_timeout": 30
         }
 } 
```

Each parameter represents:

  * **identity_api_version  (integer)** - the version of the Keystone API to use, supported versions including v2 and v3
  * **auth_url (string)** - the URL of the identity service, with proper schema ("http" or "https"), port and path ("v2.0" for Keystone v2, and "v3" for v3)
  * **username**  **(string)** - username to login with
  * **password (string)** - password to log in with
  * **project_name (string)** - name of the project to migrate to/from
  * **user_domain_name (string, Keystone v3 only)** - name of the user domain
  * **project_domain_name (string, Keystone v3 only)** - name of the project domain
  * **glance_api_version (integer)** - version of the Image API to use for any interactions with Glance, supported versions being v1 and v2
  * **allow_untrusted (boolean)** - whether to skip certificate verification if the Keystone is HTTPS-only with self-signed certificates
  * **allow_untrusted_swift (boolean, only used when replicating from an OpenStack)** - whether to skip certificate verification if the Swift proxy is HTTPS-only with self-signed certificates
  * **region_name (string)** - the name of the region to use for all operations. This can be overridden at the service level via the region option relating to each service
  * **nova_region_name (string)** - the name of the Nova region to use, overrides the main **region_name**  parameter
  * **neutron_region_name  (string) **- the name of the Neutron region to use, overrides the main **region_name**  parameter
  * **glance_region_name  (string)** - the name of the Glance region to use, overrides the main region_name parameter
  * **cinder_region_name (string)** - the name of the Cinder region to use, overrides the main **region_name**  parameter
  * **swift_region_name (string, only used when replicating from an OpenStack)** - the name of the Swift region to use, overrides the main **region_name**  parameter
  * **interface_name  (string)** - The name of the interface to use for all services. If a specific interface is required for different services, please use the option afferent to each service.
  * **nova_interface_name  (string)** - The interface name for the OpenStack Compute Service (Nova).
  * **neutron_interface_name  (string)** - The interface name of the OpenStack Networking Service (Neutron).
  * **glance_interface_name  (string)** - The interface name of the OpenStack Image Service (Glance).
  * **cinder_interface_name  (string)** - The interface name of the OpenStack Block Storage Service (Cinder).
  * **swift_interface_name  (string)** - The interface name of the OpenStack Object Storage Service(Swift or RADOS Gateway) Only used when Replicating from a source OpenStack which has Cinder-backup configured to use Swift/RADOS.
  * **ceph_options  (object)** - If performing Ceph-based Replicas from a source OpenStack, the Ceph configuration file and credentials for a user with read-only access to the Ceph pool used by Cinder backups/snapshots must be provided. Coriolis must be able to connect to the source OpenStack's Ceph RADOS cluster by being able to reach at least one Ceph-monitor host. For the easiest setup possible, simply using the same credentials used by the Cinder service(s) will work."
  * **ceph_conf_file  (string)** - Contents of the ceph.conf configuration file containing the list of monitor hosts to connect to. Ideally, this should be the same ceph.conf as used by the Cinder volume/backup service(s). The '[mon] keyring' path options are irrelevant, as the keyring which is passed through the 'Ceph Keyring File' option will be used.
  * **ceph_username  (string)** - Ceph user to use when connecting to the source OpenStack's Ceph cluster. The user must have read-only access to the Ceph pool(s) used by the Cinder-backup and Cinder-volume service(s). Ideally, this should be the same user that the Cinder services themselves are using.
  * **ceph_keyring_file  (string)** - Ceph keyring file with the access key(s) for the user given as the 'Ceph Username' for the cluster described in the given 'Ceph Configuration File'. Ideally, this should be the same keyring file as used by the Cinder service(s).
  * **ceph_pool_name  (string)** - Name of the Ceph pool in which Cinder volume snapshots/backups are stored.
  * **ceph_cluster_name  (string) **- Name of the Ceph cluster in which Cinder volume snapshots/backups are stored.
  * **ceph_connection_timeout  (integer)** - Integer number of seconds to wait on Ceph connections before timing out.



### Known issues

Please check the **[Known issues page](https://cloudbase.it/openstack-known-issues/)** for some known issues and their workaround.
