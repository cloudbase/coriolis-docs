---
title: "Coriolis License"
wp_id: 38484
---

# Coriolis License

Coriolis licenses have a start and expiration date for the allowed operation types to be performed. The licenses will **specify the maximum** number of VMs which can be Migrated using **Coriolis Migrations** and also **specify the maximum** number of VMs which can have Disaster Recovery setup using **Coriolis Replicas** and **Coriolis Replica Deployments**. The number of operations that can be performed using a license is per VM, so one 5-VM-Migration counts the same as five 1-VM-Migrations.

A valid Coriolis license is required in order to have Migrations and Replicas executed by a Coriolis installation.

## Obtaining a Coriolis license

  * Go to the About screen

Coriolis licenses are issued based on the unique ID of the Coriolis installation.

To get your Coriolis installation ID, in the main Dashboard screen, navigate to the top right corner, click the user silhouette, and click “About Coriolis”.

![](_static/images/coriolis-license.png)

  * Copy the appliance ID

The About pop-up will show you some details regarding your license (if there is one already). On the bottom row, there will be your Appliance ID which needs to be copied and sent in order to have a license generated for your installation.

![](_static/images/coriolis-license.jpg)

## Installing a Coriolis License

After you receive a new Coriolis license file, it will have to be added to the Coriolis installation.

In order to do so, please follow the below steps within the Coriolis Web UI:

  1. From the Dashboard go to “About Coriolis” (check “Obtain license 1.)
  2. In the pop-up, click “Add license” and upload/paste the provided Coriolis license file
  3. After the license is pasted click on the bottom right “Add license”

![](_static/images/image-7.png)

## How Coriolis Licenses Work

Coriolis users will need active licenses in order to start creating any Coriolis Transfers (based on their base scenario type: Migration or Replica).

Anytime a user creates a Transfer, a license reservation gets created with it, which will decrement one of the active license's available transfer count, that matches the number of instances the Transfer has been created with (for example, if a Migration Transfer containing 2 instances has been created, it will reserve 2 migration licenses, as licenses are reserved per transferred VM).

Once a scenario operation is considered fulfilled, it will mark the license itself as fulfilled (i.e. completely consumed). As long as the Transfer license is unfulfilled, it can be unreserved by first deleting its respective Transfer disks (by explicitly executing a Transfer Delete Disks operation), and then by deleting the Transfer item itself.

Migration licenses get fulfilled only after the first deployment is completed. Coriolis considers a Migration Deployment completed when all its tasks are marked as completed, and it is not able to reliably check whether that migrated instance booted successfully, Once the Migration Deployment is marked as **Completed** , users will no longer be able to either Execute the Transfer or Deploy it a second time anymore.

Replica licenses get fulfilled immediately after the first successful Transfer execution, but users are allowed to re-execute or re-deploy the licensed Transfer infinitely, in the timespan of its reserved license. If another Replica license is provided after an old one expires, re-executing the Replica Transfer will internally try to reserve a new available/non-expired license.
