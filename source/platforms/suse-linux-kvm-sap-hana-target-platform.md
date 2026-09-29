# SUSE Linux (KVM) as a destination cloud (SAP HANA SKU)

SAP HANA workloads require a separate licensing model and endpoint, which
provide SAP HANA-specific configuration options needed to meet performance,
support, and compliance requirements.

See the [**basic SKU documentation**](./suse-linux-kvm-target-platform.md)
before getting started.

```{note}
The SAP HANA SKU may also be used for other instances that require advanced
features.
```

## Configuration options

The SAP HANA endpoint uses the same `[libvirt_migration_provider]` section
as the [**basic SKU**](./suse-linux-kvm-target-platform.md#configuration-options).
The options below are the advanced settings from the SAP provider: huge pages,
NUMA pinning, guest clock and timers, vhostmd, raw disk passthrough, and
disk-controller passthrough.

`hugepage_size`, `numa_node_count`, `allocate_entire_numa_nodes`, and
`enable_vhostmd` can also be set per transfer in the target environment.
When a transfer does not set them, they fall back to the values in this section.

```ini
[libvirt_migration_provider]

# Configure replica instances to use huge pages of the given size (KB).
# Note that the huge pages must be preallocated. The possible size depends
# on the host CPU architecture, 2MB and 1GB being the most common values on
# x86-64. If unset, the VMs will not use huge pages. The VM memory capacity
# must be a multiple of the hugepage size.
hugepage_size = 0

# The amount of NUMA nodes to use for the VM. If set to 0, no explicit NUMA
# topology will be defined. If set to a positive value, the VM CPUs and
# memory will be spread across the given number of host NUMA nodes, pinning
# VM CPUs to unused host CPUs.
numa_node_count = 0

# Allocate the specified amount of host NUMA nodes entirely to the VM,
# regardless of the number of source VM vCPUs.
allocate_entire_numa_nodes = false

# Value for the Libvirt <cpu check="..."> attribute. Set to 'none' to
# disable CPU compatibility checks, or 'partial' / 'full' as required by
# your environment.
cpu_check = none

# A list of host CPUs that will not be used by pinned VM vCPUs.
#
# Contains comma separated ranges of CPUs in Libvirt format.
#
# Example: 1-4,^3,5
#
# In this example, CPUs 1,2,4 and 5 will be reserved.
# reserved_cpus =

# Number of memory pages to reserved per host NUMA node.
#
# Each entry will contain comma separated key:value pairs describing the
# NUMA node ID, the page size in KB and the number of reserved pages.
#
# Example:
#
#     reserved_memory_pages = node:0,size:2048,count:64
#     reserved_memory_pages = node:0,size:4,count:10485760
#     reserved_memory_pages = node:1,size:1048576,count:2
#     reserved_memory_pages = node:1,size:4,count:10485760
#
# In this example we're reserving 10GB of memory using standard 4K page
# size on both NUMA nodes, 2 GB of memory in 1GB pages on NUMA node 1 and
# 128MB of memory in 2MB pages on NUMA node 0.
# reserved_memory_pages =

# Defines the NUMA scheduling strategy. If enabled, the scheduler will
# favor NUMA nodes that are more loaded. If disabled, we'll try to spread
# the resources across NUMA nodes, favoring nodes that are less loaded.
# pack_numa_nodes = false

# Clock offset for replica VMs. Accepted values are 'utc' and 'localtime'.
# When unset (the default), the provider picks 'localtime' for Windows
# guests and 'utc' for all other OS types.
# clock_offset =

# VM timer configuration. Each entry is a set of comma-separated key:value
# pairs describing one timer. Windows guests additionally get a hypervclock
# timer appended unless one is already listed.
# Example:
#   cpu_timers = name:rtc,tickpolicy:catchup
#   cpu_timers = name:pit,tickpolicy:delay
#   cpu_timers = name:hpet,present:no
# cpu_timers =

# Attach the vhostmd metrics image as a read-only block device to replica
# instances. This exposes KVM host metrics to workloads such as SAP HANA via
# the vm-dump-metrics utility. Requires vhostmd to be running on the Libvirt
# host and the metrics disk at vhostmd_device_path to exist.
enable_vhostmd = false

# Path to the vhostmd metrics disk on the Libvirt host. The file disk in the
# domain XML will use this path as its source. Only used when enable_vhostmd
# is True.
vhostmd_device_path = /dev/shm/vhostmd0

# Specifies how pinned sibling CPUs should be defined in the Libvirt domain
# configuration.
#
# If sibling CPU floating is enabled, the VM vCPU will be allowed to float
# between sibling host CPUs.
#
#     <vcpupin vcpu='0' cpuset='0,16'/>
#     <vcpupin vcpu='1' cpuset='0,16'/>
#
# If sibling CPU floating is disabled, the VM vCPU will be pinned to a
# single host CPU.
#
#     <vcpupin vcpu='0' cpuset='0'/>
#     <vcpupin vcpu='1' cpuset='16/>
pinned_cpu_float_between_siblings = false

# The name of the pool used for raw passthrough disks. Will be hidden if
# 'passthrough_disks' is empty. Note that we aren't using Libvirt storage
# pools for raw passthrough disks.
raw_disk_pool_name = raw-disks

# A list of disk paths that can be attached to replica instances when the
# user selects the pool specified by "raw_disk_pool_name".
#
# Each entry must specify the target host address and the disk path on that
# host. The disks will be attached using virtio emulated devices (PCI
# passthrough cannot be used with individual disks, only entire
# controllers).
#
# Example:
#     passthrough_disks = host:192.168.1.10,path:/dev/disk/by-id/wwn-0x5c50071daf
#     passthrough_disks = host:192.168.1.10,path:/dev/disk/by-id/wwn-0x5d911034a9
#     passthrough_disks = host:192.168.1.11,path:/dev/disk/by-id/wwn-0x5911034a97
# passthrough_disks =

# A list containing PCI addresses of disk controllers that can be attached
# to replica instances.
#
# Each entry must specify the target host address and the PCI address of
# the controller on that host. The entire controller will be exposed to the
# instance using PCI passthrough, avoiding virtualization overhead. Once
# attached, the controller as well as the associated disks will no longer
# be visible to the host.
#
# The controllers are exposed to Coriolis users as storage backends
# (pools). Coriolis will pick a suitable disk from the specified controller
# when performing disk transfers.
#
# Fibre Channel HBAs often share an IO-MMU group (typically two functions
# of the same adapter). All PCI devices that belong to the same IO-MMU
# group must be listed here so they can be attached together. Only the
# first listed device in each group is exposed as a selectable storage
# pool.
#
# Example:
#     passthrough_disk_controllers = host:192.168.1.10,address:0000:af:00.0
#     passthrough_disk_controllers = host:192.168.1.10,address:0000:af:00.1
#     passthrough_disk_controllers = host:192.168.1.11,address:0000:3b:00.0
# passthrough_disk_controllers =
```

## Storage controllers exposed over PCI passthrough

PCI passthrough requires the same kernel parameters as described by the
[**SR-IOV section**](./suse-linux-kvm-target-platform.md#sr-iov)

Use the `passthrough_disk_controllers` setting to whitelist storage controllers
that can be attached to migrated VMs.

All devices that belong to a IO-MMU group must be attached together to the
same VM. In case of Fibre Channel HBAs, make sure to whitelist all the HBAs
that belong to the same IO-MMU group.

Note that only the first HBA of a group will be reported as a Coriolis storage
backend. Coriolis will automatically "detach" the devices from the host, set them
to use the VFIO driver and attach them to transfer workers or replica instances.

If a replica instance is deleted and you wish to reuse the controller for
another instance, use the "free_libvirt_resources.py" script from the appliance
console to release it and the corresponding disks.

Use the `virsh nodedev-reattach` command to expose the storage controller to
the host again, passing `pci_<address_with_underscores>` as parameter.
