---
title: "Coriolis Architecture"
wp_id: 38751
---

# Coriolis Architecture

## Key design decisions

There were several key design decisions made regarding Coriolis that set the project apart:

  * **service-oriented** : Coriolis offers Cloud Migration and Disaster Recovery as a Service (CMaaS/DRaaS), its HTTP-based REST API allowing for migration/recovery jobs to be created, scheduled, queried, and halted on the fly from both the bundled Web GUI, Python CLI client, or third-party applications
  * **scalability** : Coriolis was designed to scale horizontally to accommodate migration jobs, both small and large. Mass migrations are possible from any supported source clouds to any target ones, without any software limitations.
  * **pluggable** : The Coriolis components that interact with the source/destination platforms come in plugin form, allowing the deployment of Coriolis to best suit one's needs. As an added benefit, newly supported migration/recovery platforms may be added with ease
  * **no agent required** : using Coriolis does not necessitate any sort of agent being installed into the existing systems, be it a VM agent for the VMs which are being migrated/recovered, or any agent on the system hosting the VMs
  * **public APIs only** : during all operations, Coriolis only leverages standard user credentials and publicly available APIs of the platforms in question, no privileged accounts or access to platform internals is required!
  * **multi-tenancy** : Coriolis leverages Keystone for its identity needs, allowing for all of the multi-tenancy-related features Keystone offers (users, tenants, roles, pluggable auth (via LDAP/OAuth))
  * resistance to transient failures: all the operations Coriolis performs are retried atomically to prevent a minor network hiccup or similar anomaly from stopping a multi-VM migration
  * **clean operation** : although Coriolis may make use of temporary resources on the source or destination platforms in the migration process, it ensures proper cleanup is performed and environments are left in pristine condition, regardless of whether the operation was successful or an error was encountered
  * **built like an OpenStack project** : Coriolis is built on the same high-level technologies and libraries that OpenStack components are built of. Thus, Coriolis is written entirely in Python, relies on a Keystone service for all its identity needs, and leverages RabbitMQ (or some other AMQP implementation supported by **oslo_messaging**) for cross-component communications, stores state in a SQL relational database (or anything supported by **oslo_db**), and so on.



## Recovery Point Objective & Recovery Time Objective

Before creating a Migration or a Replica Deployment, consider the two most important parameters of a data protection plan and disaster recovery strategy: Recovery Point Objective & Recovery Time Objective. For more information, please check the **[RPO& RTO documentation](https://cloudbase.it/rpo-rto)**.

## Modes

Coriolis has two distinct modes of operation: a one-off 'move' of an instance from one platform to another ("migrations"), and continuous background sync between the state a VM on a source cloud to storage elements on the destination cloud, which are ready to deploy in case of disaster ("replicas") 

For more information regarding Coriolis Modes, please check the **[Coriolis Replica/Migration Architecture document](https://cloudbase.it/coriolis-replica-architecture/)**.

## High-level architectural overview

At a high level, Coriolis' codebase can be split up into three separate logical components:

  * **Coriolis Core** : the cloud-agnostic core of the project, responsible for creating, scheduling, and managing the lifecycle of the migration/recovery jobs
  * **Source Plugins** : these plugins implement the cloud-specific operations needed to migrate/recover an instance _from  _a certain cloud platform
  * **Destination Plugins** :  these plugins implement the cloud-specific operations needed to migrate/recover an instance _to  _a certain cloud platform 



It is worth noting that both the source and destination plugins are completely decoupled Python modules that get loaded and called by Coriolis Core. Due to this decoupling, the following advantages arise:

  * adding a source plugin for a cloud "X" will automatically mean that all transitions from X to any other cloud with an existing destination plugin are supported (and vice-versa for adding a new destination plugin)
  * source and destination plugins are developed separately, thus, a platform may be supported only as a source or a destination to accommodate specific use cases



For reference, the image below showcases a more detailed architectural overview of Coriolis' deployed components:

[![](_static/images/333.jpg)](https://i0.wp.com/cloudbase.it/wp-content/uploads/2020/05/333.jpg?ssl=1)

## TLS encryption for Coriolis REST API

All Coriolis services and internal communications leverage TLS encryption to ensure a secure channel at all levels.

When exposing the Coriolis REST API for external/remote access, Coriolis will use its own internal PKI mechanism to generate a local CA.

Once the Coriolis endpoint is exposed, the user can download the CA certificate by accessing the URL format below:

```text
http://APPLIANCE_IP:9001/coriolis-ca.crt
```

When using the**coriolis CLI tool** , besides having to source keystone authentication information, the CA certificate will also need to be passed.

Users can either export the CA’s path in the **OS_CACERT** environment variable using:

```bash
export OS_CACERT="/root/coriolis-ca.crt"
coriolis endpoint list
```

or have it passed to the client calls using the **- -os-cacert** option:

coriolis \--os-cacert /root/coriolis-ca.crt endpoint list

**IMPORTANT!** Coriolis appliance access, including services exposure, must be strictly controlled at the network level. Access should be granted only to particular connections or IPs.
