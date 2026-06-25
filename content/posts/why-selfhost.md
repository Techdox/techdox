+++
title = "Why Selfhost?"
date = 2024-03-20T09:01:04+00:00
tags = ["selfhosting"]
featured = false
start_here = true
draft = false
description = "What self-hosting actually is, why people do it, and whether it's worth the effort."
feature_image = "https://images.unsplash.com/photo-1517245386807-bb43f82c33c4?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3wxMTc3M3wwfDF8c2VhcmNofDI5fHxsYXB0b3B8ZW58MHx8fHwxNzEwODc3ODg0fDA&ixlib=rb-4.0.3&q=80&w=2000"
+++

The first thing I ever self-hosted was a WordPress blog on a cheap VPS. It broke within a week — something to do with MySQL, a config file I’d edited without understanding, and a backup I hadn’t taken. I fixed it by wiping the whole thing and starting again.

That’s when I got hooked.

Not because it worked. Because fixing it taught me more in two days than any tutorial had in two months. I’d touched Linux, SSH, DNS, Nginx, MySQL, and file permissions — all under mild panic. That’s hard to replicate any other way.

## The real reason people self-host

Privacy and data sovereignty get mentioned a lot, and they’re legitimate. Knowing your files aren’t being indexed to train someone’s model or scanned for ad targeting is a reasonable thing to care about.

But if I’m honest, that’s not what keeps me going. Learning is. Self-hosting is one of the best forcing functions I’ve found for actually understanding how things work — not just reading about them.

When you host something yourself, you own the full stack. The container, the network, the storage, the reverse proxy, the TLS certificate, the backup strategy. When something breaks — and it will — you have to work out why. That process is where most of the learning actually happens.

## The Apple elephant in the room

I’ll admit it: I run a Mac, use iCloud for some things, and have an iPhone. I write about open-source and self-hosting, and my daily driver is firmly inside the walled garden.

I’ve made peace with this. Self-hosting is about choosing your battles, not winning a purity contest. I self-host things where the trade-off makes sense — my website, my notes server, my homelab monitoring, my VPN. I don’t self-host email, because the operational overhead of running a reliable mail server isn’t worth it to me. That’s a reasonable line to draw.

You’re allowed to self-host selectively. It doesn’t have to be all-or-nothing.

## Should you actually bother?

Depends on what you want out of it.

If you want to learn how infrastructure works — Linux, networking, containers, storage, DNS — then yes, absolutely. There’s no faster path. Set up a Raspberry Pi, a ZimaBoard, or an old mini PC. Deploy something. Watch it break. Fix it.

If you want a Netflix alternative that just works, self-hosting will occasionally frustrate you. Jellyfin is great, but it’s not Netflix. That’s the honest version.

The sweet spot is treating self-hosting as a learning environment that also happens to run useful services. Proxmox for VMs. Docker or Kubernetes for containers. OPNsense for your network. Obsidian synced through your own server instead of their paid tier. These aren’t just projects — they’re skills that transfer directly to real work.

## Where to start

Pick one thing. Something low-stakes that you’d actually use.

Uptime Kuma to monitor your home network. Vaultwarden as a self-hosted Bitwarden. Nginx Proxy Manager to handle your reverse proxy. Any of these will introduce you to Docker, DNS, and enough Linux to be dangerous — without requiring you to rebuild from scratch when it breaks.

Start small, break things on purpose, and build from there. That’s roughly how everyone I know got into this.

