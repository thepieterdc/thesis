# Standards

## OCI (Open Container Initiative
- project van Linux Foundation
- Image spec
- Runtime spec

## appc (App Container) spec
- Lijkt op OCI maar dan voor apps ipv volledige operating systems

# Containers

## containerd
- Daemon voor runC, lijkt op Docker maar geen image repository

## cri-o
- [https://cri-o.io/](https://cri-o.io/)
- Is whatever Kubernetes nodig heeft om te werken
- Zo simpel mogelijk, altijd compatibel blijven met Kubernetes
- OCI containers via runC runnen

## Docker
- [https://www.docker.com/](https://www.docker.com/)
- Docker daemon is enige interface met containers

### < v1.11.0
Container processes runnen als root -> werkt niet met systemd en security issues

### >= 1.11.0
Docker convert zijn eigen image naar OCI-compliant image en gebruikt runC om die OCI image te starten

## Kata
- [https://katacontainers.io/](https://katacontainers.io/)
- Snelheid van containers met security van VM's
- Hardware virtualisatie, elke container heeft eigen kernel instance -> geen access meer tot kernel van host

## LXC/LXD
- LXC is basis (Liux Containers), LXD is een alternatieve interface op de default LXC via REST API.
- Start een compleet OS net zoals een VM
- Geen daemon interface -> werkt met upstart/systemd

## podman
- [https://podman.io/](https://podman.io/)
- Geen daemon, interactie via runC

## rkt
- [https://coreos.com/rkt/](https://coreos.com/rkt/)
- Zowel OCI/Docker images als appc images
- Geen eigen init systeem -> werkt met Linux init systems (upstart/systemd)
- Unix permissions -> scheiding van privileges, images runnen als non-root

## runC
- implementatie door OCI
- zeer low-level

# Sources
- [https://coreos.com/rkt/docs/latest/rkt-vs-other-projects.html](https://coreos.com/rkt/docs/latest/rkt-vs-other-projects.html)
- Bekijken: [https://www.ianlewis.org/en/container-runtimes-part-1-introduction-container-r](https://www.ianlewis.org/en/container-runtimes-part-1-introduction-container-r)
