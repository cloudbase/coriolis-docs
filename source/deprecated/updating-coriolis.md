---
title: "Updating Coriolis"
wp_id: 43243
---

# Updating Coriolis

[![](_static/images/image.png)](https://i0.wp.com/cloudbase.it/wp-content/uploads/2024/09/image.png?ssl=1)

NOTE! This page has been deprecated. The new instructions are available here: [Upgrading Coriolis](https://cloudbase.it/upgrading-coriolis/)

**Coriolis** virtual appliance is comprised of a set of Docker containers, a set of Kolla OpenStack services, as well as **Coriolis** service containers. For the scope of doing an in-place upgrade for Coriolis - in particular, to a newer version, the Coriolis service containers will be updated, a process which is detailed on this page.

Generally, an update that is tied to the code in the docker containers can simply use the update action with coriolis-ansible. We will treat the latest Coriolis release as being **2407.1** for this guide.

For upgrading the Coriolis virtual appliance, you must be logged in as root in an SSH shell on the appliance. You must obtain the appliance and docker registry credentials from your Cloudbase Solutions representative. The upgrade path should also be confirmed first with your Coriolis TAM, to avoid any breaking changes and be aware of any changes.

**Coriolis** is comprised of the following service containers, which will be updated as part of this process:

  * coriolis-metal-hub
  * coriolis-console-editor
  * coriolis-licensing-server
  * coriolis-web-proxy
  * coriolis-web
  * coriolis-worker
  * coriolis-minion-manager
  * coriolis-scheduler
  * coriolis-replica-cron
  * coriolis-conductor
  * coriolis-api
  * coriolis-compressor

The update process begins with bringing the Coriolis Docker and Ansible automation git repository to the latest version. You can do that with the following:

> cd /root/coriolis-docker/
> 
> git pull

Cleanup any previous existing certificate paths so there won’t be any conflicts as the upgrade process will generate new ones:

> rm -rf /etc/coriolis-certificates
> 
> rm -rf /etc/coriolis/ssl

Optionally, save the current Coriolis CLI and UI **admin** **password**. The upgrade process will reset it in Keystone so that it can be added back to the appliance. This is available in **/etc/kolla/admin-openrc.sh**.

Run this command to save the password:

> ORIGINAL_PASS=$(grep OS_PASS /etc/kolla/admin-openrc.sh | cut -d= -f2 | tr -d "'")
> 
> echo "ORIGINAL_PASS='$ORIGINAL_PASS'" >> /root/upgrade-tmp-pass

The appliance bootstrap will make sure the **SSL certificates** are generated and need to be executed first:

> /root/coriolis-docker/coriolis-ansible bootstrap

You must use the **Kolla** deploy step since 2407 is moving to SSL endpoints. This includes the OpenStack containers and the Coriolis REST API endpoint, and you must redeploy those with the new configuration to use SSL as well. The Coriolis services will not function once transitioned to use SSH if the Keystone services are not doing so as well.

> /root/coriolis-docker/kolla/deploy.sh

Optionally, save the newly generated keystone password for the **admin** user for convenience.

This is still in **/etc/kolla/admin-openrc.sh** but by this point, it should be freshly generated after the Kolla deploy.

> TMP_RECONFIGURE_PASS=$(grep OS_PASS /etc/kolla/admin-openrc.sh | cut -d= -f2 | tr -d "'")
> 
> echo "TMP_RECONFIGURE_PASS='$TMP_RECONFIGURE_PASS'" >> /root/upgrade-tmp-pass

You must log in to the docker registry from the appliance to pull the latest containers.

> REGISTRY="https://registry.cloudbase.it"
> 
> REGISTRY_USER="coriolis-appliance"
> 
> docker login "$REGISTRY" -username "$REGISTRY_USER" -password-stdin

You must configure coriolis-ansible to **pull** the images from the registry and instruct it which image **tag** to use. This can be configured in **/root/coriolis-docker/docker-images-config.yml**.

The options you will be looking for are:

  * default_coriolis_docker_images_tag: 2407.1
  * docker_pull_images: true

You can edit them manually or replace them with:

> RELEASE="2407.1″
> 
> sed -i "s@^default_coriolis_docker_images_tag.@default_coriolis_docker_images_tag: $RELEASE@g" /root/coriolis-docker/docker-images-config.yml
> 
> sed -i "s@^docker_pull_images.@docker_pull_images: true@g" /root/coriolis-docker/docker-images-config.yml

At this point, you should be ready to run the deploy action for coriolis-ansible. This will pull the specified images from the docker registry, in this case, tag 2407.1, run any necessary configuration for each service, and start the new containers from the freshly pulled images. In the end, coriolis-ansible will also validate the endpoints.

> /root/coriolis-docker/coriolis-ansible deploy

Once the deploy action completes successfully the upgrade process is finished. We can start using the **latest** Coriolis and should validate this by running a few CLI commands:

> source /etc/kolla/admin-openrc.sh
> 
> coriolis endpoint list
> 
> coriolis replica list

You can now log-out the docker registry

> docker logout

If desired, you can change the **admin password** back to the original value before the upgrade process

> source /etc/kolla/admin-openrc.sh
> 
> openstack user password set -password "the desired password optionally the original"
