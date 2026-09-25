---
title: "CloudStack as a destination cloud"
wp_id: 44185
---

# CloudStack as a destination cloud

**Coriolis  **provides agentless integration with supported virtualization platforms by running the platform plugin directly on the Coriolis Appliance. This architecture eliminates the need to deploy agents on source or destination platforms and simplifies connectivity and setup.

This document presents how to use Coriolis to replicate or migrate VMs into **Apache CloudStack**. Migrations (CMaaS) and Replicas (DRaaS) follow the same destination requirements and transfer flow described below.

## Scope and limitations

Topic| Notes  
---|---  
Direction| Import into CloudStack only  
Hypervisor| KVM zones; CloudStack **4.21 or newer**  recommended  
Offerings| Disk, minion, and migrated VM offerings must each be pre-created and chosen explicitly in Coriolis settings  
Minion offering| One minion compute offering is used for data replication and for OS morphing (Linux and Windows)  
Disk offering| Must be a custom (flexible-size) offering; fixed-size disk offerings are **not supported**  
OS morphing| Supported for common Linux distributions and Windows; validate in your environment before production use  

## Transfer executions

Steps performed by Coriolis during each transfer execution to CloudStack:

  1. On the **first**  execution for a VM, create empty replica volumes on CloudStack primary storage — one per source disk, sized to match the source. On later executions, reuse the existing replicated volumes when size and storage mapping still match.
  2. On the **first**  execution, create a live snapshot of the source VM disks (handled by the source platform). On later executions, create a new incremental snapshot based on the last successful replica execution.
  3. Deploy a temporary **Linux minion VM**  in the target zone, allocate a public IP with static NAT, and open firewall rules so that Coriolis can reach the minion.
  4. Attach the replicated volumes to the Linux minion and sync disk data from the source snapshot through the minion into the CloudStack volumes.
  5. When all disks are synced, detach the volumes from the minion, delete the temporary minion VM, and release its public IP and firewall rules. Replicated volumes remain on primary storage for the next execution or deployment.

## Deployments

Steps performed by Coriolis when deploying a replica or completing a migration to CloudStack:

  1. Snapshot the replicated volumes on CloudStack so changes can be rolled back in case of deployment failures. By default, new volumes are created from these snapshots for deployment, leaving the original replicated volumes intact for future replica executions.
  2. If **OS morphing**  is enabled, deploy a temporary minion VM matching the guest OS (**Linux template**  for Linux guests, **Windows template**  for Windows guests), attach the deployment volumes, and run OS morphing to adapt the guest for CloudStack/KVM (drivers, networking, cloud-init or cloudbase-init, and related packages).
  3. Detach the volumes from the morphing minion and delete the temporary minion VM.
  4. Deploy the final migrated VM: create a shell VM from the **Linux template** , replace its boot volume with the migrated root disk, attach remaining data disks, map guest networks from the transfer network map, and port VM configuration from the source VM (CPU, RAM, firmware, secure boot, etc.).
  5. Start the migrated VM on CloudStack (unless configured to skip starting migrated instances).

## CloudStack prerequisites

