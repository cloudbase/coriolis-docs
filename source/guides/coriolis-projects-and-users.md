---
title: "Coriolis Projects and Users"
wp_id: 39751
---

# Coriolis Projects and Users

Coriolis leverages Keystone which is the OpenStack project for identity management, in order to create a segregation between users and projects and assign roles.

Coriolis Projects and Users will provide the following:

  * Using the feature, the management of users and different projects can be done.
  * Assigning roles to users (access to one or multiple projects, roles for allowing or denying permissions)
  * Coriolis admin users can create and manage Projects and Users

By default Coriolis comes with one **admin Project** and one **admin user** assigned to it.

![](_static/images/project.jpg)

More **Projects and Users** can be created using the **"New" button** listed on the top right corner on Coriolis' Dashboard.

![](_static/images/new-pu.jpg)

When creating a new Project, the mandatory field that need to be filled in, is the **Project Name** , also there will be an option for enabling it or not to be used once the Project is created.

![](_static/images/new-project-1.2.jpg)

When creating a new User, the mandatory fields that need to be filled in, will be the **Username** , a **Password** for the new user and select the **Primary Project** for the new user. There will also be the option to have the user as enabled or not once it is created.

![](_static/images/new-user.jpg)

Once the Projects and Users are created, **further management** can be performed by **selecting the Project/User** from the Dashboard.

**NOTE!** After creating a new user, you will have to navigate to the projects screen and assign the new user to one or multiple projects, as illustrated in the screenshots below. Only after this is done the new user will be able to login to Coriolis and access the projects.

For Projects:

  * members can be added
  * user roles can be modified
  * users can be disabled or removed from the project

For Users:

  * password ca be changed
  * Project membership can be changed
  * user can be removed

![](_static/images/edit-project.jpg) ![](_static/images/edit-users-1.2.jpg)
