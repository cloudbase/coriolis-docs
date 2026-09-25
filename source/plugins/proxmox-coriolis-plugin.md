---
title: "Proxmox Coriolis Plugin"
wp_id: 42897
---

# Proxmox Coriolis Plugin

**Coriolis** integrates the platform Plugin on the Appliance itself, this way there is no need for agents to be deployed on platforms to establish the communication between the platform and the Coriolis components. Using this type of architecture, Coriolis guarantees the connection to the supported platform set up to be used as Destination, as long as the requirements are met.

Coriolis supports Proxmox VE environments starting from version 8.0 and is compatible with newer releases up to 9.1. From these, the EOL versions are not actively tested and may experience issues.

![](_static/images/proxmox-target.png)

### Proxmox as a destination cloud

For more information on using Proxmox as a **destination cloud** for Replica/MIgration, please check the **[Proxmox as a destination cloud](https://cloudbase.it/proxmox-as-a-destination-cloud)** page.

### Proxmox connection parameters

In order to connect to an Proxmox cloud to perform a migration/replica to that cloud, the following connection parameters are required:

![](_static/images/proxmox_endpoint.png)

#### Example of connection info JSON to be passed to the Proxmox plugin

```json
{
     "name": "Proxmox",
     "coriolis_regions": "Public",
     "host": "10.8.17.240",
     "port": 8006,
     "protocol": "https"
     "username": "root",
     "password": "SeKr3t",
     "authentication_realm": "pam"
     "allow_untrusted": false
 }
```

Each parameter represents:

  * **Name(string)** - the name that will be known only to Coriolis
  * **host (string)** - the address or resolvable domain name of the Proxmox host
  * **port (integer)** - the port on the **host**  to which to connect to
  * **username (string)** - the username of the Proxmox user to login with
  * **password (string)** - the password of the Proxmox user to login with
  * **allow_untrusted (boolean)** -  whether to skip certificate verification if the Proxmox endpoint has self-signed certificates (default is **false**)
  * **authentication_realm** - authentication realm to use for making API calls (default is 'pam')
  * **protocol** - the port to connect the Proxmox API through
  * **coriolis-regions** - optional list of Coriolis regions the Endpoint should be mapped to



When using hostnames for the Proxmox hosts, Coriolis needs to be able to resolve them.
