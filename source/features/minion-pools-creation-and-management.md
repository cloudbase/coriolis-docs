---
title: "Minion Pools &#8211; Creation and Management"
wp_id: 39758
---

# Minion Pools &#8211; Creation and Management

For most of the supported plugins, the set of **parameters** related to **Minion Pool Machines** are usually shared with the Destination Environment parameters to allow for the dynamic selection of whether or not to use a minion pool or perform creation/cleanup of temporary resources as usual. 

A new minion pool for a given Coriolis Cloud Endpoint can be created using the following: 

```text
coriolis minion pool create \
  --pool-endpoint $ENDPOINT_ID \
  --pool-platform source \
  --pool-os-type linux \
  # Available options can be obtained by running the following command:
  # coriolis endpoint minion pool source/destination options list
$ENDPOINT_ID
  --environment-options '{"plugin-specific": "env options"}' \
  --minimum-minions 3 \
  --notes "Some optional notes or description on the pool." \
  $POOL_NAME
```

The available parameters for minion pools include:

• **- pool-endpoint**: the ID of the Coriolis Endpoint for the pool. The Endpoint must be for a platform whose Provider Plugin supports Minon Pool management.

• **- pool-platform**: whether this should be used as a source or destination Minion Pool. The distinction is in place due to source pools requiring’s special setup steps to allow them to export VM data, while destination pools are especially deployed to import VM data to the destination platform and/or perform OSMorphing.

• **- pool-os-type**: the OS type ('linux', 'windows', or otherwise) for the Minion Pool. Source Minion Pools require them to be of OS type Linux to be able to run the data exports during VM transfers.

• **- environment-options**: JSON data with platform-specific environment options for the Minion Pool. These will usually allow for the selection of properties such as the image to be used for the temporary machines. Care should be taken to pick properties which match the declared -pool-os-type

• **- minimum-minions**: strictly positive number of Minion Machines the pool should contain once allocated.

Additional operations on minion pools include: 

```text
#inspect existing pools:
 coriolis minion pool list
 coriolis minion pool show $POOL_ID

#create a Pool Execution to set up pool VM shared resources for the specific
 platform and pool type it was configured as (e.g. a shared virtual network)
 coriolis minion pool set up shared resources $POOL_ID
 
#view and manage Minion Pool Executions:
 coriolis minion pool execution list $POOL_ID
 coriolis minion pool execution show $POOL_ID $EXECUTION_ID
 
#allocate minion pool machines:
 coriolis minion pool allocate machines $POOL_ID
 
#use a Minion Pool for a Replica or Migration
 coriolis replica/migration create \
  # NOTE: additional required parameters listed in their
  # respective sections further below.
  --instance $INSTANCE1 --instance $INSTANCE2 \
  --origin-minion-pool-id $SOURCE_POOL_ID \
  --destination-minion-pool-id $TARGET_POOL_1_ID \
  --osmorphing-minion-pool-mapping $INSTANCE1=$TARGET_POOL_2_ID

#deallocate Minion Pool machines:
 coriolis minion pool deallocate machines $POOL_ID
 
#tear down pool shared resources:
 coriolis minion pool tear down shared resources $POOL_ID
 
#update a Minion Pool (can be done only if the pool has had its
 machines deallocated and its shared resources torn down)

#coriolis minion pool update \
  # NOTE: all the paramters for 'minion pool create' can be modified except
  # for the selected minion pool --pool-endpoint and --pool-platform.
  --arguments-to-update … \
  $POOL_ID
 
#delete a minion pool (only if all of its machines/resources were torn down)
 coriolis minion pool delete $POOL_ID
```

## Minion Pools - Using when creating Migrations/Replicas

Once created, Minion Pools can then be used when creating Migrations or Replica jobs using the **- origin-minion-pool-id**, **- destination-minion-pool-id**, and **- osmorphingminion-pool-mapping** arguments as shown below:

```text
coriolis migration/replica create \
  --origin-endpoint $ENDPOINT_ID_1 \
  # NOTE: the origin Minion Pool must be associated with the
  # above selected --origin-endpoint, and have its --pool-platform
  # set to 'source' when it was created:
  --origin-minion-pool-id $OPTIONAL_SOURCE_MINION_POOL_ID \
  --destination-endpoint $ENDPOINT_ID_2 \
  # NOTE: the destination Minion Pool must be associated with the
  # above selected --destination-endpoint, and have its --pool-platform
  # set to 'destination' when it was created:
  --destination-minion-pool-id $OPTIONAL_DESTINATION_MINION_POOL_ID \
  --source-environment{-file,} "$SOURCE_ENVIRONMENT_{FILE,STRING}" \
  --destination-environment{-file,} "$DESTINATION_ENV_{FILE,STRING}" \
  --network-map{-file,} "$NETWORK_MAP_{FILE,STRING}" \
  --default-storage-backend $DEFAULT_BACKEND \
  --disk-storage-mapping $DISK_STORAGE_MAPPING \
  --storage-backend-mapping $STORAGE_BACKEND_MAPPINGS \
  # NOTE: the OSMorphing Minion Pools must be associated with the
  # above selected --destination-endpoint, and have their --pool-platform
  # set to 'destination' when they were created:
  --osmorphing-minion-pool-mapping
 $VM_NAME_1=$OPTIONS_DESTINATION_MINION_POOL \
  --instance $VM_NAME_1 --instance $VM_NAME_2
```

###  Requirements for using Minion pools for a transfer of N instances 

  * **- origin-minion-pool-id**: 
    * must have been created as a minion pool of -pool-platform type source
    * must be a pool formed of Linux machines to be used for data exports
    * must contain at least N minion machines which have been pre-allocated and available for use
  * **- destination-minion-pool-id**: 
    * must have been created as a minion pool of -pool-platform type destination
    * must be a pool formed of Linux machines to be used for data imports
    * must contain at least N minion machines which have been pre-allocated and are available for use
  * **- osmorphing-minion-pool-mapping**: 
    * must have been created as a minion pool of -pool-platform type destination
    * must be a pool formed of machines of the same OS type as the VM it was selected to perform OSMorphing on
    * must contain at least one minion machine which has been pre-allocated and is available for use


