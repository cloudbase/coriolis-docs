---
title: "Coriolis Logs"
wp_id: 38738
---

# Coriolis Logs

All Coriolis installations feature the **Coriolis logger** , a central logging daemon created to integrate into a Coriolis deployment.

This allows easy streaming of logs to any web sockets enabled destination (WebUI, CLI, etc), as well as allowing users of Coriolis to easily download logs that are aggregated by this service.

Conceivably, this can be used with any application that logs to Syslog, and data-store packages can be written for it to allow sending logs to any backend. The following writers and data stores are supported:

## Datastores

  * InfluxDB

## Writers

  * Web Sockets
  * Standard out (for testing purposes mostly)

The Logs feature can be used either from the Coriolis Web UI or through the Coriolis CLI client. 

[![](_static/images/Capture.png)](https://i0.wp.com/cloudbase.it/wp-content/uploads/2020/05/Capture.png?ssl=1)

When downloading logs, you have the option to specify a start date and an end date. This allows you to fetch the logs only for the period you are interested in. 

Moreover, each Coriolis component has a separate entry in the logger, which means you don't need to filter through one big log file for the events logged by one specific Coriolis component. In a standard Coriolis deployment, these are the components you can expect to find logs for:

  * Diagnostics
  * Web-requests
  * Coriolis-api
  * Coriolis-conductor
  * Coriolis-dbsync
  * Coriolis-replica-cron
  * Coriolis-worker

More logs may be available, depending on whether additional components are deployed as part of Coriolis.

When streaming logs, you have the option to either filter by component or receive logs from all components at the same time. 

You can also choose the severity of the logging output you wish to see. Coriolis logger uses standard Syslog severity values.

## Coriolis CLI client

Logs can be streamed or downloaded from the Coriolis-logger backend by using the Coriolis CLI client.

Please see for usage info:

```text
#coriolis log --help 
```

## Coriolis Log Rotation

Log Rotation provides the option to set log intervals with values that are available for **coriolis-api** , **coriolis-conductor** and **coriolis-worker**. It can be enabled by editing the ***-logging.conf** file for each of the 3 components mentioned above, the ***-logging.conf** files are available on Coriolis' Appliance, under **/etc/coriolis/** ***-logging.conf**

After the values are modified in the ***-logging.conf** , the container for the respective component has to be restarted for the changes to apply.

**Coriolis Log Rotation applies to v2012 release or newer.**

The following example applies to all 3 components:

```ini
[DEFAULT]

# Log rotation method.
# If set to 'interval', rotation will occur at predefined time intervals. Check
# INTERVAL ROTATION OPTIONS below.
# If set to 'size', rotation will occur once the log file reaches the predefined
# size. Check SIZE ROTATION OPTIONS below.
# Default is 'none'
log_rotation_type = none

# Maximum number of rotated log files to keep. Default is 30
max_logfile_count = 30

##### INTERVAL ROTATION OPTIONS #####
#
# The amount of time before the log files are rotated. The final interval value
# will be (log_rotate_interval * log_rotate_interval_type)
log_rotate_interval = 7

# The following interval types can be set: [seconds, minutes, hours, days, midnight]
# The default value is days. If this option is set to midnight, the rotation will
# occur every midnight, so log_rotate_interval option will be ignored.
log_rotate_interval_type = days
```
