---
title: "How to create a Migration"
wp_id: 43473
---

# How to create a Migration

To create a Migration from the Coriolis Web UI, select from the top right, “**New** ” and then select “**Transfers** ” from the drop-down.  
  
[![](_static/images/new01.png)](https://i0.wp.com/cloudbase.it/wp-content/uploads/2026/05/new01.png?ssl=1)

Coriolis defaults to Migrations by default:

[![](_static/images/Screenshot_10-7-2025_17534_10.8.254.69.jpeg)](https://i0.wp.com/cloudbase.it/wp-content/uploads/2025/07/Screenshot_10-7-2025_17534_10.8.254.69.jpeg?ssl=1)

Select the desired source and destination clouds.  
In this example, the chosen source platform will be a VMWare vSphere.

[![](_static/images/source_cloud.png)](https://i0.wp.com/cloudbase.it/wp-content/uploads/2026/05/source_cloud.png?ssl=1)

After selecting the source Endpoint and selecting next, the new window will be “Source options”, where: 

  * CBT can be automatically enabled, in case the machines on the source do not have it enabled already
  * Choose the compatibility mode for the vixDiskLib, the official VMware library Coriolis uses for exporting disk data from VMware/ESXi. By default, Coriolis is configured to use OpenVixDiskLib. Using VDDK requires additional **[setup](https://cloudbase.it/setting-up-the-vixdisklib-library/)**.



Changed Block Tracking, or **CBT** , is required by Coriolis to create the VM disk on the destination side during the Replica process. It can be enabled from VM attributes on VMware or using Coriolis' **Source options**.  
Automatically enabling CBT will **NOT** work if the VM that is to be migrated has pre-created snapshots, in which case Coriolis will provide a clear warning.

[![](_static/images/create-replica-4.jpg)](https://i0.wp.com/cloudbase.it/wp-content/uploads/2023/02/create-replica-4.jpg?ssl=1)

Select the VMware VMs that are to be migrated, and click “Next”.

[![](_static/images/create-replica-5.jpg)](https://i0.wp.com/cloudbase.it/wp-content/uploads/2023/02/create-replica-5.jpg?ssl=1)

Select the destination Cloud Endpoint. In this example, OpenStack will be used.

[![](_static/images/create-replica-6.jpg)](https://i0.wp.com/cloudbase.it/wp-content/uploads/2023/02/create-replica-6.jpg?ssl=1)

### Parallel migrations

Coriolis Migration or Replica jobs offer the flexibility to select**one or multiple source VMs for migration**. When multiple VMs are chosen, Coriolis executes all tasks concurrently and simultaneously for all selected VMs. This process begins with taking snapshots of each VM and then transferring the data in parallel.

This feature is useful when migrating a cluster comprised of multiple VMs, or when entire projects, inclusive of all VMs within them require a synchronization of the migration process.

  * ![](_static/images/Screenshot_12-3-2024_194955_10.8.254.132.jpeg)
  * ![](_static/images/Screenshot_12-3-2024_195057_10.8.254.132-scaled.jpeg)



### Specify general settings for the migration job

In the Target options page, “Simple” will be selected as the default, with a few options available:

  1. Description – where a description for the replica process may be entered
  2. Execute now – which is selected by default for the process execution to start as soon as the configuration is complete
  3. Execute now Options – an option that will offer to shut down the instances before the process starts, it is set to “no” by default



The more fine-grained OpenStack options under the "Advanced" section will also be shown shortly.  
Select “Next” after the above steps.

[![](_static/images/create-replica-8.jpg)](https://i0.wp.com/cloudbase.it/wp-content/uploads/2023/02/create-replica-8.jpg?ssl=1)

The next window will allow for the selection of a network on the destination OpenStack corresponding to each network the VM was attached to on the source VMWare.  
Once every mapping is assigned, click “Next”

[![](_static/images/create-replica-9.jpg)](https://i0.wp.com/cloudbase.it/wp-content/uploads/2023/02/create-replica-9.jpg?ssl=1)

The following window will allow for the selection of storage options on OpenStack corresponding to each datastore the VM's disks were using on the source VMWare. The storage selection can also be done for each disk individually.

[![](_static/images/create-replica-10.jpg)](https://i0.wp.com/cloudbase.it/wp-content/uploads/2023/02/create-replica-10.jpg?ssl=1)

### Specify advanced migration settings

In the case of Migrating or Replicating to Openstack, Coriolis will need to boot some temporary VMs on OpenStack to perform tasks such as data transfer and OSMorphing.

For these so-called "temporary worker VMs", some pre-created VM templates must exist on Openstack and must be referenced to Coriolis.

There are no added requirements for the template.

If Migrating Windows VMs, the Windows template must be of an equal or later version to the guests being Migrated/Replicated, as the Windows image servicing tools are not forward-compatible.

For more information regarding **[Coriolis Temporary Worker VM](https://cloudbase.it/coriolis-temporary-migration-worker/)** , please check the page.

[![](_static/images/create-replica-11.jpg)](https://i0.wp.com/cloudbase.it/wp-content/uploads/2023/02/create-replica-11.jpg?ssl=1)

If the target platform does not allow for maintaining the same MAC address, or the user asks Coriolis to change the MAC address, all network interface naming udev rules should be disabled.

### Specify scheduling options

The next step will be the Schedule

[![](_static/images/create-replica-12.jpg)](https://i0.wp.com/cloudbase.it/wp-content/uploads/2023/02/create-replica-12.jpg?ssl=1)

Here, a schedule can be created by selecting “Add Schedule”

The Schedule will run incremental syncs for that replica at the specified time and for the specified dates.

In the example, below the Schedule is set to run incremental syncs for the Replica, every day of March, every 6 hours.

In the first column, the “Run” button is available to start the schedule when the first replica finishes (by default it comes as off)

[![](_static/images/create-replica-schedule.jpg)](https://i0.wp.com/cloudbase.it/wp-content/uploads/2023/02/create-replica-schedule.jpg?ssl=1)

In the last column, the is an “Options” dialog which will allow some additional options, such as the ability to have Coriolis shut down the source VM before the disk syncing occurs, thus better guaranteeing the transfer's consistency.

[![](_static/images/image-43.png)](https://i0.wp.com/cloudbase.it/wp-content/uploads/2020/03/image-43.png?ssl=1)

### Review Migration settings and start the job

As the last step of the configuration, a summary of it will be shown with all the configurations made in the previous steps.  
If any options seem missing or incorrect, one may click "Back" to return and edit them. Clicking “Finish” will start the process of creating the Replica.

[![](_static/images/create-replica-13.jpg)](https://i0.wp.com/cloudbase.it/wp-content/uploads/2023/02/create-replica-13.jpg?ssl=1)

Now the Replica is created and the first Replica Execution is triggered. The tasks that are to be performed are available to track and monitor from the Replica view screen.

[![](_static/images/create-replica-14.jpg)](https://i0.wp.com/cloudbase.it/wp-content/uploads/2023/02/create-replica-14.jpg?ssl=1)

After the process finishes, tasks are shown as complete:

[![](_static/images/create-replica-15.jpg)](https://i0.wp.com/cloudbase.it/wp-content/uploads/2023/02/create-replica-15.jpg?ssl=1)
