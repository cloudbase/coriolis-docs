---
title: "Working with the Coriolis All-in-One Appliance"
wp_id: 38854
---

# Working with the Coriolis All-in-One Appliance

## Login and API access

The containers in the appliance are configured to use localhost networking, which means they all share the host's network interface(s), and can thus be reached on the hosts' IP address(es) at the following ports:

  * Keystone - 5000
  * Coriolis API - 7667
  * Web UI - 80/443 - port 80 automatically escalates to HTTPS on 443, the **self-signed** HTTPS certificate is unique to the appliance

## Technical details and container components

The Coriolis appliance is built on top of an Ubuntu Server LTS host, with all of the services required to run or support Coriolis being deployed and run as Docker containers.

The OpenStack components Coriolis leverages (Keystone for multitenancy and Barbican for secret management) and other supporting services (such as RabbitMQ and MariaDB) are deployed using Kolla.

The containers for each of the Coriolis services are the following:

  * **coriolis-api** - container hosting the Coriolis API service
  * **coriolis-conductor** - container hosting the Coriolis conductor service, which connects the Coriolis components
  * **coriolis-worker** - container for the Coriolis worker service, which interacts with the source/target clouds and executes the tasks needed to perform the migration/replication
  * **coriolis-web-proxy**  - container running an Apache service serving as a proxy for the Coriolis UI. All API requests for the underlying Keystone/Barbican/Coriolis API should be proxied through this container
  * **coriolis-web** - container hosting the Coriolis UI
  * **coriolis-replica-cron** - container used for the Coriolis replica functionality
  * **coriolis-logger** - container with the centralized Coriolis logging component. It used influxdb backend.
  * **coriolis-licensing-server**  - container running the licensing server

When running Docker commands, the containers may be referenced simply by their names (coriolis-api, coriolis-conductor, etc…)

The rest of the supporting services are also deployed as containers using Kolla:

  * **keystone** - container running the OpenStack identity service which is used by Coriolis
  * **barbican_worker** - container running the Barbican worker - Barbican is an Openstack service that is used to store sensitive data such as cloud connection info
  * **barbican_keystone_listener** - container for the Barbican Keystone listener
  * **barbican_api** - container for the Barbican API
  * **rabbitmq** - the container hosting a RabbitMQ server
  * **mariadb** - the container hosting the database
  * **cron** - container for the time-based job scheduler
  * **kolla_toolbox** - contains the Kolla utilities
  * **fluentd** - container running the logging service for all services deployed by Kolla (NOT including the Coriolis components) 
  * **memcached** - container running Memcached 

## Changing the SSL certificates used by Coriolis

To configure an SSL certificate on your Coriolis server, the following certificate files must be prepared:

  * **Server Certificate** - certificate.pem
  * **Root CA Certificate** - cacert.pem
  * **Certificate Key** - key.pem

These files must be made available on any web server the Coriolis appliance can reach over the network.

With that, open the Coriolis appliance console and use option _“9) Change Coriolis API certificate chain”_.

You'll be prompted to enter the URL for each of the three files. After the console downloads and validates the files, it will prompt you to enter the full FQDN of the Coriolis Appliance the certificate is valid for.

In case of any error during the loading process, option _“10) Restore Coriolis API certificate chain”_ lets you roll back to the previous state.

[![](_static/images/coriolis-api-certificate-menu.png)](https://i0.wp.com/cloudbase.it/wp-content/uploads/2026/06/image.png?ssl=1)