Item| Requirement  
---|---  
API access| Coriolis can reach the CloudStack API over HTTPS  
API permissions| Volumes, VMs, templates, offerings, networks, public IPs, firewall, static NAT, snapshots  
Zone| Selected per Transfer; determines templates, offerings, networks, and storage  
Offerings| Custom disk offering plus compute offerings for minion and migrated VM — see [Disk and compute offerings](#disk-and-compute-offerings)  
Templates| Linux: zone cloud-init template (defaults work); Windows: custom WS2022+ template for morphing — see [Recommended Minions](#recommended-minions)  
Primary storage| KVM storage pools mapped in Coriolis storage mappings  
Public IPs| Account can allocate public IPs for temporary workers in the target zone  

### Required CloudStack Permissions

Coriolis requires a CloudStack user with the native **Admin - Read-Only** role, supplemented with the following additional permissions.

These permissions allow Coriolis to perform the operations required for virtual machine migration, including managing compute resources, storage volumes and snapshots, and network connectivity.

Virtual Machine| Storage| Network  
---|---|---  
deployVirtualMachine startVirtualMachine stopVirtualMachine updateVirtualMachine destroyVirtualMachine expungeVirtualMachine addNicToVirtualMachine
listGuestOsMapping| createVolume  
deleteVolume resizeVolume attachVolume detachVolume createSnapshot deleteSnapshot
listStoragePools| associateIpAddress  
disassociateIpAddress enableStaticNat disableStaticNat createFirewallRule deleteFirewallRule

> **Note:** The **Admin - Read-Only** role provides the baseline read-only access. The permissions listed above must be granted in addition to that role to enable Coriolis migration operations.

## Endpoint connection

Coriolis connection to CloudStack requires a user account that has generated API keys and secrets. For more details, access this CloudStack documentation page: [Using API Key and Secret Key based Authentication](https://docs.cloudstack.apache.org/en/latest/adminguide/accounts.html#using-api-key-and-secret-key-based-authentication)

Create a CloudStack **destination**  endpoint in Coriolis with:

Field| Value  
---|---  
API Endpoint| CloudStack API URL (for example **https://cloudstack.example.com/client/api**)  
API Key| API key for the migration account  
API Secret| Matching API secret  

## Networking and connectivity

  * Temporary minions use a **public IP**  with static NAT. Plan guest networks and IP capacity accordingly.
  * Map each source VM network to a CloudStack guest network in the transfer **network map**.
  * Coriolis must reach each temporary minion public IP on the ports below.

Port| When needed  
---|---  
TCP 22| All migrations (Linux temporary minion)  
TCP 4433, 5566| Disk replication (default data path uses 5566)  
TCP 5986| Windows OS morphing only  

## Recommended minions

Coriolis deploys **temporary minion VMs**  in CloudStack during Transfers and OS morphing. For Linux, pick an existing cloud-init template already available in the zone — custom image build is not required. For Windows OS morphing, prepare and register a dedicated minion template.

> **Windows guests**
> 
> Disk replication always uses the Linux Minion. When OS Morphing WIndows guests, both Linux and Windows templates must be configured.

### Linux temporary worker

**Recommended:**  a default CloudStack **Ubuntu 24.04**  (or newer) cloud-init template already registered in the zone. These templates work **out of the box**  — Coriolis supplies cloud-init userdata at deploy (SSH key, user, networking). You do not need to build or customize a Linux worker image for CloudStack.

Item| Requirement  
---|---  
Template source| Built-in or vendor-supplied CloudStack Linux cloud-init template in the target zone  
OS version| Ubuntu 24.04 LTS or newer; at least as recent as migrated Linux guests when possible  
Used for| Disk replication (all migrations), Linux OS morphing, final VM shell deploy  
In Coriolis, set **Linux template**  to the template name or UUID from your zone dropdown. See [CloudStack cloud-init templates](https://docs.cloudstack.apache.org/en/latest/adminguide/templates/_cloud_init.html) if your zone has no suitable template yet.

### Windows temporary worker

**Recommended:**  Windows Server **2019**  or newer (Standard or Datacenter) with all the VirtIO drivers installed.

Item| Requirement  
---|---  
OS version| WS2019 or newer; must be the **same version or newer**  than the Windows guest being morphed  
Suggested template name| **coriolis-minion-ws2019**  
CloudStack guest OS type| Windows Server 2019 (64-bit) or matching type  
Cloudbase-init| Required — userdata via CloudStack metadata and/or config drive  
WinRM HTTPS| Required on TCP 5986 for OS morphing  
QEMU guest agent| Recommended (included with VirtIO driver pack)  
Used for| Windows OS morphing only — not used for disk replication  
Prepare the golden image, configure cloudbase-init as below, sysprep, and register the template in CloudStack.

#### Cloudbase-init configuration

CloudStack has no API to set the Windows minion password through the QEMU guest agent. Coriolis deploys the morphing minion with **cloudbase-init userdata**  that sets the **Administrator**  password. The template must apply that userdata and configure WinRM HTTPS on every first boot — CloudStack **deployVirtualMachine**  re-runs cloudbase-init on each deploy, so WinRM must be set up through cloudbase-init plugins in the template.

Edit both files on the golden VM (keep **metadata_services  **and **plugins  **aligned):

  * **C:\Program Files\Cloudbase Solutions\Cloudbase-Init\conf\cloudbase-init.conf**  — first boot after deploy
  * **C:\Program Files\Cloudbase Solutions\Cloudbase-Init\conf\cloudbase-init-unattend.conf**  — sysprep only

```ini
[DEFAULT]
username=Administrator
groups=Administrators
inject_user_password=false
first_logon_behaviour=no

metadata_services=cloudbaseinit.metadata.services.configdrive.ConfigDriveService,cloudbaseinit.metadata.services.cloudstack.CloudStack

plugins=cloudbaseinit.plugins.common.mtu.MTUPlugin,cloudbaseinit.plugins.common.sethostname.SetHostNamePlugin,cloudbaseinit.plugins.windows.networkconfig.NetworkConfigPlugin,cloudbaseinit.plugins.windows.licensing.WindowsLicensingPlugin,cloudbaseinit.plugins.common.userdata.UserDataPlugin,cloudbaseinit.plugins.windows.winrmlistener.ConfigWinRMListenerPlugin

winrm_configure_https_listener=true
winrm_configure_http_listener=false
winrm_enable_basic_auth=true
```

Setting| Why  
---|---  
**username=Administrator**|  Coriolis WinRM login is always Administrator  
**UserDataPlugin**|  Applies Coriolis deploy userdata (password below)  
**ConfigWinRMListenerPlugin**  \+ HTTPS| Coriolis requires **https:// <ip>:5986/wsman**; HTTP/5985 is not used  
**winrm_enable_basic_auth=true**|  Required for Coriolis WSMan authentication  
CloudStack + ConfigDrive metadata| Userdata must reach the guest; order services to match your network offering  
The minion guest network offering must deliver userdata via CloudStack metadata (virtual router), config drive (**config-2**  ISO), or both. If you use config drive only, enable **ConfigDrive**  on the network offering.

At deploy, Coriolis sends base64 **#cloud-config**  userdata like:

```yaml
#cloud-config
users:
  - name: Administrator
    passwd: '<generated>'
    primary_group: Administrators
```

#### Seal the template (sysprep)

After configuring cloudbase-init, run sysprep with cloudbase-init’s **Unattend.xml**  and register the stopped VM as a CloudStack template. If cloudbase-init already ran on the golden VM during testing, clear its registry state first so the next deploy is treated as a true first boot (otherwise WinRM may stay on HTTP/5985 only).

```powershell
# Optional — only if cloudbase-init already ran on this VM
Remove-Item -Force -Recurse 'HKLM:\SOFTWARE\Cloudbase Solutions' -ErrorAction SilentlyContinue
# Sysprep (use cloudbase-init Unattend.xml path on your image)
& 'C:\Windows\System32\Sysprep\sysprep.exe' /generalize /oobe /shutdown `
  '/unattend:C:\Program Files\Cloudbase Solutions\Cloudbase-Init\conf\Unattend.xml'
```

Validate after a test deploy from the template:

```powershell
winrm enumerate winrm/config/listener
Get-Content 'C:\Program Files\Cloudbase Solutions\Cloudbase-Init\log\cloudbase-init.log'
```

Expect an **HTTPS listener on 5986** , **UserDataPlugin**  applying the Administrator password, and no **SetUserPasswordPlugin**  errors.

### Recommended compute and disk offerings

Suggested CloudStack offering names (any active UUID or name works if requirements are met):

Role| Suggested name| Type| Notes  
---|---|---|---  
Replica disks| **Coriolis custom disk**|  Custom disk offering| Flexible size; one offering for all replica volumes  
Temporary workers| **Coriolis minion**|  Custom compute offering| Flexible CPU/RAM; bounds ≥ 2 vCPU / 2048 MB  
Final migrated VM| **Coriolis migrated VM**|  Custom compute offering| Flexible CPU/RAM; bounds for your largest source VMs  

### Deploy sizing (flexible custom offerings)

Role| CPU / RAM at deploy  
---|---  
Linux or Windows temporary minion| 2 vCPU, 2048 MB RAM  
Final migrated VM| Matches the source VM  
Fixed-size compute offerings use CloudStack’s configured CPU and RAM. Fixed-size **disk**  offerings cannot be used for replica volumes.

## Disk and compute offerings

Create three offerings in CloudStack, then map them to the Coriolis destination target environment (UI or API). Coriolis does not choose an offering for you when several exist in a zone.

### The three offerings

Coriolis setting| Create in CloudStack| Purpose  
---|---|---  
Disk offering| Custom (flexible-size) disk offering| Replica volumes during data replication  
Minion service offering| Compute offering| Temporary workers (replication and OS morphing)  
Migrated VM service offering| Compute offering| Final migrated VM after cutover  
See [Recommended minions](#recommended-minions) for template choices, suggested offering names, and deploy sizing.

## Target environment options

Destination target environment fields for CloudStack (UI or API):

Option| Required| Notes  
---|---|---  
Zone| Yes| Target CloudStack zone  
Linux template| Yes| Zone cloud-init template; default CloudStack templates work out of the box  
Windows template| Windows morphing| WS2019+ with [Cloudbase-init configuration](#cloudbase-init-configuration); not used for data replication  
Disk offering| Yes| Custom flexible disk offering  
Minion service offering| Yes| Temporary minions  
Migrated VM service offering| For deployments| Final VM  
Storage mappings| Yes| Each source disk → primary storage pool  
Network map| Yes| Each source network → guest network  
Disk controller| No| Default recommended: virtio  
Guest OS type| No| Optional override on final VM  
Advanced migrated VM options| No| Optional extra VM settings at deploy  
Windows VirtIO ISO / Cloudbase-Init URLs| Windows morphing| URLs must be reachable from the temporary minion  
Use floating IP| No| Associate a public IP on the final VM (enabled by default)
