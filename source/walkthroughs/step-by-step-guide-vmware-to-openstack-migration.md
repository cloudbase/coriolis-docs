---
title: "Step-by-step guide VMware to OpenStack Migration"
wp_id: 43627
---

# Step-by-step guide VMware to OpenStack Migration

## Prerequisites

Coriolis virtual appliance is provided in the format of an OVA file. This can be deployed directly as-is on VMware.

The VMDK disk file must be extracted and converted into the required virtual disk format for other platforms. More details on this can be found in the [**install guide here**](../guides/install-coriolis.md)

### Obtain Coriolis License

Coriolis requires a license to be installed before being able to run a migration job. The Coriolis team or the Coriolis Partner you have can provide you with an evaluation license.

The Coriolis virtual appliance must be deployed first, and the Appliance ID must be obtained.

  * Go to the About screen

Coriolis licenses are issued based on the unique ID of the Coriolis installation.

To get your Coriolis installation ID, in the main Dashboard screen, navigate to the top right corner, click the user silhouette, and click “About Coriolis”.

![](_static/images/coriolis-license.png)

  * Copy the appliance ID

The About pop-up will show you some details regarding your license (if there is one already). On the bottom row, there will be your Appliance ID, which needs to be copied and sent to have a license generated for your installation.

![](_static/images/license1.png)

#### Installing a Coriolis License

After you receive a new Coriolis license file, it needs to be added to the Coriolis installation.

To do so, please follow the steps below within the Coriolis Web UI:

  1. From the Dashboard, go to “About Coriolis” (check “Obtain license 1.)
  2. In the pop-up, click “Add license” and upload/paste the provided Coriolis license file
  3. After the license is pasted, click on the bottom right “Add license”

![](_static/images/image-7.png)

### Communication ports between the platforms and the Coriolis appliance

The following ports must be allowed in any firewall(s) present in the network where the source platform - Coriolis virtual appliance - target platform reside.

#### OpenStack

**Service**| **Default Port**| **Protocol**  
---|---|---  
Keystone| 5000| TCP  
Cinder| 8776| TCP  
Nova| 8774| TCP  
Glance| 9292| TCP  
Neutron| 9696| TCP  
Swift| 8080| TCP  
Ceph| 6789| TCP  
Temporary Migration Worker - Source| 22, 4433| TCP  
Temporary Migration Worker - Destination| 22  
443 5986
5566| TCP  

#### VMware

**Service**| **Default** **Port**| **Protocol**  
---|---|---  
Management| 443| TCP  
CBT Source| 443| TCP  
Temporary Migration Worker - Destination| 22  
4433 5986
5566| TCP  
Management (to all ESXi nodes)| 902| TCP  

### Endpoints creation for VMware and OpenStack platforms

A Coriolis endpoint represents the connection information that Coriolis will use to interact with the platforms that are part of the migration.

To create endpoints, from the Coriolis Appliance, click “Cloud Endpoints” on the left side menu, then click “Add Endpoint”.

![](_static/images/endpoint1.png)

From the new pop-up, select the Endpoint that is to be used

In the new pop-up, fill in the details for your Endpoint.

#### For VMware

  1. Give a name to the new endpoint
  2. Enter the credentials for a user with the permissions required for Coriolis to migrate off VMware
  3. Add the host IP address 
     * FQDNs can be used, given that the Coriolis virtual appliance network settings allow for resolving the DNS names

![](_static/images/endpoint3.png)

  * **NAME** - the name of the endpoint that will be added
  * **DESCRIPTION** - a description for the endpoint (recommended in the case where multiple endpoints of the same type exist)
  * **USERNAME** - the VMware username
  * **PASSWORD** - the password for the provided username
  * **HOST** - the VMware vSphere hostname or IP address
  * **PORT** - the port number used for accessing the VMware vSphere
  * **ALLOW UNTRUSTED** - either trust or not self-signed certificates. For evaluation purposes, this option can be enabled.

After the details are filled in, click “Validate and save”. Coriolis will then automatically attempt to log in to the VMware platform to ensure the provided credentials are correct.

If the validation step fails, please review all of the provided details to ensure that they are correct.

#### For OpenStack

  1. Give a name to the new endpoint
  2. Provide the login username and its password
  3. Keystone URL must be provided as the authentication URL
  4. Project where the user specified above has access
  5. Keystone API version must be selected; v2 comes as the default

