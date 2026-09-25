---
title: "Microsoft Hyper-V Coriolis Plugin"
wp_id: 38511
---

# Microsoft Hyper-V Coriolis Plugin

**Coriolis** integrates the platform Plugin on the Appliance itself, this way there is no need for agents to be deployed on platforms to establish the communication between the platform and the Coriolis components. Using this type of architecture, Coriolis guarantees the connection to the supported platform set up to be used as either Source or Destination, as long as the requirements are met.

This section describes the functionality available via Coriolis' Hyper-V plugin, which enables Coriolis to both migrate (CMaaS) and replicate (DRaaS) instances from Hyper-V.

[![](_static/images/hyper-v-source.jpg)](https://i0.wp.com/cloudbase.it/wp-content/uploads/2022/04/hyper-v-source.jpg?ssl=1)

## Hyper-V Coriolis endpoint

When creating the Hyper-V endpoint in Coriolis, a local account must be used for the WinRM connection between the Coriolis appliance and the Hyper-V node, as well as the RCT password, as detailed below.

Using a domain account for the WinRM connectivity is subject to additional configuration at the domain level to allow such access. Please refer to the Microsoft documentation for further details on how this can be achieved.

[![](_static/images/hv.png)](https://i0.wp.com/cloudbase.it/wp-content/uploads/2025/05/hv.png?ssl=1)

## Deployment requirements and supported Hyper-V instances

### Deployment requirements

The Hyper-V plugin supports Windows hosts starting from Windows Server 2016 and up to Windows Server 2025.

The worker components of Coriolis need HTTPS-enabled WinRM access to the Hyper-V host (port 5986 by default).

When using Microsoft Hyper-V as a source platform, a lightweight RCT service must be initially set up by the user. The installation and configuration process for the service is explained on this page.

Coriolis will use the following connections when interacting with the Hyper-V host(s):

  * WinRM must be enabled and configured as detailed below.
  * RCT Service. The RCT service is securely accessed through x509 certificates, which are transparent to the user.



### WinRM enablement

On the Microsoft Hyper-V (source) hosts, WinRM can be easily enabled by running one of our Coriolis helper scripts. Keep in mind that this will work **only** **with self-signed certificates**.

  * First, the script has to be downloaded on the Windows Server VM



```text
$URL="https://raw.githubusercontent.com/cloudbase/coriolis-resources/master/windows/winrm-gen.ps1"

$Path="C:\<Path-to-file>\winrm-gen.ps1"

Invoke-Webrequest -URI $URL -OutFile $Path
```

  * Next, navigate to the directory where the script resides and run it



cd C:\<Path-to-file>\ .\winrm-gen.ps1

```text
cd C:\<Path-to-file>\

.\winrm-gen.ps1
```

During the installation process, outputs are provided with the current status of the running task. Once it finishes, the message 'Done' will be shown. Optionally when using**SSL** the **computer name** can be specified.

### Manual configuration of WinRM with self-signed SSL certificate

The steps required to configure and **enable WinRM HTTPS** service and configure **Windows Firewall** to allow **WinRM HTTPS** port **5986.**

This can be achieved by running:

```text
$winrm quickconfig -transport:https
```

The above command can be tested afterward with the following:

> #Check if WinRM is enabled and configured
>  $winrm get winrm/config
>
>  #Locate WinRM listeners and addresses
>  $winrm enumerate winrm/config/listener
>
>  #Display WinRM Firewall rules
>  Get-NetFirewallPortFilter | Where-Object -Property LocalPort -EQ 5986  
>
>  #Expected output
>  Protocol : TCP
>  LocalPort : 5986
>  RemotePort : Any
>  IcmpType : Any
>  DynamicTarget : Any

Enable the basic authentication for WinRM, from the command prompt using the following command:

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

In a test environment, **WinRM** can be used with **self-signed SSL certificates**.

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

#### Make sure that WinRM Basic Authentication is enabled, using the following steps

  * Check if it is enabled: "winrm get winrm/config/Service” The output should be similar to this:



> AllowUnencrypted = false
> 
> Auth
> 
> Basic = false
> 
> Kerberos = true
> 
> Negotiate = true
> 
> Certificate = true
> 
> CredSSP = false
> 
> CbtHardeningLevel = Relaxed 

 

  * Enable the auth Basic authentication: "winrm set winrm/config/Service/auth @{Basic="true”}” Now, if we check again, it should be “Basic = true” and the validation should pass.



## Hyper-V as a source cloud

### Migrating (CMaaS) from Hyper-V

Migrations from Hyper-V operate in the same way Replicas do and thus entail the same requirements and steps described below.

### Replicating (DRaaS) from Hyper-V

**Input** : the name or GUID of the VM.

NOTE! Please consider reviewing the general steps recommended to be performed before creating a migration for a VM from Hyper-V in the dedicated documentation titled "Preparing a VM for migration/replication".

#### Steps performed by Coriolis

  1. read the configuration of the instance on the source Hyper-V (compute specs, disks, etc…) using PowerShell cmdlets through WinRM
  2. create an app-consistent snapshot (Checkpoint) of the VM
  3. export the data of the VM's disk(s) through the RCT service



After the above steps are completed, the migration process proceeds with the steps that are defined in the selected destination cloud plugin.

### OSMorphing steps taken when migrating from Hyper-V

For exported VMs, Coriolis will take the following OSMorphing steps as part of the migration process from Hyper-V:

#### Linux

  * refer to the destination cloud for the tools that are being installed
  * optionally, the user can remove the LIS components from the destination instance, if no longer required by the platform



#### Windows

  * no OSMorphing steps are taken as the integration services are part of the Windows guest OS itself



For more information regarding the Coriolis Worker template, please check the **[Coriolis Temporary Migration Worker](https://cloudbase.it/coriolis-temporary-migration-worker) **page.

### RCT service installation and configuration procedure

The RCT (Resilient Change Tracking) lightweight service  (<https://github.com/cloudbase/rct-service>) is an in-house project by Cloudbase that exposes a REST Service for the Hyper-V RCT to obtain the RCT info from a given virtual disk and stream the data remotely over an authenticated HTTPS channel. It allows live and incremental snapshots of VMs running on Hyper-V servers 2016 and above.

As prerequisites, the Windows machine must have the Hyper-V features enabled.

#### Download the binary and extract the .zip file

#### RCT binary download

> [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
>
>  $cli = New-Object "System.Net.WebClient"
>  $cli.DownloadFile("[https://cloudbase.it/downloads/app/hyper-v/rct-service.zip"](https://cloudbase.it/downloads/app/hyper-v/rct-service.zip%22), "$env:USERPROFILE\rct-service.zip")
>
>  Expand-Archive $env:USERPROFILE\rct-service.zip -DestinationPath $env:USERPROFILE\rct 

#### Generating the certificates

Generate the X509 certificates for encryption of data transfer and store them in $env:USERPROFILE\rct. Alternative methods of X509 certs generation can be used, in this case, we are using a bundle that generates a CA, server cert, and client cert altogether. The CA allows client certificate verification. By default, local hostname and IPs are added to the certificate, in addition, localhost and 127.0.0.1 are added in the command line.

#### Download the executable and expand the archive file

Download the generator and extract the files:

> $cli.DownloadFile("[http://wiki.cloudbase.it/_media/gen-certs.zip"](http://wiki.cloudbase.it/_media/gen-certs.zip%22), "$env:USERPROFILE\gen-certs.zip")
> 
>
> Expand-Archive "$env:USERPROFILE\gen-certs.zip" -DestinationPath "$env:USERPROFILE\rct"

#### Generate certificates and store them into _$env:USERPROFILE\rct_

#### Generate X509 certificates

```text
& "$env:USERPROFILE\rct\gen-certs.exe" -certificate-hosts "127.0.0.1,localhost" -output-dir "$env:USERPROFILE\rct" 
```

#### Generate Rocket.toml file

1) Note down the full path to the X509 certificates folder

#### Get certificates full path

ls $env:USERPROFILE\rct 

```text
ls $env:USERPROFILE\rct 
```

In our case, it is _C:/Users/Administrator/rct/_

#### Create an array variable

2) create a config file array variable and replace accordingly the desired _auth_key/ port/ certs &key path_, as follows:

```text
$config = @"
[global]
# Use something else
auth_key = "swordfish"
address = "0.0.0.0"
port = 6677
 
[global.tls]
certs = "C:/Users/Administrator/rct/srv-pub.pem"
key = "C:/Users/Administrator/rct/srv-key.pem"
"@
```

#### Generate the config file

#### Create Rocket.toml file

```powershell
Set-Content C:\Rocket.toml $config
```

We are using forward slashes in the config!

Depending on your client, you may need to concatenate the **ca-pub.pem** with **srv-pub.pem**

#### Allow RCT service and port in Firewall

#### Enable RCT port in the firewall

```text
New-NetFirewallRule -DisplayName rct -Direction Inbound -LocalPort 6677 -Protocol TCP -Action Allow 
```

#### Create the RCT service

Enable RCT service to start automatically, and manually start the service for first-time use:

> $params = @{
> Name = "rct-service"
> BinaryPathName = '"C:\Users\Administrator\rct\OpenStackService.exe" rct-service "C:\Users\Administrator\rct\rct-service.exe"'
> DisplayName = "rct-service"
> StartupType = "Automatic"
> }
> New-Service @params

### Hyper-V connection parameters

Supported Actions: | Migration Source - Replica Source  
|  Comments   
---|---|---  
Plugin identifier| **hyper-v**|  Identifies the plugin. Used for the **- provider** CLI parameter  
Credentials needed| Admin credentials and WinRM/HTTPS access to the Hyper-V host| Necessary credentials to give to Coriolis  
Deployment requirements| Only Hyper-V hosts running Windows 10/Server 2016 or later are supported. Coriolis worker component(s) need network access to the Hyper-V host| Coriolis deployment and environment connectivity requirements  
Source disk export requirements| A lightweight RCT service must be installed and configured on the source Hyper-V host(s)| Requirements to use the replica export (DRaaS source) features  
Instance identification scheme| Name or GUID| How instances to migrate/replicate are identified on a source cloud handled by this plugin  
Network identification scheme| Names of Virtual Switches| How networks are identified by the plugin. Required for the **network_map** field of the **- destination-environment**  
Storage identification scheme| IDs of QoS Policies| How storage backends are identified by the plugin. Required for the **storage_map** field of the **- destination-environment**  

#### Example of connection info JSON to be passed to the Hyper-V plugin

To connect to Hyper-V to perform a migration/replica from it, the following connection parameters are required:

> {
>  "host": "10.7.200.100",
>  "username": "Administrator",
>  "password": "Passw0rd",
>  "port": 5986,
>  "allow_untrusted": true,
>  "rct_port": 6677,
>  "rct_password": "swordfish"
>  }

Each parameter represents:

  * **host (string)** : resolvable hostname or IPv4/v6 address of the Hyper-V host
  * **username (string)** : username for the Windows host. Can include domain as a prefix (with backslashes)
  * **password (string)** : password for the above user
  * **port (integer)** : port number the Hyper-V server has a WinRM Listener configured to listen on
  * **allow_untrusted (boolean)** : whether or not to accept connecting to hosts with a self-signed certificate
  * **rct_password (string)** : _auth_key_ used when generating Rocket.toml file as described in the RCT setup section of this document
  * **rct_port (integer)** : port number the Hyper-V server has RCT Listener configured as used in Rocket.toml file generation



For replication, the following can be used:

```json
{
     "fallback_to_crash_consistent_snapshots": true,
     "verify_rct_server": false
 }
```

Each parameter represents:

  * **fallback_to_crash_consistent_snapshots (string)** - Use crash-consistent snapshots if Hyper-V enablement is not installed in the guest VM
  * **verify_rct_server (string)** - Verify the SSL certificate for RCT service. Set to No if using a self-signed certificate.


