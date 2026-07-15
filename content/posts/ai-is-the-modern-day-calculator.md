+++
title = "AI Is the Modern-Day Calculator"
date = 2026-07-15T18:53:02+12:00
tags = ["ai", "homelab", "kubernetes"]
featured = false
draft = false
description = "I thought giving an AI agent access to my servers was a terrible idea. A few months later, it was building Kubernetes clusters in my homelab."
feature_image = ""
+++

# AI Is the Modern-Day Calculator

I think it's safe to say that AI is here to stay.

If you're still on the fence, or feel like you're playing catch-up, I was in a similar position until a few months ago. I used AI, but only at the surface level.

At work, we regularly check in on how we're using AI and whether it's helping. My usual answer was something along the lines of:

> "Yeah, it's good at checking the grammar in my emails and helping me troubleshoot things."

That was about it.

I'm normally a nerd for anything new and technical, so I'm not entirely sure why I never went much deeper. Maybe I didn't see the need. Maybe the useful parts were buried under an impressive amount of AI-generated rubbish.

Whatever the reason, that changed after a conversation at work.

## Why would you give AI access to your server?

During one of our catch-ups, we started talking about AI agents and some of the mess people were getting themselves into, especially with tools such as OpenClaw.

My response was fairly predictable:

> "Why would you give AI access to your server?"

To be fair, that's still a reasonable question.

Giving any application access to your infrastructure creates risk. Giving an AI agent terminal access, credentials, and the ability to execute commands deserves even more thought.

But the idea stuck with me.

What could an agent actually do if I gave it a proper task? Not grammar checking. Not rewriting an email. Real infrastructure work.

Eventually, curiosity won.

## This is where Hermes entered the picture

Hermes is an open-source AI agent from Nous Research. Unlike a normal chatbot, Hermes can use tools. It can work with files, run terminal commands, search the web, connect to APIs, and remember useful information between sessions.

It also isn't tied to a single model provider. You can connect it to hosted models from providers such as OpenAI or run models locally if you have the hardware.

Hermes has support for command approvals and isolated terminal environments, but none of that makes agent access automatically safe. You still need to decide what the agent can access, which credentials it receives, and how much damage those credentials could cause.

I've [written separately about the safety side of running an AI agent](/i-tried-running-an-ai-agent-are-they-safe/). For this experiment, I decided to start on dedicated hardware rather than installing it on an existing server.

I took my gaming rig, wiped it, installed Ubuntu Server, and set up Hermes. Once it was running, I connected my OpenAI account and started figuring out what to do with it.

Installing an agent is the easy part.

The awkward question comes next.

Now what?

## A proper first test

At the time, I was planning to build a Kubernetes cluster in my Proxmox environment using kubeadm.

Normally, that would mean creating the virtual machines, configuring the operating systems, installing the container runtime, setting up Kubernetes, deploying the networking layer, and joining the nodes together.

It was a decent-sized project and exactly the sort of thing I wanted to test.

So I gave Hermes SSH access to the environment and asked:

> "Hermes, here is SSH access to my Proxmox environment. Spin up a three-node Kubernetes cluster using kubeadm."

Then it went to work.

I watched as it connected to Proxmox, created the virtual machine template, deployed the VMs, installed Kubernetes, and connected the nodes.

Eventually, it came back with the result:

> "Nick, your cluster is ready."

Right.

That was suspiciously painless.

## Checking its homework

I connected the cluster to Portainer so I could inspect what Hermes had built.

This wasn't just three virtual machines with Kubernetes technically running. The cluster had Calico networking, cert-manager, and monitoring deployed from the start.

The nodes were connected, the workloads were running, and the cluster was usable.

There was still something missing, though. I wanted MetalLB so services could receive addresses on my local network.

I gave Hermes another instruction:

> "MetalLB would be useful. Deploy it into the cluster."

Again, it went away, completed the work, and returned with the result.

No weekend spent copying commands from documentation. No collection of half-finished notes explaining which node I had reached. No wondering whether I had remembered to install the same package on all three machines.

It was just done.

That was the point where I started questioning this way of working.

## Is this lazy?

I know how to build a Kubernetes cluster.

I understand what the agent is doing, and I could have completed the deployment myself. I've done this sort of work before.

So was I being lazy by asking an AI agent to do it?

After thinking about it, I don't believe I was.

AI feels like the modern-day calculator.

A calculator didn't make maths irrelevant. It changed which parts of maths were worth doing manually. You still need to understand the problem, choose the correct calculation, and recognise when the result makes no sense.

AI agents are similar.

Knowing Linux, networking, Kubernetes, and security still matters. In some ways, that knowledge becomes even more important because the agent can make changes much faster than you can.

If you don't understand the environment, you have no reliable way to tell whether the agent did a good job. It might return with complete confidence while leaving you with a broken network, an insecure configuration, or a cluster that falls over the moment something restarts.

AI can help experienced people move faster.

It can also help inexperienced people break things faster.

## My role didn't disappear

During the deployment, my role changed.

Instead of manually typing every command, I described the result I wanted. I gave Hermes access to the environment, watched what it was doing, inspected the finished cluster, and asked for changes when something was missing.

I spent less time copying commands and more time defining what "done" should look like.

That still required technical knowledge. I needed to know that Calico was handling the cluster networking. I needed to understand why MetalLB was useful in my environment. I needed Portainer to inspect the cluster and confirm that the workloads were healthy.

The agent carried out the work, but I was still responsible for the outcome.

That feels like the important shift.

The useful skill may no longer be remembering every command needed to deploy a service. It may be knowing how the pieces fit together, how to describe the outcome clearly, and how to verify that the result is safe and correct.

## This doesn't mean handing AI the keys to production

I'm not suggesting that everyone should give an AI agent unrestricted root access to their production servers.

That would be a terrible takeaway from this experiment.

I started with dedicated hardware and a controlled project. I watched the work as it happened, and I had enough experience with the technology to inspect the result.

If you're experimenting with agents, start somewhere you can afford to make mistakes. Use scoped credentials where possible. Keep backups. Require approval for destructive commands. Make sure you know what the agent can reach before giving it access.

An isolated agent host also doesn't magically protect everything else. Once you give that agent SSH credentials for another system, those credentials become part of its reach.

The goal isn't to remove caution. It's to use the tool without pretending the risks don't exist.

## Are we going to be left behind?

Two people can understand the same technical problem equally well. If one of them completes every repetitive step manually while the other uses an agent and checks the result, the second person is probably going to finish first.

That doesn't make them smarter. It doesn't mean the agent is always right. It means they have a tool that can carry out the routine work much faster.

We accepted this with calculators. We accepted it with search engines, scripts, infrastructure as code, and configuration management. Nobody gets extra points for manually configuring fifty servers when an Ansible playbook can do it consistently.

AI agents feel like the next step in that progression.

My experience over the last few months has changed how I look at AI. I no longer see it as something that checks my grammar or gives me troubleshooting suggestions.

I see it as something I can work alongside.

I provide the context, access, constraints, and expected outcome. The agent carries out the work. I inspect what comes back and remain responsible for the result.

There will always be things I prefer to do myself. There will also be environments where giving an agent access isn't appropriate.

{{< racknerd >}}

## Final thoughts

Refusing to use AI because I can complete the work by hand now feels a bit like refusing to use a calculator because I know how to do long division.

Knowing how to do the work still matters.

Knowing when not to do all of it by hand might matter just as much.
