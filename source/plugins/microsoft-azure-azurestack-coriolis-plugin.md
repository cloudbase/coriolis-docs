---
title: "Microsoft Azure/AzureStack Coriolis Plugin"
wp_id: 38520
---

# Microsoft Azure/AzureStack Coriolis Plugin

**Coriolis** integrates the platform Plugin on the Appliance itself, this way there is no need for agents to be deployed on platforms to establish the communication between the platform and the Coriolis components. Using this type of architecture, Coriolis guarantees the connection to the supported platform set up to be used as either Source or Destination, as long as the requirements are met.
Only**Azure Stack Hub** is supported. Other Azure Stack offerings (including Azure Stack HCI, Azure Local, or similar solutions) are not available in Coriolis.

![](_static/images/azure-target-options.png)

### Deployment requirements and supported Azure API versions

#### Deployment requirements

The worker components of Coriolis need network access to the ARM APIs of the targeted Azure/AzureStack region.

Additionally, the Coriolis worker components should have network access to the network range from which Public IPs are allocated for the respective Azure/ Azure Stack region. This is required for reaching the temporary VMs Coriolis will deploy as part of the Migration/Replication operations.

For the Azure endpoint in Coriolis, it is recommended to use an **Azure SPN (Service Principal)** rather than password-based authentication with username and password.

#### Supported Azure API versions

The Coriolis Azure plugin only supports interacting with Azure through the Resource Manager (ARM) APIs, and will not work with the Service Management (ASM) APIs.

### Azure as a source cloud

For more information regarding **[Azure as a source cloud](../platforms/azure-as-a-source-cloud.md)** , please check the documentation page.

### Azure as a destination cloud

For more information regarding **[Azure as a destination cloud](../platforms/azure-as-a-destination-cloud.md)** , please check the documentation page. 

### Required permissions

The Azure account whose credentials are given to Coriolis must have permissions to:

  * read access on the properties of the source VMs and associated resources (VMs, disks, NICs, Public IPs, and virtual networks) within the resource group which is being migrated from
  * create temporary compute resources (VMs, disks, NICs, Public IPs, and virtual networks) within the resource group which is being migrated to/from

### Azure connection parameters

In order to connect to Azure to perform a migration/replica to it, the following connection parameters must be supplied:

#### Example of connection info JSON to be passed to the Azure plugin

```json
{
     
     "subscription_id": "1621bde4-09ee-4904-bea6-cd58316b4bb8",
     
     "service_principal_credentials": {
         "client_id": "7d9ffca0-be78-4f85-a13f-14e791413068",
         "client_secret": "7tnshUgXxrA8iCtCB1VpAiJ5LwP/qhe2q6pVhVYOQfs="
     },
     "default_resource_group": "",
     "tenant": "",
     
     
     
     "cloud_profile": "AzureCloud",
     "custom_cloud_properties": {
         "endpoints": {
             "management_endpoint": ""
         },
         "suffixes": {
             "storage_endpoint": ""
         }
     }
 }
```

Only **service_principal_credentials** must be provided. Should both be provided, Coriolis will prefer using the user credentials.

The parameters representing:

  * **subscription_id  (string)** - the ID of the Azure subscription to perform the migration under
  * **client_id (string, required for service_principal_credentials)** - the ID of the authorized client app to login with
  * **client_secret (string, required for service_principal_credentials)** - the client secret to login with
  * **tenant  (string, required for service_principal_credentials)** - the ID of the Azure AD tenant
  * **default_resource_group (string)** - the name of a resource group to default to using.
  * **cloud_profile (string)** - string identifier of the Azure cloud profile. Can be one of 'AzureCloud', 'AzureChinaCloud', 'AzureUSGovernment', 'AzureGermanCloud' or 'CustomCloud'.
  * **custom_cloud_properties.endpoints.management_endpoint (string)** - string URL of the ARM Management Endpoint for the target Azure/Azure Stack region
  * **custom_cloud_properties.suffixes.storage_endpoint (string)** - string DNS suffix for Blob Storage Accounts.

### Using Coriolis with Azure Stack

The Coriolis Azure plugin should be able to perform migration/replications to Azure Stack identically to how it operates with Azure itself, with the mention that some additional parameters (such as the ARM API endpoint of the Azure Stack region) be filled into the connection options. 

Additionally, the Root Certificate of the AzureStack must be imported in the coriolis-worker component, this should only be required for deployment of Azure Stack Development Kit. To do that, follow the next steps:

  * Export the root Certificate of the AzureStack:

