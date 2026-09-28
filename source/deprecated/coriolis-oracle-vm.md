---
title: "Coriolis &#8211; Oracle VM &#8211; Getting started"
wp_id: 37594
---

# Coriolis &#8211; Oracle VM &#8211; Getting started

Coriolis® performs software-defined migrations of virtual workloads among different clouds and virtualization solutions at scale, supporting also DRaaS (disaster recovery as a service) scenarios. More information on Coriolis is available [here](https://cloudbase.it/coriolis).

This guide explains how to configure Coriolis for Oracle VM. Note: all the actions executed by Coriolis leverage the standard API provided by the cloud infrastructure, no admin access is required.

### Oracle VM templates

Coriolis needs two VM templates (one with a vanilla Oracle Linux 7 installation and one with Windows Server 2012 R2 or above) that will be used for instantiating temporary workers involved during the replica and migration steps. The templates need **ovmd** (Linux) and Oracle VM PV drivers (Windows) installed for Coriolis to retrieve the assigned IP address via API. For the same purpose, a DHCP service is required in order to assign IPs to the temporary VMs.

An Oracle Linux 7 template is available at <https://cloudbase.it/downloads/OL7_template.tgz> and can be easily imported in Oracle VM manager as described in the [Oracle VM documentation](https://docs.oracle.com/cd/E64076_01/E64082/html/vmusg-repositories-template-import.html):

![](_static/images/OVM_import_template_2.png)

After the import is completed, assign to the template a network with DHCP and outgoing Internet access (direct or via proxy):

![](_static/images/OVM_template_network_2.png)

Note: Windows templates cannot be redistributed due to licensing limitations, please refer to the section “**How to create the Oracle VM worker templates**” for details.

### Configuration

A few configuration settings are needed when using Oracle VM as a target cloud.

Use an editor like _vi_ or _nano_ to edit **/etc/coriolis/coriolis.conf** and replace the following settings accordingly. The parameters refer to the VM templates location and login information, along with the network, pool, and repository to be used when spawning the temporary VMs. The network specified in **migr_network_name** needs to be reachable by Coriolis and the temporary VMs cloned from the templates during a migration need to be able to access Internet resources via HTTP/HTTPS (e.g. yum repositories).

```ini
[oracle_vm_migration_provider]
migr_template_name_map = linux: OracleLinux7_template, windows: WS2012R2_template
migr_template_username = root
migr_template_password = coriolis
migr_network_name = Management
server_pool_name = pool1
repository_name = repo1
# virtual_disk_clone_type can be: THIN_CLONE, SPARSE_COPY, NON_SPARSE_COPY
virtual_disk_clone_type = THIN_CLONE
windows_pv_drivers_url = https://cloudbase.it/downloads/ovm_win_pv_drivers_all_323.zip
```

Set **virtual_disk_clone_type** as described above, based on your preferences and infrastructure requirements. If you opt for thin cloning, ensure that it is supported by your Oracle VM storage.

The **windows_pv_drivers_url** setting is the URL of a zip archive containing the Windows Oracle VM PV drivers to be automatically installed by Coriolis in the Windows VMs migrated from other clouds or virtualization solutions (e.g. VMware). The driver drivers can be obtained from any Windows instance with the Oracle VM PV drivers already installed. The sample URL included here is for reference only.

The configuration file contains also other settings, no other changes are needed for this starting guide.

### Proxy settings

The following section in **/etc/coriolis/coriolis.conf** provides the proxy settings for accessing external resources (e.g. yum or apt repositories):

```ini
[proxy]
url = http://proxy:3128
# Optional proxy credentials
# username =
# password =
# Optional comma separated list of proxy exclusions
# no_proxy =
```

### How to create the Oracle VM worker templates

Two VM templates are needed, one for migrating Linux VMs (any distro) and one for Windows VMs (any version).

#### Linux

Install an Oracle Linux 7 x64 VM with the following settings:

  * Xen HVM PV Drivers domain type
  * 1GB RAM
  * 2 vCPUs
  * 1 vNIC connected to a network reachable from the Coriolis appliance
  * 1 virtual disk (10 GB, sparse allocation)

Perform a minimal system installation. **Do not partition the disk with LVM** , use standard partitioning.

Once done, update the system and install the Unbreakable Enterprise Kernel:

```bash
yum update -y
yum install kernel-uek -y
```

Install the OVM daemon (**ovmd**) and related dependencies. This is needed for Coriolis to automate the configuration of the VMs deployed from the template and obtain their IP address.

```bash
yum install ovmd xenstoreprovider libovmapi ovm-template-config* --enablerepo=ol7_addons -y
yum install lvm2 -y
systemctl enable ovmd
systemctl enable ovm-template-initial-config
```

Once done, shutdown the VM (cleaning the Bash history is optional):

```text
history -c && poweroff
```

Once the VM is powered off, using Oracle VM Manager, disconnect the ISO, clone the VM in a VM template, and provide a name to be used in the Coriolis config file (e.g. _OracleLinux7_template_ in the sample Coriolis config). The VM can now be deleted.

#### Windows

Perform a standard installation of Windows Server 2012 R2 Standard Core with the following settings:

  * Xen HVM PV Drivers domain type
  * 2GB RAM
  * 2 vCPUs
  * 1 vNIC connected to a network reachable from the Coriolis appliance
  * 1 virtual disk (20 GB, sparse allocation)

Once the operating system is installed, add the [Oracle Linux PV drivers](https://www.oracle.com/virtualization/ovm-windows-pv-drivers.html) and configure a WINRM HTTPS listener with basic authentication.

Configuring WINRM can be easily achieved with the following PowerShell script:

```text
wget https://raw.githubusercontent.com/ansible/ansible/devel/examples/scripts/ConfigureRemotingForAnsible.ps1 -UseBasicParsing -OutFile ConfigureRemoting.ps1
powershell -ExecutionPolicy remoteSigned -File ConfigureRemoting.ps1
```

Once done, you can shut down the VM, disconnect the ISO, and clone the VM in a VM template (named _WS2012R2_template_ in the sample Coriolis config) as explained for the Linux case above. The VM can now be deleted.

Notes:

  * The VM can be optionally sysprepped (fully unattended)
  * Ensure that proper Microsoft licensing is available since Coriolis will need to spawn and destroy Windows VMs temporarily during a migration.
