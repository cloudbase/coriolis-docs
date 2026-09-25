---
title: "Installing the Coriolis All-in-One Appliance"
wp_id: 38491
---

# Installing the Coriolis All-in-One Appliance

## Deploy Coriolis VM

1\. Obtain the Coriolis trial appliance image

Contact your Cloudbase Solutions representative for the virtual appliance, which is usually shipped as an OVA file.

2\. Import the image and create a VM from it

Depending on the environment where Coriolis will be deployed, the Appliance disk image may need to be converted to a format accepted by the said platform.

For converting the appliance disk format, Cloudbase recommends the use of qemu-img, as it is both easily obtainable and straightforward to use.

If you're performing the conversion on a Linux host, please look up how to install **qemu-img** from your distribution's standard package repositories. On Windows, a Windows-only build of **qemu-img** can be obtained from Cloudbase from the following [**qemu-img page**](https://cloudbase.it/qemu-img-windows/).

For Linux distributions, you can use:

# First extract the OVA tar -xvf coriolis-appliance.ova # this will extract the vmdk disk. Use qemu-img to convert it: qemu-img convert -f vmdk -O qcow2 disk-0.vmdk image-name.qcow2

1234 | # First extract the OVAtar -xvf coriolis-appliance.ova# this will extract the vmdk disk. Use qemu-img to convert it:qemu-img convert -f vmdk -O qcow2 disk-0.vmdk image-name.qcow2  
---|---  
  
For this example, the Coriolis VM will be deployed in VMWare by importing the .ova file directly from the Web link.

 NOTE: If using Coriolis for DRaaS scenarios, deploying Coriolis on the source platform is not recommended for fault tolerance reasons. In DRaaS scenarios, please deploy the appliance on the destination platform or within a space that is external and independent of both platforms.

Example network configuration

Scenario 1:  
Single network interface to the Coriolis appliance that handles all communications with the source and target platforms, including the data transfer.  
It must be ensured that the speedlink for the virtual interface is higher than 1Gbps, as that will affect the migration job duration.

Scenario 2:  
A first interface is used for management and platform communication.  
The 2nd interface handles the data replication, this must be on a high bandwidth for faster migrations.

3\. Connect to the Coriolis appliance

After the deployment is complete, connect to the serial console of the Coriolis VM from the platform on which it is deployed.

[![](_static/images/coriolis-console.jpg)](https://i0.wp.com/cloudbase.it/wp-content/uploads/2022/04/coriolis-console.jpg?ssl=1)

4\. Obtain the password to the **admin** account for Coriolis

In order to get the admin password of the Coriolis web UI, navigate to option '**2** ', **Show UI Login Details**

[![](_static/images/pass.jpg)](https://i0.wp.com/cloudbase.it/wp-content/uploads/2022/04/pass.jpg?ssl=1)

**NOTE:** If the environment the Coriolis Appliance was deployed in does not feature DHCP, you will have to log in to the serial console of the appliance and manually configure static networking within it, using option '4' Edit/Inspect Network Settings. It is recommended that the appliance be rebooted after any networking-related reconfigurations.

The appliance will automatically configure the settings below if provided by the network configuration or a metadata service. The following settings should be verified and confirmed:

a. Ensure that all network settings are correct for the Coriolis Appliance. This includes the DNS entries, as Coriolis must be able to resolve FQDNs for various online Cloud Providers.

b. Ensure that the Coriolis Appliance is allowed to connect to an online NTP host, or that the time is properly synced with the hypervisor. Certain operations will fail if the time drifts and fails to sync.

NOTE: SSH access to the Coriolis virtual appliance is not permitted and not provided to the user. This restriction is enforced for security and stability reasons, as it can introduce the risk of unauthorized modifications, configuration drift, and unintended system changes that may compromise the integrity, supportability, or proper functioning of the appliance.

Any required configuration, troubleshooting, or maintenance operations can be performed through the (serial) console of the appliance, as that provides all the required options and configuration.

[![](_static/images/network.jpg)](https://i0.wp.com/cloudbase.it/wp-content/uploads/2022/04/network.jpg?ssl=1)

5\. Log in to the Coriolis Web UI

Open a new browser tab and type in the IP address of your Coriolis machine and log in using the credentials from the previous step.

[![](_static/images/login-coriolis.jpg)](https://i0.wp.com/cloudbase.it/wp-content/uploads/2023/02/login-coriolis.jpg?ssl=1)

After the credentials are entered, click on **Login,** and the Coriolis Dashboard will load

[![](_static/images/coriolis-ui.jpg)](https://i0.wp.com/cloudbase.it/wp-content/uploads/2023/02/coriolis-ui.jpg?ssl=1)
