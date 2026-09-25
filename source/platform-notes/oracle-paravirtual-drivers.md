---
title: "Oracle Paravirtual Drivers"
wp_id: 39500
---

# Oracle Paravirtual Drivers

When using **Coriolis ' Replica/Migration** function for Windows VMs using any of the supported source platforms to one of the Oracle-supported platforms, **Coriolis** will need to have access to a set of **Oracle Paravirtual Drivers** for the Migrated VM to run on the destination Oracle platform correctly.

The following steps apply to **Oracle VM** only.

For Coriolis to have access to a set of Oracle Paravirtual Drivers, the installation packages will have to be available as an archive file over the network or placed directly on the Coriolis appliance.

The following steps will guide toward extracting the Oracle Paravirual Drivers files and having them available for Coriolis to use:

  * a **Windows VM** is required on the Oracle platform and is available
  * **download** Oracle Paravirtual Drivers from the Oracle official support page 
    * Oracle VM Windows PV drivers are available at no charge and can be downloaded by following the instructions**[here](https://www.oracle.com/virtualization/technologies/vm/downloads/server-storage-vm-downloads.html)**.
  * have the Setup.exe file of the PV drivers copied on the **Windows VM** under the system drive root folder (usually C:\\)
  * run the following script on the **Windows VM** , which will **install** and **create an archive** of the PV drivers files under the **pv-drivers** folder on the system drive.

The end archive created by the below script must contain the files and sub-folders of the "Oracle VM Windows PV Drivers" directory but not the directory itself.

```text
Start-Process -Wait -ArgumentList "/silent" -PassThru -FilePath '$env\Setup.exe'
 $winnet = "${env:ProgramFiles(x86)}\Oracle Corporation\Oracle VM Windows PV Drivers\winnet"
 $winlh = "${env:ProgramFiles(x86)}\Oracle Corporation\Oracle VM Windows PV Drivers\winlh"
 if (!(Test-Path $winnet) -or !(Test-Path $winlh)) {
     Write-Information -MessageData "OVM PV drivers folder structure is not as expected" -InformationAction Continue
 }
 New-Item -ItemType directory -Path $env\pv-drivers
 Compress-Archive -Path "${env:ProgramFiles(x86)}\Oracle Corporation\Oracle VM Windows PV Drivers\*" -DestinationPath "$env\pv-drivers\pv-drivers.zip"
```

  * copy the PV drivers archive to a web server where Coriolis has access to, or directly on Coriolis Appliance 
    1. for using a webserver: 
       * using **Coriolis CLI** , navigate to **/etc/coriolis**
       * edit **coriolis.conf** file 
       * under**oracle_vm_migration_provider** add the path to **windows_pv_drivers_url =**
    2. for using the local Coriolis Appliance 
       * have the pv-drivers copied into a new directory on Coriolis Appliance
       * navigate to /etc/coriolis and use SCP to transfer the file to the Appliance
       * edit **coriolis.conf** file 
       * under**oracle_vm_migration_provider** add the path to **windows_pv_drivers_url =**
  * on Coriolis, add the PV drivers archive path to Coriolis' configuration file 
    * connect to Coriolis command-line interface
    * add the link to **coriolis.conf** file located under **/etc/coriolis/**
      * $**windows_pv_drivers_url =** Path to the PV drivers archive
    * **restart** the Coriolis Worker container 
      * $**docker restart** **coriolis-worker**

Once the above steps are complete, **Coriolis** will be able to **Migrate** Windows VMs and install platform specifics to **Oracle destination environments**.
