+++
title = "Things Kubernetes Forced Me to Learn This Week"
date = 2025-12-15T20:37:20+00:00
tags = ["certification", "kubernetes"]
featured = false
draft = false
description = "I built a kubeadm Kubernetes cluster in my Proxmox homelab and immediately ran into etcd issues. This time, instead of rebuilding, I understood why it was happening. That understanding changed how I approach Kubernetes and my homelab."
feature_image = "/content/images/2025/12/lfs258-kubernetes-fundamentals.png"
+++

In my last post, I talked about slowing down and really *learning* Kubernetes rather than just following labs and copy-pasting manifests. Since then, I’ve put that mindset to the test in my own homelab… and Kubernetes immediately reminded me who’s in charge.

### **Building a kubeadm Cluster in My Proxmox Homelab**

I recently set up a Kubernetes cluster using **kubeadm** on my Proxmox homelab. This wasn’t a managed environment or a one-command install. This was very much a “real” cluster, control plane, workers, certificates, and all the moving parts that come with it.

Initially, the cluster came up… sort of. Nodes joined, pods started, and then things got weird.

**The etcd Wall (and Why It Mattered)**

I started running into **etcd issues**. Slow responses, warnings, and behaviour that felt inconsistent and fragile. Earlier in my Kubernetes life, this is the point where I probably would have rebuilt the cluster, blamed Proxmox, or quietly pretended nothing was wrong.

This time, something was different.

After completing my **Kubernetes Fundamentals training**, I finally had the mental model to understand what I was looking at. etcd isn’t just “a database Kubernetes uses somewhere in the background”. It *is* the source of truth for the entire cluster.

Everything flows through it:

- Cluster state
- Desired vs actual configuration
- Leader election
- Scheduling decisions

If etcd is unhealthy, Kubernetes doesn’t slowly degrade. It panics.

Once I understood how tightly coupled etcd is to the control plane, the symptoms I was seeing suddenly made sense. The issue wasn’t random. Kubernetes was behaving exactly as designed, I just hadn’t understood the design before.

That moment alone made the fundamentals training worth it.

### **Applying That Knowledge in the Real World**

Being able to reason about etcd meant I could actually troubleshoot the problem instead of guessing. I could look at logs, timings, and behaviour and say “this is why this is happening” instead of “this feels broken”.

That shift from *reacting* to *understanding* is probably the biggest win so far in this journey.

### **Migrating My Homelab to Kubernetes (One Service at a Time)**

With a working cluster and a lot more confidence, I’ve started migrating parts of my homelab to Kubernetes.

The first service I moved was **Portainer**.

Rather than going all-in with a full HA deployment straight away, I deployed Portainer using **KubeSolo**. For my homelab, this is a perfectly reasonable approach. It runs Portainer using **SQLite instead of etcd**, which keeps things simple and stable for a single-instance setup.

So far, it’s been running without issues and has been a great way to ease into running “real” services on Kubernetes without over-engineering everything on day one.

### **What I’m Learning So Far**

A few takeaways that are really sticking with me:

- Kubernetes makes much more sense when you understand *why* components exist, not just how to deploy them
- etcd is not optional, abstract, or ignorable. If you don’t understand it, Kubernetes will humble you
- Homelabs are the best place to break things, as long as you actually stop and learn from the breakage

{{< racknerd >}}

### **What’s Next**

Next steps for me are:

- Continue migrating homelab services to Kubernetes gradually
- Spend more time intentionally breaking and fixing the cluster
- Keep progressing toward the CKA with a stronger focus on fundamentals and real-world scenarios

This journey is already proving that slowing down, asking “why”, and getting hands-on beats rushing through labs every time.

More updates soon. Kubernetes will absolutely find new ways to test me.
