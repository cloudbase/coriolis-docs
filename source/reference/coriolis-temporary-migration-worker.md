---
title: "Coriolis Temporary Migration Worker"
wp_id: 38904
---

# Coriolis Temporary Migration Worker

## Introduction
The Coriolis Temporary Migration worker is a temporary VM created on the destination platform to perform tasks such as transferring data and installing platform-specific drivers. After the process is complete, the temporary worker VM is deleted.

Linux and Windows OS images must be present on the destination platform for the temporary worker to boot and perform the tasks.

In a situation of Replicating/Migrating a Linux VM, only a Linux template will be required, as both **Disk cloning** and **OSMorphing** processes use Linux.

NOTE! When migrating a **Windows VM** , both **Linux and Windows templates** have to be specified, as **Disk cloning** is performed using the Linux template and **OSMorphing** is performed using the Windows template.

## Linux Temporary Migration Worker

In the case of Linux OS images, we recommend using **Ubuntu Server 24.04 LTS (or newer)** , or **Oracle Linux Server 9 (or newer).** Both distributions have cloud images provided by their vendors, which can be used as-is, without any modifications.

## Windows Temporary Migration Worker

When migrating Windows VMs, the Windows template used must be of an equal or later version than the guests being migrated, as the Windows image servicing tools are not forward-compatible.

**NOTE!** For all Windows VM Migration/Replication, the **System Language** used in the Windows Template must be set to **English**.

For the Windows template VM used by Coriolis' worker on all supported Cloud Endpoints, the following are required:

  * install the latest Windows updates and reboot the system to complete the installation
  * install the virtualization drivers as well as the corresponding guest VM agent 
    * The agent can be either the Qemu guest agent or the VMware Tools, to ensure that the platform will be able to fetch the network configuration of the temporary worker spawned from this template
  * install **cloudbase-init**
    * Coriolis relies on the default cloudbase-init username as "**Admin**". The "**Admin**" account must not be disabled in the temporary worker image.
  * configure and enable **WinRM HTTPS** service**,** and configure **Windows Firewall** to allow **WinRM HTTPS** port **5986**
    * The helper script mentioned below will handle this configuration as well.
    * alternatively, both can be enabled by running the following command in a PowerShell session: 

```text
$winrm quickconfig -transport:https
```

  * the above command can be tested afterward with the following:

```powershell
#Check if WinRM is enabled and configured
$winrm get winrm/config

#Locate WinRM listeners and addresses
$winrm enumerate winrm/config/listener

#Display WinRM Firewall rules
$Get-NetFirewallRule -DisplayGroup "Windows Remote Management" | Get-NetFirewallPortFilter | Format-Table
#Output
Protocol LocalPort RemotePort IcmpType DynamicTarget
 
 TCP      5986      Any        Any      Any
 TCP      5986      Any        Any      Any
```

Enable the basic authentication for WinRM from the command prompt using the following command:

```bash
$ winrm set winrm/config/service/auth '@{Basic="true"}'

# Validate the service settings
$ winrm get winrm/config/service/Auth
Auth
    Basic = true
    Kerberos = true
    Negotiate = true
    Certificate = false
    CredSSP = false
    CbtHardeningLevel = Relaxed
```

### Manual configuration of WinRM with a self-signed SSL certificate

In a test environment, **WinRM** can be used with **self-signed SSL certificates**.

Note that this method is not recommended, and newer Windows editions no longer support this method.

  * Creating the self-signed certificate on the destination machine.

```text
New-SelfSignedCertificate -Subject 'CN=servername.domain.com' -TextExtension '2.5.29.37={text}1.3.6.1.5.5.7.3.1'
```

  * Configuring the server’s WinRM web server (listener) to use the self-signed certificate for authentication.

```text
winrm create winrm/config/Listener?Address=*+Transport=HTTPS '@{Hostname="servername.domain.com"; CertificateThumbprint="<cert thumbprint here>"}'
```

  * Opening the appropriate ports on the destination machine’s Windows firewall**:**

```text
$FirewallParam = @{ 
      DisplayName = 'Windows Remote Management (HTTPS-In)'
      Direction = 'Inbound' 
      LocalPort = 5986 
      Protocol = 'TCP' 
      Action = 'Allow' 
      Program = 'System' 
} 
New-NetFirewallRule @FirewallParam
```

  * Executing a command to initiate a remote connection on the client using a PowerShell cmdlet like **Enter-PSSession**.

More details regarding **WinRM** are available on the **[Microsoft documentation page](https://docs.microsoft.com/en-us/windows/win32/winrm/portal)**.

* * *

#### Test the connection

winrs tool from Windows can be used to test the connection, recommended to be done from another Windows instance against the running Windows OS to be set as a template.

```text
winrs -r:https://servername:5986 -u:user_name -p:password servername
```

### Helper script to enable WinRM with a self-signed SSL certificate

WinRM can also be enabled by running one of our Coriolis helper scripts. Keep in mind that this will work **only** **with Self Signed Certificates**.

  * First, the script has to be downloaded on the Windows Server VM

```text
$URL="https://raw.githubusercontent.com/cloudbase/coriolis-resources/master/windows/winrm-gen.ps1"

$Path="C:\<Path-to-file>\winrm-gen.ps1"

Invoke-Webrequest -URI $URL -OutFile $Path
```

  * Next, navigate to the directory where the script resides and run it

```text
cd C:\<Path-to-file>\

.\winrm-gen.ps1
```

During the installation process, outputs are provided with the current status of the running task. Once it finishes, the message 'Done' will be shown.

Optionally, when using **SSL**, the **computer name** can be specified.

## Other considerations

For **Oracle destination** platforms, the Linux **temporary migration worker** image we recommend using is **Oracle Linux 9 and above**.

For **Microsoft Azure/AzureStack** **destination** platforms, we recommend using **Ubuntu Server 24.04** or newer as **Linux temporary migration workers**.

If the target platform does not allow for maintaining the same MAC address, or the user asks Coriolis to change the MAC address, all network interface naming **udev** rules should be disabled.

The Windows templates must be created based on the above instructions, or consider our **[Windows Cloud images](https://cloudbase.it/windows-cloud-images/)** offering, which can also be used for production workloads.
