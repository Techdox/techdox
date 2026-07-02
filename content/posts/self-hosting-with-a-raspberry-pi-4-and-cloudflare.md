+++
title = "Self-Hosting With a Raspberry Pi 4 and Cloudflare"
date = 2023-03-28T07:25:51+00:00
tags = ["selfhosting", "raspberry-pi", "cloudflare"]
description = "My self-hosting setup on a Raspberry Pi 4 with Docker and Cloudflare — the hardware, the services I run, and how traffic reaches them without exposing my home IP."
featured = false
start_here = true
draft = false
feature_image = "https://images.unsplash.com/photo-1568332339712-fa479d5494fa?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=MnwxMTc3M3wwfDF8c2VhcmNofDN8fHJhc3BiZXJyeSUyMHBpfGVufDB8fHx8MTY3OTk4NjgxMA&ixlib=rb-4.0.3&q=80&w=2000"
+++

If you know me personally or have watched my [YouTube channel](www.youtube.com/techdoxnz), you're probably aware of my love for self-hosting and trying out different services on my own rather than relying on paid or free hosting options. One of my favorite tools for self-hosting is the Raspberry Pi - these low-power devices are affordable (or at least they were before the current chip shortage), and when combined with Docker, they can handle a lot of tasks. In particular, the Raspberry Pi 4 - with its quad-core processor and 8GB of RAM - packs a serious self-hosting punch.

That's why I've decided to start documenting my self-hosting journey in a new blog series, complete with videos covering new services I haven't yet explored. And today, I'll be sharing my current setup with you, starting with how I use a Raspberry Pi 4 in conjunction with Cloudflare to self-host my own services.

{{< racknerd >}}

## Hardware

![None](/content/images/2023/03/IMG_2009-Small.png)

*Raspberry Pi 4 - Quad Core - 8GB RAM*

Let's start by taking a look at my hardware setup. For my Raspberry Pi 4, I'm using an Argon One M.2 case that houses a 120GB M.2 SSD. There were a few reasons why I opted for this setup. Firstly, SD cards can often fail when hosting web applications for an extended period of time, so I wanted a more reliable storage solution. Additionally, this particular case has excellent cooling, which is essential for ensuring stable performance when running resource-intensive services.  
  
If you are interested in it check it out [here](https://www.pbtech.co.nz/product/SEVRBP0326/Raspberry-Pi-Argon-ONE-M2-Aluminum-Alloy-Top-Case).

## Self-Hosted Services

Now, let's take a look at the three services I'm currently running on my Raspberry Pi 4: Portainer, Nextcloud, and Ghost.

## Portainer

Portainer is an essential tool for me when it comes to managing my Docker containers. Since all of my services run in containers, Portainer makes it incredibly easy to manage and organize them. If you're not familiar with Portainer, I recommend checking out my video on it.

## Nextcloud

Nextcloud is a popular self-hosted alternative to cloud-based storage and collaboration platforms like G-Suite. With Nextcloud, you can store and manage files and images, use the native chat application, and even access a variety of office suite tools with plugins. If you're interested in learning more about Nextcloud, check out my video.

## Ghost

Finally, Ghost is the platform that you're currently reading this blog post on. It's a content management system that makes blogging a breeze. I've tried a variety of other blogging tools - including Jekyll, other static site generators, and Wordpress - but Ghost is by far the easiest to host and manage. If you're curious, I've created a video about Ghost as well.

## Cloudflare Zero Trust

Cloudflare Zero trust is really the core component that ties everything together for me.

For me, Cloudflare Zero Trust is the core component that ties everything together. If you're not familiar with it, Cloudflare Zero Trust is essentially a reverse proxy solution that lets you expose your local services to the internet without having to open any ports on your local router. Instead, you install the Cloudflare Tunnel as a Docker image, which authenticates with Cloudflare and then allows you to set up and expose your services. I've created a video on this topic as well, so be sure to check it out if you're interested. I am being vague here as I have a video on this one as well!

In this post, I've shared my current self-hosting setup, which consists of a Raspberry Pi 4 with an Argon One M.2 case, running Portainer, Nextcloud, and Ghost. These services are all managed through Docker containers, and I use Cloudflare Zero Trust as a reverse proxy solution to expose them to the internet without having to open any ports on my local router. Overall, I've found this setup to be reliable, efficient, and affordable, making it a great choice for anyone interested in self-hosting their own services. If you're interested in learning more about any of these tools or services, be sure to check out my videos for more in-depth information or leave a comment below.
