+++
title = "KubeSolo: Moving From Docker to Kubernetes in a Homelab"
date = 2026-06-05T00:00:00+12:00
tags = ["kubernetes", "selfhosting", "docker"]
featured = true
draft = false
description = "Not every homelab needs a 3-node Kubernetes cluster. KubeSolo gives you a single-node way to learn Kubernetes, run real workloads, and migrate from Docker without building more infrastructure than you need."
+++

Kubernetes is one of those things that can feel simple in a course and messy the moment you try to run it at home.

In a homelab, the problem usually is not "can I build a cluster?" It is "does this actually make sense for what I am running?"

If you only have one small server, an old mini PC, a Raspberry Pi, or a VM in Proxmox, building a full multi-node cluster can be overkill. You need to think about control plane nodes, worker nodes, etcd health, storage, networking, upgrades, and failure domains. That is great learning, but it can also turn a simple self-hosted service into a weekend of debugging.

That is where KubeSolo has been useful for me. It gives me a way to run Kubernetes workloads on a single machine without pretending my homelab is a production data centre.

## What is KubeSolo?

[KubeSolo](https://www.kubesolo.io) is a single-node Kubernetes implementation. The important bit is that it still exposes the Kubernetes API, so you can use normal Kubernetes tools like `kubectl`, manifests, and Helm charts.

The difference is that it removes the parts that only really matter when you are running multiple nodes. In a normal Kubernetes cluster, you have components designed around clustering, leader election, shared state, and node-to-node networking. Those pieces matter a lot when you are running a highly available cluster, but they are not always useful when everything is on one box under your desk.

KubeSolo keeps the Kubernetes workflow, but simplifies the underlying setup for a single host.

It is also worth mentioning that KubeSolo is maintained by [Portainer](https://portainer.io), where I work. So yes, I am close to it. But the reason I am writing about it is because it fits a real homelab use case: learning and running Kubernetes without needing to build more infrastructure than the workload needs.

## Why Not Just Stick With Docker?

Docker is still excellent for self-hosting. If your Docker Compose files are working and you are happy with them, there is no urgent reason to rip everything out.

For a lot of homelabs, Docker Compose is still the simplest and most sensible option. A `compose.yaml` file, a few bind mounts, and a reverse proxy can get you a very long way.

The reason to try Kubernetes is usually learning, consistency, or tooling.

Maybe you want to understand how Kubernetes works before touching it at work. Maybe you want to use Helm charts because a project maintains those better than its Compose examples. Maybe you want to learn deployments, services, ingress, config maps, secrets, and persistent volumes in an environment you actually care about.

That is where a single-node Kubernetes setup makes sense. You are not doing it because Docker is bad. You are doing it because you want to learn Kubernetes concepts on real services without making your homelab harder than it needs to be.

{{< racknerd >}}

## How It Fits in a Homelab

The easiest way to think about KubeSolo is as a Kubernetes host, not a Kubernetes cluster in the traditional sense.

In Docker, you might run a service like this:

- The container runs on one machine
- Volumes live on that same machine
- Ports are exposed on that same machine
- If the machine goes down, the service goes down

KubeSolo is similar from an infrastructure point of view, but the way you describe and manage the workload changes:

- A container becomes a Kubernetes `Deployment` or `StatefulSet`
- A published port becomes a `Service`
- A bind mount or named volume becomes a `PersistentVolumeClaim`
- Environment variables can move into `ConfigMap` and `Secret` objects
- A Compose stack becomes a set of manifests or a Helm chart

That mapping is what makes it useful. You still have the reality of one physical machine, but you start learning Kubernetes primitives instead of only Docker primitives.

For example, if you deploy Nginx with a `LoadBalancer` service, KubeSolo can expose that service on the host IP. In practical homelab terms, that means you can point your browser, reverse proxy, or DNS records at the machine and reach the workload without needing a cloud load balancer.

Storage is similar. KubeSolo includes local persistent volume support, so a workload can request storage using a `PersistentVolumeClaim`. Under the hood, that storage is still local to the node. That is fine for a homelab, but it is important to understand what it means: if the disk or host dies, Kubernetes will not magically move that data somewhere else. You still need backups.

## What You Get

For a small homelab node, the useful pieces are:

- A normal Kubernetes API to work with
- `kubectl` support
- Helm chart support
- `LoadBalancer` services using the host IP
- Local persistent volume support
- CoreDNS and container networking included
- Support for x86_64, ARM, ARM64, and RISC-V 64

That means it can run on the kind of hardware people actually use at home: mini PCs, ZimaBoards, Raspberry Pis, spare desktops, and small VMs.

The main thing I like is that it lets me practise Kubernetes against services I already understand. I can take something like Nginx, Portainer, Uptime Kuma, or a small internal app and learn how it behaves as a Kubernetes workload.

## Installing KubeSolo

One thing to note before you start: KubeSolo does not want Docker, Podman, or containerd already running on the same machine. Use a fresh VM or a dedicated host if you are testing it.

The install is straightforward:

```bash
curl -sfL https://get.kubesolo.io | sudo sh -
```

This installs KubeSolo and registers it as a systemd service. Watch it come up with:

```bash
journalctl -u kubesolo -f
```

Once it's running, the admin kubeconfig is at `/var/lib/kubesolo/pki/admin/admin.kubeconfig`. Copy that to your local machine, point kubectl at it, and check your node:

```bash
kubectl get nodes
```

You should see a single node in a `Ready` state.

At that point, you are not learning a "fake" interface. You are talking to Kubernetes, just on a single-node setup.

## Deploying Your First Workload

From here, you deploy workloads the same way you would on another Kubernetes environment. A simple test is Nginx with a `LoadBalancer` service:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx
spec:
  replicas: 1
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx:latest
        ports:
        - containerPort: 80
---
apiVersion: v1
kind: Service
metadata:
  name: nginx
spec:
  type: LoadBalancer
  selector:
    app: nginx
  ports:
  - port: 80
    targetPort: 80
```

```bash
kubectl apply -f nginx.yaml
```

Then check the service:

```bash
kubectl get svc nginx
```

You should see the service exposed on the node's IP. Hitting that IP on port 80 should take you to Nginx.

That small example teaches a few important Kubernetes ideas:

- The `Deployment` manages the pod
- The pod runs the container
- The `Service` gives the workload a stable way to be reached
- The `LoadBalancer` type exposes it outside the cluster

That is the kind of learning I find valuable in a homelab. You are not just following a tutorial. You are seeing how Kubernetes objects fit together on a machine you control.

## Migrating From Docker Without Making a Mess

I would not move everything at once.

The better approach is to pick one low-risk service and migrate that first. Something like a test Nginx container, a dashboard, or a service where you already have good backups.

For each Docker service, ask:

- What image does it run?
- What ports does it expose?
- What environment variables does it need?
- What files or volumes must persist?
- Does it need access to other services?
- How will I back it up and restore it?

Those questions map nicely into Kubernetes objects. The image and replicas go into a `Deployment`. The ports go into a `Service`. Configuration goes into a `ConfigMap` or `Secret`. Persistent data goes into a `PersistentVolumeClaim`.

This is also where Kubernetes can force better habits. Instead of one Compose file quietly holding everything, you start thinking more clearly about what is configuration, what is secret, what is storage, and what is networking.

That does not mean Kubernetes is simpler than Docker. It usually is not. But it can make the structure of an application more explicit.

## Portainer Integration

Since KubeSolo implements the Kubernetes API, Portainer can connect to it as a Kubernetes environment. That is useful if you already manage Docker or Kubernetes hosts through Portainer and want this node visible in the same place.

You can also install the Portainer Edge Agent during setup using an environment variable. For my setup, that makes sense because I already use Portainer elsewhere in the lab. But it is not required to understand or use KubeSolo. You can do everything with `kubectl` if that is how you prefer to learn.

## What It Does Not Solve

This part matters.

KubeSolo is single-node Kubernetes. That means it does not give you high availability. If the host is offline, your workloads are offline. If the local disk fails and you do not have backups, your data is at risk. If you want workloads to move between machines automatically, you need a real multi-node cluster and the storage/networking design that goes with it.

So I would not treat KubeSolo as a replacement for learning full cluster design. It is more of a stepping stone, or a practical option for services that only need one node anyway.

For a homelab, that is not a bad thing. A lot of self-hosted services already run on one box. KubeSolo just lets you manage those services with Kubernetes patterns.

## Is It Worth It?

For me, yes, but with a specific use case.

I would use KubeSolo if:

- You want to learn Kubernetes on real homelab workloads
- You only have one machine available
- You want to use Helm charts or Kubernetes manifests
- You understand that single-node means no high availability
- You are happy managing backups yourself

I would probably stick with Docker Compose if:

- Your current setup works and you do not care about learning Kubernetes yet
- You want the least moving parts possible
- You do not need Kubernetes-native tooling
- You are running services for other people and uptime matters more than experimenting

That is the balance I keep coming back to in my own homelab. Kubernetes is worth learning, but it is also very easy to overcomplicate things.

KubeSolo gives me a middle ground: one machine, real Kubernetes objects, normal Kubernetes tooling, and enough simplicity that I can focus on how and why things work rather than spending all my time maintaining a cluster.