Note: For advanced OpenStack endpoint options, please refer to the **OpenStack connection parameters** on the **[Coriolis OpenStack plugin](http://openstack-coriolis-plugin)** page.

![](_static/images/endpoint5.png)

  * **NAME** - a name for the endpoint to be created
  * **DESCRIPTION** - a description for the endpoint (recommended in the case where multiple endpoints of the same type exist)
  * **IDENTITY API VERSION** - the version of the Keystone API to use, supported versions including v2 and v3
  * **AUTHENTICATION URL** - the URL of the identity service, with proper schema ("http" or "https"), port, and path ("v2.0" for Keystone v2, and "v3" for v3)
  * **USERNAME** - username to log in with
  * **PASSWORD** - password to log in with
  * **PROJECT NAME** - name of the project to migrate to/from
  * **GLANCE API VERSION** - version of the Image API to use for any interactions with Glance, supported versions being v1 and v2

### Coriolis Temporary Worker Template

The Coriolis Temporary Migration worker is a temporary VM that Coriolis creates on the destination platform to perform tasks such as transferring data and installing platform-specific drivers. After the process is complete, the temporary worker VM is deleted.

There must be present Linux and Windows OS images on the destination platform for the temporary worker to boot and perform the tasks.

In a situation of Replicating/Migrating a Linux VM, only Linux templates are required, as both **Disk cloning** and **OSMorphing** processes use Linux.

NOTE! When migrating a **Windows VM** , both **Linux and Windows templates** have to be specified. The **Disk cloning** is performed using the Linux template, and **OSMorphing** is performed using the Windows template.

#### Linux Temporary Migration Worker

For Linux OS images, we recommend using **Ubuntu Server 20.04 LTS (or newer)** , or **Oracle Linux Server 8 (or newer).** Both distributions have cloud images provided by their vendors, which can be used as-is, without any modifications.

#### Windows Temporary Migration Worker

When Migrating Windows VMs, the Windows VM template must be based on the same version of the VM to be migrated

More information on configuring the Windows Migration Template can be found on the **[Coriolis Temporary Migration Worker page](../reference/coriolis-temporary-migration-worker.md)**.

## Migration process

Once the prerequisites are met, a Migration can be started.

From the Coriolis Dashboard, select 'New' and then 'Transfer'

![](_static/images/mgr0.png)

On the 'Transfer' page, the default transfer type is set to 'Migration'. Selecting next will create the migration.

![](_static/images/Screenshot_10-7-2025_17534_10.8.254.69.jpeg)

The source platform needs to be selected as follows.

![](_static/images/mgr3.png)

For VMware as a source platform, the options are represented by:

  * Automatically Enable CBT - this option, if enabled, will allow Coriolis to enable CBT before disk replication
  * vixDiskLib compatibility mode - it is set to 8.0 by default, and it is backwards compatible in the case that your VMware runs on older versions
  * Use VM Hostname as Instance Name - if enabled, Coriolis will use the hostname of the machine to identify it more easily

All the platform specifics are available on **[VMware as a source page](../platforms/vmware-as-a-source-cloud.md)**.

![](_static/images/mgr4.png)

The next page provides a list of all the VMs available on the selected source platform. Here, we can select one or multiple machines to be migrated

![](_static/images/mgr5.png)

Once the source details are set, the next step will provide the target platform list, from which we can select one, as seen below.

![](_static/images/mgr6.png)

Once the target platform is selected, target options must be allocated to the VM/VMs to be migrated.

All the options are found on the[ **OpenStack as a destination page**](../platforms/openstack-as-a-destination-cloud.md).

![](_static/images/mgr7.png)

The next page allows us to select the OpenStack network to be used by the migrated VM/VMs

![](_static/images/mgr8.png)

After the network, storage will be selected, where we can find:

  * Default Storage - storage type on the destination that will be applied for all disks
  * Storage Backend Mapping
  * Disk Mapping - individual disk mapping using different storage backend types

![](_static/images/mgr9.png)

User scripts will provide the flexibility to perform changes on the VMs to be migrated just before booting on the target platform. This step comes with two options:

  * Global Scripts - applied for all VMs to be migrated based on being either Linux or Windows machines
  * Instance Scripts - individual machine scripts

![](_static/images/mgr10.png)

With the next step, Coriolis will provide a Schedule page, allowing the possibility to run the task on a specific date.

![](_static/images/mgr11.png)

The last customization page provides the following options:

  * Execute Now - when enabled, the transfer will execute immediately after the options are configured
  * Shutdown Instance(s) - when enabled. Coriolis will shut down the instance(s) in the source platform before the transfer is executed.
  * Auto Deploy - when enabled, Coriolis will automatically deploy the instance on the target platform once the transfer is complete.
  * Clone DIsks - when enabled, the disks will be cloned during the deployment
  * Skip OS Morphing - when enabled, OS Morphing will be skipped during the deployment - NOTE - this option is recommended to use only when Source and Target are based on the same platform

![](_static/images/mgr12.png)

The last page before starting the Transfer represents a Summary of all the previously selected options.

To start the Transfer, click on 'Finish'.

![](_static/images/mgr13.png)