```powershell
 $exportFileBase = "C:\AzureStackRoot"
 $certFile = $exportFileBase + ".cer"
 $pemFile = $exportFileBase + ".pem"
 $label = "AzureStackSelfSignedRootCert"
 # get and export certificate:
 $cert = Get-ChildItem Cert:\CurrentUser\Root | Where-Object Subject -eq "CN=$label" | select -First 1
 Export-Certificate -Type CERT -FilePath $certFile -Cert $cert
 # convert to PEM:
 certutil.exe -encode $certFile $pemFile 
```

  * Import it in Coriolis-worker by just adding the content of cert file to the end of this file _“/usr/local/lib/python3.6/dist-packages/certifi/cacert.pem”. Or _running the following commands on Coriolis host:

```bash
 $ docker cp /path/to/cert.pem coriolis-worker:/root/cert.pem 
 $ docker exec -ti coriolis-worker bash -c 'cat /root/cert.pem >> /usr/local/lib/python3.6/dist-packages/certifi/cacert.pem' 
```

### Azure Stack endpoint creation

In the endpoint creation window for the Azure provider "Custom Cloud" must be selected under the cloud profile.

The additional parameters required by Coriolis for the Azure Stack endpoint can be obtained in JSON form by using azure-cli with the Azure Stack registered.

These can be copied into an expandable, optional field in the endpoint creation window "Paste Configuration"

#### Obtain Azure Stack cloud details with azure-cli

```bash
$ az cloud register -n <environmentname> --endpoint-resource-manager "<a href="https://management.local.azurestack.external%22">https://management.local.azurestack.external"</a> --suffix-storage-endpoint "local.azurestack.external" --suffix-keyvault-dns ".vault.local.azurestack.external"
 $ az cloud set -n <environmentname>
 # depending on the Azure Stack version a different cloud profile could be needed when registering Azure Stack with the cli.
 $ az cloud update --profile 2018-03-01-hybrid
 $ az cloud show
 # Example JSON output with an ASDK registered as the active cloud.
 {
   "endpoints": {
     "activeDirectory": "<a href="https://adfs.local.azurestack.external/adfs%22">https://adfs.local.azurestack.external/adfs"</a>,
     "activeDirectoryDataLakeResourceId": null,
     "activeDirectoryGraphResourceId": "<a href="https://graph.local.azurestack.external/%22">https://graph.local.azurestack.external/"</a>,
     "activeDirectoryResourceId": "<a href="https://management.adfs.azurestack.local/e2bf6aa1-7a8f-4bb9-b8cb-caef446339ec%22">https://management.adfs.azurestack.local/e2bf6aa1-7a8f-4bb9-b8cb-caef446339ec"</a>,
     "appInsightsResourceId": null,
     "appInsightsTelemetryChannelResourceId": null,
     "batchResourceId": null,
     "gallery": "<a href="https://providers.azurestack.local:30016/%22">https://providers.azurestack.local:30016/"</a>,
     "logAnalyticsResourceId": null,
     "management": "<a href="https://management.local.azurestack.external%22">https://management.local.azurestack.external"</a>,
     "mediaResourceId": null,
     "microsoftGraphResourceId": null,
     "ossrdbmsResourceId": null,
     "resourceManager": "<a href="https://management.local.azurestack.external%22">https://management.local.azurestack.external"</a>,
     "sqlManagement": null,
     "vmImageAliasDoc": null
   },
   "isActive": true,
   "name": "ASDK",
   "profile": "2018-03-01-hybrid",
   "suffixes": {
     "acrLoginServerEndpoint": null,
     "azureDatalakeAnalyticsCatalogAndJobEndpoint": null,
     "azureDatalakeStoreFileSystemEndpoint": null,
     "keyvaultDns": null,
     "sqlServerHostname": null,
     "storageEndpoint": null
   }
 }
   
```

More details for registering an Azure Stack in azure cli can be found in [Microsoft's documentation](https://docs.microsoft.com/en-us/azure-stack/user/azure-stack-version-profiles-azurecli2).

### Azure/AzureStack platform specifics

Supported Actions: | Migration Source/Destination - Replica Source/Destination| Comments  
---|---|---  
Plugin identifier| **azure**|  Identifies the plugin. Used for the **- provider** CLI parameter  
Credentials needed| Azure AD service principal credentials| Necessary credentials to give to Coriolis  
Deployment requirements| Coriolis worker component(s) need network access to the ARM APIs| Coriolis deployment and environment connectivity requirements  
Source disk export requirements| Disk export is done through Coriolis' in-build data replication engine.| Requirements to use the replica export (DRaaS source) features  
Instance identification scheme| Names (must be unique)| How instances to migrate/replicate are identified on a source cloud handled by this plugin  
Network identification scheme| Names of Virtual Networks in Azure + names of subnet inside VN| How networks are identified by the plugin. Required for the **network_map** field of the **- destination-environment**  
Storage identification scheme| Azure Storage Account types (both for Blob Storage-based VHDs and Managed Disks)| How storage backends are identified by the plugin. Required for the **storage_map** field of the **- destination-environment**
