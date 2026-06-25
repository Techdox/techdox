+++
title = "Embracing Proxmox: Virtualization Adventures in Self-Hosting"
date = 2023-09-20T09:28:34+00:00
tags = ["selfhosting", "proxmox"]
featured = false
draft = false
description = "In my journey from Raspberry Pis to a dedicated Proxmox server, I embraced virtualization. Self-hosting offers endless learning, even when things break—a cycle of challenges and rewards."
feature_image = "https://images.unsplash.com/photo-1695137300649-57882b305d34?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3wxMTc3M3wwfDF8YWxsfDh8fHx8fHwyfHwxNjk1MjAwNjA4fA&ixlib=rb-4.0.3&q=80&w=2000"
+++

Recently, I made the decision to upgrade from hosting my services on a collection of single-board computers, such as my Raspberry Pis, to a dedicated server. Initially, I began by installing Debian and using it as I would with any other server I've had. However, after some discussions, it became clear that Proxmox was the way to go. This approach allows me to set up a dedicated server for my services, but in a virtualised environment. With Proxmox, I can run multiple virtual machines, each serving specific purposes, like a dedicated machine for my NFS shares or virtual machines for testing, including a Windows VM and various Linux distributions. It's also an excellent platform for me to learn more about Proxmox itself.

I'm quite pleased with this approach. Now that I have a dedicated virtual environment and plenty to learn about, I can return to my collection of Raspberry Pis and other single-board computers for more tinkering. This brings me to my next area of exploration—migrating live applications.

The services I need to migrate include:

1. The Techdox Blog
2. Personal NextCloud
3. Two Bookstack environments
4. HomePage Personal Dashboard

The pre-planning for this migration led me to create my Docker Volume backup and restore script, which allowed me to back up my Techdox Blog, containing both the Ghost frontend and its database.

For those interested in the script, you can find it here: [Docker Backup Script](https://github.com/Techdox/docker_backup).

{{< racknerd >}}

Self-hosting is undoubtedly a hands-on endeavour, and I can understand why some people prefer hosted solutions. However, as someone in the tech field who values continuous learning, self-hosting provides an almost endless loop of opportunities for growth. Just when you think everything is running smoothly, something might break, and then it becomes a new learning experience as you figure out how to fix it. It's a cycle of challenges and rewards.

If you're curious about my experience with installing Proxmox for the first time, you can check out my journey here.
