---
title: "Setting up the vixDiskLib library used for Coriolis Transfers"
wp_id: 38811
---

# Setting up the vixDiskLib library used for Coriolis Transfers

The Coriolis VMWare vSphere plugin allows for Migrating (CMaaS) or Replicating (DRaaS) from individual ESXi hosts or VMWare vSphere deployments using [Changed Block Tracking](https://kb.vmware.com/s/article/1020128?lang=en_US) (CBT) technology.

Coriolis achieves this by leveraging the vixDiskLib library from the official VMWare Virtual Disk Development Kit (VDDK) to call into the CBT subsystem to diff and fetch the blocks of the virtual disks of the VMWare VM(s) being migrated.

**vixDiskLib-related deployment configuration options**

Before setting up the vixDiskLib SOs in use, please double-check the location where Coriolis is configured to search for the library:

#From Coriolis' console menu, select 'option 3' for editing #Verify the config $ cat /etc/coriolis/coriolis.conf ... [vmware_vsphere_migration_provider] ## NOTE: The last path appended here should be identical to the `coriolis_vmware_vix_disklib_dir` ## option shown above vixdisklib_library_directory = /opt/coriolis/vmware-vix-disklib

12345678 | #From Coriolis' console menu, select 'option 3' for editing#Verify the config$ cat /etc/coriolis/coriolis.conf...[vmware_vsphere_migration_provider]## NOTE: The last path appended here should be identical to the `coriolis_vmware_vix_disklib_dir`## option shown abovevixdisklib_library_directory = /opt/coriolis/vmware-vix-disklib  
---|---  
  
**NOTE:** The archive file containing the desired version of vixDiskLib should have been provided alongside your ESXi license(s), but it can also be downloaded from [VMWare's code distribution service](https://code.vmware.com/web/sdk/60/vddk). Depending on the source used, you may need to download/extract the VDDK as a whole in order to find the actual file(s) containing vixDiskLib.

After identifying the correct directory path for the library ("/opt/coriolis/vmware-vix-disklib" in this example), as well as the URL of the archive file containing the desired version of vixDiskLib, you may install it by running the following:

**Installing a different`vixDiskLib` version**

$ VIX_DIR_PATH="/opt/coriolis/vmware-vix-disklib" $ VIXDISKLIB_TGZ_URL="<VIXDISK_LIB_TGZ_URL_LOCATION>" # From Coriolis' console menu, select 'option 3' for editing <br /># Remove previous vixDiskLib installation: $ rm -rf "$VIX_DIR_PATH/*" $ mkdir /tmp/vix # Download, extract and copy the .tgz: $ wget $VIXDISKLIB_TGZ_URL -O <vddk.tar.gz> $ tar -xzf <vddk.tar.gz> -C /opt/coriolis/vmware-vix-disklib/ --strip-components=2 vmware-vix-disklib-distrib/lib64 # NOTE: validate correct version is installed and symlinks are present: $ ls -l "$VIX_DIR_PATH" ... # NOTE: please remember to confirm 'Restart Coriolis container' option upon exit, for the changes to take effect 

12345678910111213141516 | $ VIX_DIR_PATH="/opt/coriolis/vmware-vix-disklib"$ VIXDISKLIB_TGZ_URL="<VIXDISK_LIB_TGZ_URL_LOCATION>" # From Coriolis' console menu, select 'option 3' for editing <br /># Remove previous vixDiskLib installation:$ rm -rf "$VIX_DIR_PATH/*"$ mkdir /tmp/vix # Download, extract and copy the .tgz:$ wget $VIXDISKLIB_TGZ_URL -O <vddk.tar.gz>$ tar -xzf <vddk.tar.gz> -C /opt/coriolis/vmware-vix-disklib/ \--strip-components=2 vmware-vix-disklib-distrib/lib64 # NOTE: validate correct version is installed and symlinks are present:$ ls -l "$VIX_DIR_PATH" ... # NOTE: please remember to confirm 'Restart Coriolis container' option upon exit, for the changes to take effect   
---|---
