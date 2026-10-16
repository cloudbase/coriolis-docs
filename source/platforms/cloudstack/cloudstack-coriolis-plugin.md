---
title: "CloudStack"
---

# CloudStack

**Coriolis** integrates the platform Plugin on the Appliance itself, this way there is no need for agents to be deployed on platforms to establish the communication between the platform and the Coriolis components. Using this type of architecture, **Coriolis** guarantees the connection to the supported platform set up to be used as either Source or Destination, as long as the requirements are met.

## Scope and limitations

Topic| Notes  
---|---  
Direction| Import into CloudStack only  
Hypervisor| KVM zones; CloudStack **4.21 or newer**  recommended  
Offerings| Disk, minion, and migrated VM offerings must each be pre-created and chosen explicitly in Coriolis settings  
Minion offering| One minion compute offering is used for data replication and for OS morphing (Linux and Windows)  
Disk offering| Must be a custom (flexible-size) offering; fixed-size disk offerings are **not supported**  
OS morphing| Supported for common Linux distributions and Windows; validate in your environment before production use  

## CloudStack prerequisites

Item| Requirement  
---|---  
API access| Coriolis can reach the CloudStack API over HTTPS  
API permissions| Volumes, VMs, templates, offerings, networks, public IPs, firewall, static NAT, snapshots  
Zone| Selected per Transfer; determines templates, offerings, networks, and storage  
Offerings| Custom disk offering plus compute offerings for minion and migrated VM — see [Disk and compute offerings](cloudstack-as-a-destination-cloud.md#disk-and-compute-offerings)  
Templates| Linux: zone cloud-init template (defaults work); Windows: custom WS2022+ template for morphing — see [Recommended Minions](cloudstack-as-a-destination-cloud.md#recommended-minions)  
Primary storage| KVM storage pools mapped in Coriolis storage mappings  
Public IPs| Account can allocate public IPs for temporary workers in the target zone  

### Required CloudStack Permissions

Coriolis requires a CloudStack user with the native **Admin - Read-Only** role, supplemented with the following additional permissions.

These permissions allow Coriolis to perform the operations required for virtual machine migration, including managing compute resources, storage volumes and snapshots, and network connectivity.

| Virtual Machine | Storage | Network |
|:---:|:---:|:---:|
| deployVirtualMachine | createVolume | |
| startVirtualMachine | deleteVolume | associateIpAddress |
| stopVirtualMachine | resizeVolume | disassociateIpAddress |
| updateVirtualMachine | attachVolume | enableStaticNat |
| destroyVirtualMachine | detachVolume | disableStaticNat |
| expungeVirtualMachine | createSnapshot | createFirewallRule |
| addNicToVirtualMachine | deleteSnapshot | deleteFirewallRule |
| listGuestOsMapping | listStoragePools | |

```{note}
The **Admin - Read-Only** role provides the baseline read-only access. The permissions listed above must be granted in addition to that role to enable Coriolis migration operations.
```

## Endpoint connection

Coriolis connection to CloudStack requires a user account that has generated API keys and secrets. For more details, access this CloudStack documentation page: [Using API Key and Secret Key based Authentication](https://docs.cloudstack.apache.org/en/latest/adminguide/accounts.html#using-api-key-and-secret-key-based-authentication)

Create a CloudStack **destination**  endpoint in Coriolis with:

Field| Value  
---|---  
API Endpoint| CloudStack API URL (for example **https://cloudstack.example.com/client/api**)  
API Key| API key for the migration account  
API Secret| Matching API secret  

## CloudStack as a destination cloud

For more information on using CloudStack as a **destination cloud** for Replica/Migration, please check the **[CloudStack as a destination cloud](../cloudstack/cloudstack-as-a-destination-cloud.md)** page.
