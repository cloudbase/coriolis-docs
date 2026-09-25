---
title: "Coriolis Endpoints"
wp_id: 38488
---

# Coriolis Endpoints

Coriolis **Cloud Endpoints** are a type of resource within Coriolis which contains the connection details and credentials for the cloud platforms Coriolis will be interacting with.

Once created, the Cloud Endpoints will be referenced during the creation of Migration/Recovery jobs to/from the respective cloud platform they describe.

## Creating endpoints

In order to create endpoints, from the Coriolis Appliance, click “Cloud Endpoints” from the left side menu, then click “Add Endpoint”.

[![](_static/images/coriolis-add-endpont.jpg)](https://i0.wp.com/cloudbase.it/wp-content/uploads/2023/02/coriolis-add-endpont.jpg?ssl=1)

From the new popup, select the Endpoint that is to be used

[![coriolis new endpoint](_static/images/endpoints.png)](https://i0.wp.com/cloudbase.it/wp-content/uploads/2024/03/endpoints.png?ssl=1)

In the new popup, fill in the details for your Endpoint.

Note that VMWare is used in this specific example and that other platforms will feature their specific connection parameters. Please consult the respective platform's Coriolis plugin documentation for details on the parameters required for your desired platform.

  1. Give a name to the new endpoint
  2. Enter the credentials for a user with the permissions required for Coriolis to Migrate/Replica VMWare
  3. Add the host IP address

[![](_static/images/image-10.png)](https://i0.wp.com/cloudbase.it/wp-content/uploads/2020/03/image-10.png?ssl=1)

  * **NAME** - the name of the endpoint that will be added
  * **USERNAME** - the VMWare username
  * **PASSWORD** - the password for the provided username
  * **HOST** - the VMWare vSphere hostname of IP address
  * **PORT** - the port number user for accessing the VMWare vSphere
  * **ALLOW UNTRUSTED** - either trust of not self-signed certificates

After the details are filled in, click “Validate and save”. Coriolis will then automatically attempt to log in to the VMWare platform to ensure the provided credentials are correct.

If the validation step fails, please review all of the provided details to ensure that they are correct.

Perform the same previous steps for the other Endpoints that are to be used.

## Exporting or Importing Coriolis Cloud Endpoints

After setting up the endpoints manually you will be able to download the file with the endpoint's configuration for backup purposes or importing into a different Coriolis installation.

Firstly, you’ll have to select your Endpoint, by accessing the Cloud Endpoints in your appliance.

[![](_static/images/endpoint-export.png)](https://i0.wp.com/cloudbase.it/wp-content/uploads/2023/02/endpoint-export.png?ssl=1)

Now, from the new window, select from the top left “Actions” and then “Download .endpoint file”

[![](_static/images/image-29.png)](https://i0.wp.com/cloudbase.it/wp-content/uploads/2020/03/image-29.png?ssl=1)

By having an Endpoint file downloaded, you will be able to upload it using another user or when deploying another appliance.

The file can be uploaded when following the steps to add a new Endpoint, by selecting “upload” from the bottom of the page instead of selecting one on the Clouds.

[![](_static/images/image-30.png)](https://i0.wp.com/cloudbase.it/wp-content/uploads/2020/03/image-30.png?ssl=1)
