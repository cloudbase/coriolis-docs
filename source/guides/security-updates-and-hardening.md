---
title: "Security Updates and Hardening"
wp_id: 44044
---

# Security Updates and Hardening

**Coriolis** security is maintained through a combination of automatic operating system security updates, regular product releases, and secure deployment practices.

Operating system security patches are automatically applied through the unattended-upgrades mechanism, helping keep the underlying hosts protected against newly disclosed vulnerabilities. In addition, each new Coriolis release includes refreshed container images containing updated software packages, dependencies, and security fixes available at the time of release.

Administrators can further strengthen the security of deployed services by applying TLS cipher hardening policies to externally exposed endpoints such as Keystone and Barbican.

## Security Maintenance

Coriolis is designed to benefit from ongoing security maintenance at both the operating system and application levels.

### Automatic Operating System Security Updates

Coriolis appliances use automated operating system security patching through the standard unattended-upgrades mechanism. This ensures that security updates released for the underlying operating system are automatically applied as they become available, helping maintain a secure runtime environment with minimal operational overhead.

### Coriolis Releases and Container Image Refreshes

Coriolis services are delivered as containerized components. With each new Coriolis release, whether a minor or major version, the service container images are rebuilt and refreshed.

These refreshed images incorporate updated software packages, dependencies, and security fixes available at the time of the release. As a result, upgrading to newer Coriolis versions allows deployments to benefit from both product enhancements and the latest available security updates included in the service images.

### Upgrading Coriolis Services

Customers are encouraged to upgrade to newer Coriolis releases as they become available. New releases may include:

  * Security fixes
  * Dependency updates
  * Bug fixes
  * Performance improvements
  * New features and enhancements

By keeping Coriolis services up to date, deployments benefit from the latest platform improvements as well as refreshed service images containing updated software components.

## TLS Cipher Hardening

In order to ensure compatibility with various environments and integrations, the Coriolis appliance's services, by default, accept the following TLS ciphers:

```text
TLS_ECDHE_ECDSA_WITH_AES_128_CBC_SHA
TLS_ECDHE_ECDSA_WITH_AES_128_CBC_SHA256
TLS_ECDHE_ECDSA_WITH_AES_128_CCM
TLS_ECDHE_ECDSA_WITH_AES_128_CCM_8
TLS_ECDHE_ECDSA_WITH_AES_128_GCM_SHA256
TLS_ECDHE_ECDSA_WITH_AES_256_CBC_SHA
TLS_ECDHE_ECDSA_WITH_AES_256_CBC_SHA384
TLS_ECDHE_ECDSA_WITH_AES_256_CCM
TLS_ECDHE_ECDSA_WITH_AES_256_CCM_8
TLS_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384
TLS_ECDHE_ECDSA_WITH_ARIA_128_GCM_SHA256
TLS_ECDHE_ECDSA_WITH_ARIA_256_GCM_SHA384
TLS_ECDHE_ECDSA_WITH_CAMELLIA_128_CBC_SHA256
TLS_ECDHE_ECDSA_WITH_CAMELLIA_256_CBC_SHA384
TLS_ECDHE_ECDSA_WITH_CHACHA20_POLY1305_SHA256
```

As an additional security measure, administrators may choose to restrict the TLS cipher suites accepted by externally accessible services.

Cipher hardening helps ensure that service communications use modern cryptographic algorithms while reducing exposure to older or less secure cipher suites.

To restrict the TLS ciphers used by Coriolis services, users need to enter the **Coriolis console**. From there, they should access the **Edit/Inspect Coriolis Configuration**. Each configurable service has a separate configuration file to tweak and will be described in the sections below.

### Apache-based services

The Coriolis API service is exposed using Apache web server, and its configuration file can be found at **/etc/coriolis/wsgi-coriolis.conf**. Inside the **VirtualHost <appliance_ip>:7667** section, the following TLS cipher configuration can be applied:

Inside of the services that are exposed using the Apache web server, the same configuration shall be set. Inside their respective **VirtualHost** sections, the following TLS cipher configuration can be applied:

```text
SSLCipherSuite HIGH:!aNULL:!MD5:!3DES:!RC4:!SHA1:!kRSA
```

This configuration permits strong cipher suites while excluding legacy algorithms and static RSA key exchange.

The Apache-based services are listed in the table below:

**Service Name**| **Configuration File Location**| **Apache Section**  
---|---|---  
Coriolis API service| /etc/coriolis/wsgi-coriolis.conf| VirtualHost _< APPLIANCE_IP>_:7667  
Coriolis Web UI Service| /etc/coriolis/coriolis-web-vhost.conf| VirtualHost *:443  
Keystone| /etc/kolla/keystone/wsgi-keystone.conf| VirtualHost *:5000  

### Barbican Service

The integrated Barbican service is deployed using uWSGI with TLS enabled; a similar cipher policy can be configured for the HTTPS listener. The configuration file for this service can be found at **/etc/kolla/barbican-api/vassals/barbican-api.ini**.

You can add the custom cipher configuration to the existing **https-socket** option:

```text
https-socket = <appliance_IP>:9311,server.crt,server.key,SSLCipherSuite HIGH:!aNULL:!MD5:!3DES:!RC4:!SHA1:!kRSA
```

## Validation

Make sure to exit the console, which will prompt for a restart of all the running services. This will make sure that all the configuration changes apply.

After applying TLS hardening, administrators should verify that services remain accessible and that client applications can continue to connect successfully.

It is recommended to validate the exposed protocols and cipher suites using standard TLS assessment tools before rolling changes into production environments.

### Checking Applied TLS Ciphers with OpenSSL and nmap

After applying TLS cipher hardening, you can validate the effective configuration from a remote machine using the OpenSSL client. This confirms what cipher suites are actually negotiated on the exposed service endpoints.

For a full TLS handshake overview:

```text
openssl s_client -connect <host>:<port>
```

Use nmap to list all accepted ciphers by the services:

```text
nmap --script ssl-enum-ciphers -p <port> <host>
```
