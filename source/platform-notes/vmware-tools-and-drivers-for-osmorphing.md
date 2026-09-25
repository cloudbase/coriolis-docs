---
title: "VMware tools and drivers for OSMorphing"
wp_id: 40584
---

# VMware tools and drivers for OSMorphing

When using **Coriolis ' Replica/Migration** function for Windows VMs using any of the supported source platforms to one of the VMWare supported platforms, **Coriolis** will need to have access to a set of **VMware tools and drivers** for the Migrated VM to run on the destination VMware platform correctly.

For Coriolis to have access to a set of VMware drivers, the installation packages must be available as an archive file over the network or placed directly on the Coriolis appliance.

The following steps will guide towards extracting the VMWare tools and drivers files and having them available for Coriolis to use:

  * A Windows Server VM deployed in the VMware environment
  * VMware tools must be installed on the newly deployed Windows Server VM
  * once the above requirements are met, run the PowerShell script that will create a .zip file for the drivers 
    * the script can be copied from the [GitHub page](https://github.com/cloudbase/coriolis-resources/blob/master/vmware/extract_drivers.ps1).
  * copy the VMware tools archive to a (local/private) web server 
    * the web server must be accessible from the temporary worker network on the target cloud
    * the **URL** for the .zip file will be required in **Advanced Target Options** when performing **Replica/Migration**.

Once the above steps are complete, **Coriolis** will be able to **Migrate** Windows VMs and install platform specifics to **VMware destination environments**.
