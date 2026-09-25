---
title: "Install the Snapshot Agent for Bare Metal Servers"
wp_id: 41765
---

# Install the Snapshot Agent for Bare Metal Servers

#### Prerequisites

Before installing the snapshot agent on the machines, make sure that storage and network requirements are met.

For more information regarding it, please check **[Snapshot Agent for Bare Metal Servers prerequisites](https://cloudbase.it/snapshot-agent-for-bare-metal-servers-prerequisites)** page.

#### Download the Coriolis Snapshot Agent

The **Coriolis Snapshot Agent** needs to be downloaded on the server which will be used for the Coriolis Replica/Migration task.

The following steps will offer guidance for downloading and extracting the file:

1\. Connect to your server via **SSH**

2\. Download the file 

```text
cd ~
wget https://github.com/cloudbase/coriolis-snapshot-agent/releases/download/1.1.1/coriolis-snapshot-agent.tar.gz
```

3\. Extract the downloaded file

```text
tar -xvzf coriolis-snapshot-agent.tar.gz
```

4\. Now the script is ready to run from the following path on the server

~/coriolis-snapshot-agent/

```text
~/coriolis-snapshot-agent/
```

#### Install the Coriolis Snapshot Agent

1\. To install the snapshot agent, you will need to run the interactive installation script, and provide any information it requires:

  * Connect to the machine where you will install the agent and navigate to the directory where it is extracted


  * Run the install script copied on the machine 



```text
./coriolis-snapshot-agent -install
```

[![](_static/images/install-1.jpg)](https://i0.wp.com/cloudbase.it/wp-content/uploads/2022/10/install-1.jpg?ssl=1)

  * Once the script runs, you will be prompted to enter the IP address or Hostname (by using the same DNS servers from your infrastructure, which will be able to resolve both Coriolis' Bare Metal Servers Hostname/s) of the Coriolis Appliance



[![](_static/images/install2.jpg)](https://i0.wp.com/cloudbase.it/wp-content/uploads/2022/10/install2.jpg?ssl=1)

  * Then you will be prompted to enter the **CA Fingerprint** , which can be copied from the top right corner **Coriolis Bare Metal Hub Fingerprint** on the Coriolis UI **Bare Metal Servers** tab as seen below 


  * Also, you will be asked to mention if the machine is used as a web server or not, an option that the **Coriolis Appliance** further uses to generate the certificates.



[![](_static/images/bm-severs.jpg)](https://i0.wp.com/cloudbase.it/wp-content/uploads/2022/10/bm-severs.jpg?ssl=1)

[![](_static/images/install3.jpg)](https://i0.wp.com/cloudbase.it/wp-content/uploads/2022/10/install3.jpg?ssl=1)

  * The following prompt will ask again for the VM's IP address, which will communicate with the Coriolis Metal Hub. (this can be changed in the case that there is a secondary interface on the VM and that one will be preferred for usage)
  * The port that will be used for connection and transfer will prompt you to select a custom one or the default **9999**
  * **The snapstore device will be selected automatically based on the mount point specified when setting up the prerequisites, it must be must be either an empty disk or an empty iSCSI target mounted**
    * The file system for the snapstore disk must support a Linux-specific system call named fallocate (zero range), which is available on the following file systems: 
      * ext4
      * xfs
      * btrfs 



[![](_static/images/snapstore.jpg)](https://i0.wp.com/cloudbase.it/wp-content/uploads/2023/04/snapstore.jpg?ssl=1)

  * After confirming all the steps, Snapshot Agent will proceed with the install task, connection to the Coriolis Appliance, and the creation process of the **Coriolis User** and the group '**disk** '.

[![](_static/images/image.png)](https://i0.wp.com/cloudbase.it/wp-content/uploads/2023/09/image.png?ssl=1)

  * Once the interactive script completes the task, the machine is ready to be added as a **Bare Metal Server** to the **Coriolis Dashboard** and be used for **Replica/Migration**.



#### Coriolis Snapshot Agent Config

With the installation complete, **Coriolis Snapshot Agent** will create a config file containing the selected options and the agent defaults. For more information on the **config file** , check the **[Coriolis Snapshot Agent Config](https://cloudbase.it/coriolis-snapshot-agent-config)** page.

#### Other considerations

Both UEFI and BIOS firmware type-based systems are supported.

Installing and using the Coriolis Snapshot Agent inside a guest VM should work for hardware virtualized-type instances, excluding containers or other virtualization modes.
