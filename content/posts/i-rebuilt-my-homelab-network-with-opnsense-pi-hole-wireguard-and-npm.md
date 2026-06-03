+++
title = "I Rebuilt My Homelab Network with OPNsense, Pi-hole, WireGuard, and NPM"
date = 2026-05-28T20:27:32+00:00
tags = ["banter", "selfhosting", "zimaboard"]
featured = true
draft = false
description = "I rebuilt my homelab network around OPNsense, Pi-hole, WireGuard, Nginx Proxy Manager, Portainer, Docker, and Kubernetes. Here’s what I’m running, why I chose each piece, and how it all fits together."
feature_image = "/content/images/2026/05/blog.png"
+++

# I Rebuilt My Homelab Network with OPNsense, Pi-hole, WireGuard, and NPM

I’ve been running a homelab for a while now, but after a recent rebuild, I finally have a network setup I’m genuinely happy with.

This isn’t a step-by-step guide. There are already plenty of those out there. This is more of a walkthrough of what I’m running, why I chose it, and a few things that surprised me along the way.

If you’re somewhere around an intermediate level, you know what Docker is, you’ve self-hosted a few things, and you’re comfortable enough in a terminal, this should all make sense without me needing to explain what a subnet is.

## The Hardware

Everything starts with a ZimaBoard.

It’s a small x86 single-board server with dual NICs, which makes it a great fit for a router. It isn’t the most powerful machine in the world, but it doesn’t need to be. Routing, DNS, firewall rules, and a VPN endpoint aren’t exactly asking it to render the next Pixar movie.

One NIC goes to the WAN side, connected to the modem. The other NIC goes to a switch, which everything else on my LAN connects to.

Simple, clean, and exactly what I wanted.

## OPNsense as the Router

I replaced my ISP router with OPNsense running on the ZimaBoard.

If you haven’t used OPNsense before, it’s an open source firewall and router OS based on FreeBSD. At first glance it can look a bit intimidating, especially if you’re coming from a normal consumer router. But once you understand the layout, it becomes surprisingly approachable.

The main reasons I went with OPNsense were:

- Full control over firewall rules
- Native WireGuard support
- Built-in Unbound DNS resolver
- Plugin support for things like Suricata IDS
- No black box, no cloud dependency, and no subscription

The default WAN behaviour is deny-by-default, which is exactly what I want. Nothing is exposed unless I intentionally open it.

Right now, the only thing I expose publicly is the WireGuard UDP port. Everything else stays internal.

## DNS: Pi-hole and Unbound

DNS is one of those things most people set once and never think about again. Usually it gets pointed at Cloudflare, Google, or whatever the ISP provides.

I wanted more control, so I run Pi-hole for ad and tracker blocking, with Unbound behind it for recursive DNS resolution.

In practice, that means:

- Pi-hole handles DNS queries from devices on my network
- Known ad and tracker domains get blocked before they load
- Anything allowed gets passed to Unbound
- Unbound resolves those queries directly instead of forwarding everything to a third-party DNS provider
- DNSSEC validation is enabled

The end result is that my ISP’s DNS servers are bypassed, I’m not sending all my DNS queries to Cloudflare or Google, and ads are blocked network-wide.

That also helps on devices where browser extensions aren’t really an option, like smart TVs, phones, tablets, and random IoT gear.

One of the best parts of this setup has been local DNS.

Every important device or service on my network gets a proper hostname, such as:

- opnsense.techdox.nz
- portainer.techdox.nz
- homeassistant.techdox.nz

These all point to internal IPs. No more remembering which 192.168.x.x address belongs to what. My brain has limited storage, and I’d rather not waste it memorising IP addresses.

## WireGuard VPN

WireGuard runs directly on OPNsense rather than on a separate host.

That was a deliberate choice. Since OPNsense is already my router and firewall, it makes sense to terminate the VPN there too. It integrates cleanly with firewall rules and means I don’t need another machine or container involved just to get remote access.

With WireGuard, I get:

- Remote access to my full LAN from anywhere
- DNS pushed through the tunnel
- Pi-hole blocking while I’m remote
- Local hostnames working outside the house
- A single UDP port open on WAN

That DNS part is worth calling out.

When I’m away from home and connected to WireGuard on my MacBook, my DNS still goes through Pi-hole. That means opnsense.techdox.nz resolves correctly, ads are still blocked, and everything behaves as if I’m sitting on my LAN.

I knew that was the goal, but I didn’t fully appreciate how nice it would feel until I tested it and everything just worked.

That’s the good homelab dopamine right there.

## Nginx Proxy Manager

Nginx Proxy Manager is my reverse proxy.

All of my internal services sit behind it, and it handles TLS termination using proper Let’s Encrypt certificates.

So instead of going to something like:

192.168.x.x:9000

I can just use:

portainer.techdox.nz

It has a valid certificate, no browser warnings, and I don’t have to remember random ports.

A few important details about how this fits together:

- My techdox.nz service subdomains are internal only
- They point to Nginx Proxy Manager’s internal IP
- NPM handles certificates using DNS challenge
- I don’t need to expose ports 80 or 443 to the internet
- It works on LAN and over WireGuard because DNS is handled properly

That last point is what makes the whole thing feel polished. Whether I’m at home or connected remotely, I use the same URLs.

## Portainer

Portainer manages the application side of my homelab, including both Docker and Kubernetes environments.

I use it for everything from Home Assistant, to monitoring tools, to random self-hosted apps I’m testing. Having a web UI for Docker is one of those things that can feel unnecessary until you’re managing more than three containers. Then suddenly it becomes very nice to have.

Portainer itself runs on my main homelab machine, not on the ZimaBoard.

That’s intentional. The ZimaBoard has one job: run OPNsense and keep the network alive. I want that device to stay lean and boring.

Boring infrastructure is good infrastructure.

## What Surprised Me

A few things surprised me during this rebuild.

### Local DNS over VPN just works

I assumed remote access would feel more clunky. I thought I’d either need to expose services publicly, remember internal IPs, or set up some messy split DNS workaround.

But once WireGuard was pushing DNS through the tunnel and my local overrides were in place, everything resolved exactly like I was sitting at home.

That was probably the moment where the whole setup clicked.

### Unbound makes DNS feel properly private

A lot of people who care about DNS privacy switch to a “privacy-respecting” resolver like Cloudflare’s 1.1.1.1.

That’s still better than using random ISP DNS, but it still means you’re handing all your DNS queries to a third party.

With Unbound doing recursive resolution, I’m not forwarding all my queries to one provider. It’s a small detail, but it matters if you care about understanding and controlling your own network.

### OPNsense is more approachable than it first looks

The OPNsense UI is dense, and some of the terminology is closer to enterprise networking than home networking.

But after spending a few hours with it, the logic starts to make sense.

Firewall rules, interfaces, gateways, DNS, DHCP, VPNs, NAT, it all starts clicking together. And once it does, going back to a consumer router feels very limiting.

{{< racknerd >}}

## Is It Worth It?

If you’re asking whether you should rebuild your home network like this, the honest answer is: it depends.

If you just want your self-hosted services to run reliably, a simpler setup is perfectly fine. You don’t need to overcomplicate things just for the sake of it.

But if you want to learn how networking actually works, gain proper control over your traffic, and build something you genuinely understand, this kind of setup is absolutely worth it.

I rebuilt my network because I wanted to properly learn OPNsense.

I ended up understanding DNS, VPNs, reverse proxying, certificates, and firewalling much better than I did before.

That’s the real value of homelabbing.

Not just running services, but learning how all the pieces fit together.

Keep learning.
