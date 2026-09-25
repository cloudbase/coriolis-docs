---
title: "Coriolis OVM exporter"
wp_id: 40248
---

# Coriolis OVM exporter

**Coriolis OVM Exporter** is an **open-source application** that augments Oracle VM to enable efficient **incremental backups** of virtual machine disks hosted on reflink (Data Block Sharing) capable filesystems. At the moment, this means OCFS2 backed data stores. 

Coriolis OVM exporter is installed as an additional service on each individual compute node inside the OVM cluster and presents a simple REST API that allows you to create, delete and compare snapshots for virtual machines.

The Coriolis OVM Exporter service has been integrated with Coriolis to efficiently and safely move the virtual machines from OVM to any of the supported destinations, without any kind of interruption to business continuity on the source.

Coriolis has two options when exporting Oracle VM instances:

  * A generic solution that relies exclusively on OVM provided APIs
  * Coriolis OVM Exporter



The **generic solution** will create disk snapshots using OVM APIs. Those snapshots get attached to a temporary worker instance in the OVM environment as data disks. At this point, Coriolis will read each disk in fixed-size chunks, and create checksums for each individual chunk. This information will then be stored and compared to a later snapshot of the same disks.

In contrast, **Coriolis OVM Exporter** does not need to undergo such time-consuming and expensive computations and does not require any temporary resources to be spun up in your OVM cluster. It only requires the **Coriolis OVM Exporter** service to be available on your compute nodes. It uses **[reflinks](https://blogs.oracle.com/linux/xfs-data-block-sharing-reflink)** to create crash-consistent snapshots, and **[fiemap](https://www.kernel.org/doc/Documentation/filesystems/fiemap.txt)** to compare the differences between snapshots.   
This way we can do **efficient incremental backups** by simply **copying only what has changed** from a previous replica run.

[![](_static/images/ovm-exporter-no.jpg)](https://i0.wp.com/cloudbase.it/wp-content/uploads/2021/05/ovm-exporter-no.jpg?ssl=1)[![](_static/images/ovm-exporter1.jpg)](https://i0.wp.com/cloudbase.it/wp-content/uploads/2021/05/ovm-exporter1.jpg?ssl=1)

**Toggling** between the **generic solution** and **Coriolis OVM Exporter** is displayed above.

### Installing and Configuring Coriolis OVM Exporter

In order to be able to use the Coriolis feature of OVM Exporter, the service must exist on the compute node on which the virtual machine that is to be exported, resides.

The following steps will provide guidance on how to configure and run the Coriolis OVM Exporter service on a compute node. These steps must be carried out on each and all OVM compute nodes that are managed by OVM

1\. Establish connection to the compute node and navigate to the following path:

cd /usr/local/bin/

```text
cd /usr/local/bin/
```
  
2\. At this point you can choose to **build** Coriolis OVM Exporter yourself or **download** the pre-compiled binary from GitHub. For build information, please refer to the project**[README file](https://github.com/cloudbase/coriolis-ovm-exporter)** available on GitHub. We will focus on using the pre-compiled binary for the remainder of this article:

```text
wget https://github.com/cloudbase/coriolis-ovm-exporter/releases/download/v0.1/coriolis-ovm-exporter 
```
  
3\. Set the newly downloaded file as executable

```text
chmod +x /usr/local/bin/coriolis-ovm-exporter
```
  
4\. Create a new configuration directory and navigate to its path

```text
mkdir /etc/coriolis-ovm-exporter && cd /etc/coriolis-ovm-exporter
```
  
5\. Coriolis uses an encrypted connection to the Coriolis OVM Exporter agent, and thus an SSL certificate is required. If you decide to use **self-signed certificates** , make sure you enable "**Allow insecure** " in the Endpoint connection information for your source cloud (**[Coriolis Endpoint page](https://cloudbase.it/coriolis-endpoints)**).

The certificated from a trusted third-party authority or self-signed user-generated certificates must be copied to the newly-created directory.

6\. Under the same directory, create a configuration file named **config.toml** using the following example

```ini
vi confing.toml

# Path on disk to the database file the exporter will use.
 db_file = "/etc/coriolis-ovm-exporter/exporter.db"

# This is the base URL to your OVM manager. We will use this to
# authenticate login requests. Make sure this matches the manager
# that this node belongs to.
#
# NOTE: Setting this is <em>OPTIONAL</em>. If this setting is omitted, the
# exporter will attempt to fetch the manager IP from the ovs-agent
# database.
# ovm_endpoint = "https://your-ovm-api-server.example:7002"

[jwt]
# Obviously, this secret needs to be changed
 secret = "yoidthOcBauphFeykCotdidNorjAnAtGhonsabShegAtfexbavlyakPak4SletEd"

[api]
 bind = "0.0.0.0"
 port = 5544
     [api.tls]
     # These settings are required
     certificate = "/etc/coriolis-ovm-exporter/srv-pub.pem"
     key = "/etc/coriolis-ovm-exporter/srv-key.pem"
     ca_certificate = "/etc/coriolis-ovm-exporter/ca-pub.pem"
```
  
7\. Once the configuration file is created and the parameters are set, install the startup script from one of the examples available **[here](https://github.com/cloudbase/coriolis-ovm-exporter/tree/main/contrib)**

a. If the chosen option is upstart, follow the instructions

```text
#navigate to the following path to create the configuration file
cd /etc/init

#create the configuration file using the example mentioned above
vi coriolis-ovm-exporter.conf

#start the Coriolis OVM Exporter service
start coriolis-ovm-exporter
```
  
b. If you're running systemd instead of upstart, follow the instructions

```bash
#navigate to one of the following paths tp create the configuration file
cd /lib/systemd/system

or

cd /etc/systemd/system

#create the configuration file using the example mentioned above
vi coriolis-ovm-exporter.service

#reload the daemon and start the Coriolis OVM Exporter service
systemctl daemon-reload
systemctl start coriolis-ovm-exporter
```
  
After the **Coriolis OVM Exporter service** has been configured and is running on the **OVM compute nodes** , you can return to Coriolis and start a Replica/Migration using the OVM Exporter option.
