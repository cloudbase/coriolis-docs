---
title: "Amazon Web Services (AWS) Coriolis Plugin"
wp_id: 38516
---

# Amazon Web Services (AWS) Coriolis Plugin

**Coriolis** integrates the platform Plugin on the Appliance itself, this way there is no need for agents to be deployed on platforms to establish the communication between the platform and the Coriolis components. Using this type of architecture, Coriolis guarantees the connection to the supported platform set up to be used as either Source or Destination, as long as the requirements are met.

[![](_static/images/AWS-source.jpg)](https://i0.wp.com/cloudbase.it/wp-content/uploads/2022/04/AWS-source.jpg?ssl=1)[![](_static/images/ASW-destination.jpg)](https://i0.wp.com/cloudbase.it/wp-content/uploads/2022/04/ASW-destination.jpg?ssl=1)

### Deployment requirements and supported AWS instances

#### Deployment requirements

The worker components of Coriolis need network access to the AWS APIs, as well as to the public IPs of the temporary VMs Coriolis will be creating during the migration process.

#### Supported instances

**The AWS Coriolis plugin only supports EBS-backed instances**. Migrating instance-storage-based VMs is unfeasible given Coriolis' agentless nature (from the point of view of the migrated instances).

Currently,**only HVM guests are supported** , with support for PV guests in advanced development stages.

### AWS connection parameters

In order to connect to AWS to perform a migration from it, the following connection parameters are required:

#### Example of connection info JSON to be passed to the AWS plugin

```json
{
     "region": "us-west-2",
     "access_key_id": "BKIAKWUNHI3HYZJ7Y3EQ",
     "secret_access_key": "XuuT6SMN5Ub96AXMEIX9gvPXITK3xnfyRFJOkaSo"
 }
```

Each parameter represents:

  * **region (string)** - the AWS region from which to migrate the selected instances. For a complete table of the available regions and their identifiers, please review the "Available Regions" section of [this](http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/using-regions-availability-zones.html) article of Amazon's documentation
  * **access_key_id (string)** - the ID of the access key to connect with
  * **secret_access_key  (string)** - the secret access key to connect with



### AWS as a source cloud

For more information on using AWS as a **source cloud** for Replica/MIgration, please check the **[AWS as a source cloud](https://cloudbase.it/aws-as-a-source-cloud)** page.

### AWS as a dstination cloud

For more information on using AWS as a **destination cloud** for Replica/MIgration, please check the **[AWS as a destination cloud](https://cloudbase.it/aws-as-a-destination-cloud)** page.

### AWS platform specifics

Supported Actions: | Migration Source/Destination - Replica Source/Destination| Comments  
---|---|---  
Plugin identifier| **AWS**|  Identifies the plugin. Used for the **- provider** CLI parameter  
Credentials needed| Standard AWS API access keys| Necessary credentials to give to Coriolis  
Deployment requirements| Coriolis worker component(s) need network access to the AWS APIs| Coriolis deployment and environment connectivity requirements  
Source disk export requirements| VM disks must be EBS-backed. Disk export is done through Coriolis' in-build data replication engine.| Requirements to use the replica export (DRaaS source) features  
Instance identification scheme| ID or "Name" tag| How instances to migrate/replicate are identified on a source cloud handled by this plugin  
Network identification scheme| IDs of VPCs| How networks are identified by the plugin. Required for the **network_map** field of the **- destination-environment**  
Storage identification scheme| EBS volume types| How storage backends are identified by the plugin. Required for the **storage_map** field of the **- destination-environment**  
For more information regarding Coriolis Worker template, please check the **[Coriolis Temporary Migration Worker](https://cloudbase.it/coriolis-temporary-migration-worker) **page.
