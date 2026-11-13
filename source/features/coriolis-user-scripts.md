---
title: "Coriolis User Scripts"
---

# Coriolis User Scripts

**User Scripts** allow users to hook into Coriolis’ OS Morphing process and execute any needed last-minute customizations for the instance(s) being Migrated before being booted up on the destination cloud platform.

## How To Add User Scripts

The feature is available in the following scenarios:

  * Creating a Deployment from a current Transfer (from an existing transfer, head to `Actions > Create Deployment > User Scripts`):

![](_static/images/coriolis-user-scripts-create-deployment.png)

  * When creating a transfer you will be prompted after setting up the Storage mapping:

![](_static/images/coriolis-user-scripts-new-transfer.png)

## Types Of User Scripts

User scripts can be:

  * **Global**: All instances of the given type will be executing the given script (i.e. selecting multiple instances at once when creating transfers, all the Windows instances will be executing the script added to *Windows Script File*, while all the Linux ones will be executing the script added to *Linux Script File*). Great for mass migrations to set up network configs, install updates, etc.
  * **Instance**: Each selected instance can have its own designated script to run individually. This may come in handy when you have different setups for different VMs.

Each of these can also have different times when to run during OS Morphing, depending on the use case.

![](_static/images/coriolis-user-scripts-run-times.png)

  * **Before mount**: Runs before the OS partition is mounted during OS morphing, e.g. to unlock encrypted disks;
  * **After mount**: Runs after the OS partition is mounted during OS morphing (the default);
  * **First boot**: Injected during OS morphing and executed when the VM boots for the first time.

## How user scripts should look like

Depending on the operating system that is being migrated, the user scripts may be:

  * for Linux VMs, any scripting language available on a standard Linux (bash, python, etc.)
  * for Windows VMs, PowerShell and batch scripts are supported.

### Linux User Scripts

#### After mount

The script runs on the worker VM and receives the path of the migrated OS root as `$1`. Anything written outside that path stays on the worker and doesn’t reach the migrated VM.

The simplest approach is to use `chroot`, so that commands run with the migrated OS’s own tools and normal paths:

```bash
#!/bin/bash

root_disk="$1"

chroot "$root_disk" /bin/bash -c 'echo "This script was ran at $(date)" > /root/coriolis_user_script_test.log'
```

This script creates `/root/coriolis_user_script_test.log` on the migrated VM.

You can also skip `chroot` and prefix each path:

```bash
#!/bin/bash

root_disk="$1"

echo "This script ran at $(date)" > "$root_disk/root/coriolis_user_script_test.log"
```

#### First boot

The script runs on the migrated VM itself, so paths are normal and no parameter is passed:

```bash
#!/bin/bash
set -e

echo "This script ran at $(date)" > /root/coriolis_user_script_test.log
```

  * It’s run as root by the systemd service `coriolis-firstboot.service`, once the network is up and after Coriolis’s own first boot scripts. The migrated OS must use systemd.
  * It’s saved in `/usr/lib/coriolis/firstboot/user/`.
  * Its output goes to the journal: `journalctl -u coriolis-firstboot`.

### Windows User Scripts

#### After mount

The script runs on the worker VM and receives the root of the migrated OS drive as `$args[0]`, for example `F:\`. Windows has no chroot, so use paths under `$args[0]`, or tools that can work on an offline image, such as `dism.exe`.

```powershell
$OS=$args[0]
dism.exe /Image:$OS /Get-Drivers
```

This lists the third-party drivers on the migrated OS. It doesn’t change anything, and its output only goes to the Coriolis debug log.

An after mount script can also add a script for Cloudbase-Init to run at first boot:

```powershell
$custom_script = @"
script_line1
script_line2
"@

$custom_script | Out-File $args[0]Cloudbase-Init\LocalScripts\99-custom-script.ps1
```

The lines between `@'` and `'@` are saved as a script in the `LocalScripts` folder on the migrated disk, and Cloudbase-Init runs them when the VM first boots. To use your own commands, replace those lines. The closing `'@` must stay at the very start of its line.

#### First boot

Here you can enter only the commands you want to run. Coriolis saves them in the Cloudbase-Init LocalScripts folder, and Cloudbase-Init runs them when the VM first boots. No parameter is passed, and paths are the VM’s normal ones. Cloudbase-init is installed on the migrated VM during OS Morphing.

```powershell
$file = "$env:PUBLIC\Desktop\coriolis_user_script_test.txt"
"This script ran at $(Get-Date)" | Out-File -FilePath $file -Encoding ascii
```

This has the same result as the after mount example above, with less to write, so you only need one of the two.

## Step-by-Step Run Using User Scripts

First we create a transfer with the usual configuration (preferred **Target Options**, **Network Mapping** and **Storage Mapping**), then we will be prompted with the User Scripts.

![](_static/images/coriolis-user-scripts-step-1.png)

Here, we will be selecting the Instance Script for `ubuntu-server`, then proceed to select the `OS morphing: after mount` option, and proceed to select the shell file that you will want to use for the instance.

![](_static/images/coriolis-user-scripts-step-2.png)

In this case, we are using `ubuntu-user-script.sh` that looks like this:

```bash
#!/bin/bash
set -e

root_disk="$1"

chroot "$root_disk" /bin/bash -c "apt update && apt install -y btop"

chroot "$root_disk" /bin/bash -c 'echo "The script was ran at $(date)" > /root/coriolis_user_script_test.log'

exit 0
```

![](_static/images/coriolis-user-scripts-step-3.png)

After adding the script, we will proceed to hit Save, which will close the User Scripts modal, then proceed with the transfer as usual.

During the OS Morphing Task in the Deployment phase, we will be able to see that the script was executed.

![](_static/images/coriolis-user-scripts-step-4.png)

After the migration is done, we can proceed to our destination cloud and check the script output.

![](_static/images/coriolis-user-scripts-step-5.png)

As we can see, the script ran successfully on the migrated VM.
