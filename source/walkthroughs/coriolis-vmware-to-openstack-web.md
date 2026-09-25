---
title: "Coriolis &#8211; How to migrate VMs from VMware to OpenStack using the Web interface"
wp_id: 37739
---

# Coriolis &#8211; How to migrate VMs from VMware to OpenStack using the Web interface

Beside the [command line interface (CLI)](https://cloudbase.it/coriolis-vmware-to-oracle-vm-cli), Coriolis provides a web UI designed for a guided user experience.

To begin with, just point the browser (Firefox, Chrome, Safari or Edge) to the address of your Coriolis VM. The website uses a self signed certificate by default, so you might want to add a security exception in your browser.

[![](_static/images/Coriolis-Web-Welcome.png)](https://cloudbase.it/coriolis-how-to-migrate-vms-from-vmware-to-oracle-vm-using-the-web-interface/coriolis-web-welcome/)You can use the “admin” user to login with the password randomly generated during the deployment. To retrieve the password, just connect to the VM using **SSH**(default credentials:**root / coriolis**) and run:

```text
grep OS_PASSWORD /etc/kolla/admin-openrc.sh
```

Once logged in, click on “**Cloud Endpoints** ”:

[![](_static/images/Coriolis-Web-Endpoints.png)](https://cloudbase.it/coriolis-how-to-migrate-vms-from-vmware-to-oracle-vm-using-the-web-interface/coriolis-web-endpoints/)

### Creating an endpoint for OpenStack

After clicking on “**New** ” you will see all available cloud endpoint options currently installed, for example:

[![](_static/images/Coriolis-Web-Create-Endpoint.png)](https://cloudbase.it/coriolis-vmware-to-oracle-vm-web/coriolis-web-create-endpoint/)Choose “**OpenStack** ” and provide all the required data. Make also sure to set “**Allow Untrusted** ” to “**Yes** ” if your OpenStack API endpoint uses a HTTPS self signed certificate.

[![](_static/images/Coriolis-Web-Create-OpenStack-Endpoint-2.png)](https://cloudbase.it/coriolis-vmware-to-openstack-web/coriolis-web-create-openstack-endpoint-3/)Once done, click “**Save** ”. This will create the endpoint and trigger a validation of the data by attempting a connection to the OpenStack API.

[![](_static/images/Coriolis-Web-Validating-Endpoint.png)](https://cloudbase.it/coriolis-how-to-migrate-vms-from-vmware-to-oracle-vm-using-the-web-interface/coriolis-web-validating-endpoint/)

### Creating an endpoint for VMware vSphere

You can repeat the same procedure choosing "**VMware** " and provide the required data. Also in this case make sure to set “**Allow Untrusted** ” to “**Yes** ” if your VMware vSphere API endpoint uses a self signed certificate.

[![](_static/images/Coriolis-Web-Create-VMware-Endpoint.png)](https://cloudbase.it/coriolis-how-to-migrate-vms-from-vmware-to-oracle-vm-using-the-web-interface/coriolis-web-create-vmware-endpoint/)

Like in the previous case, clicking “**Save** ” will create the endpoint and trigger the connection validation.

### Configuring a replica for a VM from vSphere to OpenStack

Click on “**Replicas** ” and choose “**New** ”. You will be greeted by an introductory screen:

[![](_static/images/Coriolis-Web-New-Replica-1.png)](https://cloudbase.it/coriolis-how-to-migrate-vms-from-vmware-to-oracle-vm-using-the-web-interface/coriolis-web-new-replica-1/)

Click “**Next** ” and select the source endpoint (**VMware**):

[![](_static/images/Coriolis-Web-New-Replica-2.png)](https://cloudbase.it/coriolis-how-to-migrate-vms-from-vmware-to-oracle-vm-using-the-web-interface/coriolis-web-new-replica-2/)

Click “**Next** ” and choose the target endpoint (**OpenStack**):

[![](_static/images/Coriolis-Web-New-Replica-3-OpenStack.png)](https://cloudbase.it/coriolis-vmware-to-openstack-web/coriolis-web-new-replica-3-openstack/)After clicking “**Next** ” again, it’s time to select the VM(s) to migrate. You can apply filters on the name to simplify the search:

[![](_static/images/Coriolis-Web-New-replica-5.png)](https://cloudbase.it/coriolis-how-to-migrate-vms-from-vmware-to-oracle-vm-using-the-web-interface/coriolis-web-new-replica-5/)Click “**Next** ” to set the OpenStack specific options, starting with the name of the **flavor** to be used:[![](_static/images/Coriolis-Web-New-replica-6-OpenStack.png)](https://cloudbase.it/coriolis-vmware-to-openstack-web/coriolis-web-new-replica-6-openstack/)Clicking once more “**Next** ” will bring you to the **Network Mapping** , where for each network used by the VM(s) on the source cloud we need to select a matching network on the target. This is where the VMs will be connected after being migrated.[![](_static/images/Coriolis-Web-New-replica-7-OpenStack.png)](https://cloudbase.it/coriolis-vmware-to-openstack-web/coriolis-web-new-replica-7-openstack/)Click “**Next** ” and you will see the **scheduling** options:

[![](_static/images/Coriolis-Web-New-replica-8.png)](https://cloudbase.it/coriolis-how-to-migrate-vms-from-vmware-to-oracle-vm-using-the-web-interface/coriolis-web-new-replica-8/)One more “**Next** ” and you have a final confirmation screen:

[![](_static/images/Coriolis-Web-New-replica-9-OpenStack.png)](https://cloudbase.it/coriolis-vmware-to-openstack-web/coriolis-web-new-replica-9-openstack/)Click “**Finish** ” and the replica will start executing:[![](_static/images/Coriolis-Web-New-replica-10-OpenStack.png)](https://cloudbase.it/coriolis-vmware-to-openstack-web/coriolis-web-new-replica-10-openstack/)You can now click on the replica to see the execution details:[![](_static/images/Coriolis-Web-Replica-Execution-OpenStack.png)](https://cloudbase.it/coriolis-vmware-to-openstack-web/coriolis-web-replica-execution-openstack/)Once completed, the replica can be executed incrementally multiple times to update the replicated content (this is typically scheduled, e.g. hourly, daily, weekly, etc).

### Migrating the VM from the replica

From the replica details, you can click on “**Migrate Replica** ” to get the VM(s) running on OpenStack:[![](_static/images/Coriolis-Web-Migrate-Replica-OpenStack.png)](https://cloudbase.it/coriolis-vmware-to-openstack-web/coriolis-web-migrate-replica-openstack/)

You can click on “**View Migration Status** ” to watch the migration progress. The "**migrations** " view can also be reached through the main menu (click on the top left icon).[![](_static/images/Coriolis-Web-Migrate-Replica-2-OpenStack.png)](https://cloudbase.it/coriolis-vmware-to-openstack-web/coriolis-web-migrate-replica-2-openstack/)Once completed, the migration status will change accordingly:

[![](_static/images/Corolis-Web-Migration-completed-OpenStack.png)](https://cloudbase.it/coriolis-vmware-to-openstack-web/corolis-web-migration-completed-openstack/)Congratulations, your VM is now running and accessible from the OpenStack Horizon dashboard:[![](_static/images/Corolis-Web-Migration-completed-Horizon.png)](https://cloudbase.it/coriolis-vmware-to-openstack-web/corolis-web-migration-completed-horizon/)
