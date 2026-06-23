+++
title = "My Homelab AI Setup: Useful Access, Limited Permissions"
date = 2026-06-23T00:00:00+12:00
tags = ["ai", "homelab", "kubernetes"]
featured = true
draft = false
description = "How Hermes helped migrate my homelab from Docker to Kubernetes using scoped access, local context, and practical automation instead of unlimited permissions."
feature_image = ""
+++

# My Homelab AI Setup: Useful Access, Limited Permissions

I used Hermes to help migrate my homelab from Docker onto Kubernetes.

That sounds a bit dramatic, but it's basically true. I gave Hermes access to the parts of my homelab it needed to work with, including Proxmox and the Docker hosts running my existing services, and told it to review the whole setup and make a migration plan.

The important bit is that I didn't just hand it the keys and walk away. I wanted something useful, not reckless. Hermes needed enough access to actually do the work, but not so much that it could turn my homelab into a cautionary tale.

That balance turned out to matter a lot.

## Why I did it this way

My homelab had grown into a real mess of moving parts.

I had Docker services running on one side, a Proxmox layer underneath it, and a Kubernetes cluster I wanted to bring up properly on top. There were VMs to size correctly, storage to wire in, dashboards to rebuild, and a bunch of services that needed to move without me spending a week doing everything by hand.

That's exactly the kind of thing I wanted Hermes to help with.

Not as a toy. Not as a "look, AI can answer questions" demo. I wanted it to act more like an operator that understands my environment, knows how I deploy things, and can carry out the boring work without me having to babysit every step.

So I told it to review the homelab, plan the migration, and get moving.

## What Hermes actually did

Hermes started by mapping out the environment and building a migration plan.

From there it went to work:

- provisioned a Proxmox template
- spun up three VMs for the Kubernetes cluster
- deployed the cluster
- handled the services that needed to move off Docker
- migrated workloads into Kubernetes
- created Grafana dashboards for the new setup
- resized some of the Proxmox VMs so resources could be shifted where they mattered more
- connected to my NAS and set up storage for the cluster
- documented the whole thing in Obsidian so I'd have runbooks and notes for later

That's the part that genuinely impressed me.

What would have taken me days, maybe longer, got done in a much tighter window because Hermes already understood the shape of my setup and the way I like to run things.

It wasn't magic. It was just a local AI system with enough context to be useful and enough access to do real work.

## Why that worked

The reason this worked is because Hermes wasn't guessing.

It knew:

- how my homelab is laid out
- which services live where
- how I tend to deploy things
- what my Proxmox and Docker setup looks like
- how the Kubernetes side should be built
- what I care about documenting afterward

That matters. A lot.

If an assistant doesn't understand your environment, it's just throwing suggestions at the wall. If it does understand your environment, it becomes genuinely useful.

It can make a plan that fits the actual system instead of some imaginary best-practice diagram. And once it knows your deployment patterns, it stops feeling like a generic chatbot and starts feeling more like a very persistent junior operator with a perfect memory.

That's a good thing, as long as you keep the permissions sane.

## Limited permissions was the whole point

I wanted Hermes to be useful without giving it unlimited reach.

So I kept the access scoped to what it needed for the job. That meant it could help with the Proxmox side, work through the Docker and Kubernetes migration, and handle the related setup work, but it wasn't just roaming around with permanent access to everything in the lab.

That's the right way to do it.

If access is only needed for a task, it should only last for that task. If the AI is helping with infrastructure, it should be able to work, but only within the boundaries you set.

That's what made the setup feel comfortable instead of sketchy. It wasn't "trust the AI with everything." It was "give it enough access to be useful, and then get the access out of the way again."

## What changed after the migration

The biggest difference wasn't just that I now had services running on Kubernetes.

It was that the whole homelab started to feel more structured.

I could:

- deploy new services in a more repeatable way
- keep the cluster resources in the right place
- use Grafana to make the new setup visible
- rely on the NAS properly for storage
- keep documentation alongside the actual setup
- avoid repeating the same admin work over and over

And now, when I want to set up a new service, I can often just send Hermes a GitHub link and tell it to install it.

It already knows how I deploy things.
It already knows my environment.
It already knows the shape of the stack.

So instead of me manually rebuilding the same setup pattern each time, Hermes can take care of it in the way that fits my homelab.

That feels weird, honestly. But it also feels very efficient.

## The part I like most

The best part isn't that Hermes can do the work.

It's that it does the work the way I would have done it, just faster and with less friction.

It's not trying to invent a new workflow every time. It's using the conventions already in the homelab, following the layout I already use, and keeping the documentation current so I can always go back and check how something is wired up.

That's what makes it actually valuable.

A lot of AI demos stop at "look, it can answer a prompt." That's fine, but it's not that interesting.

This is different. This is an AI that helps run a real homelab, understands the environment, and keeps the knowledge in Obsidian so it doesn't disappear after the conversation ends.

That's the bit I wanted.

{{< racknerd >}}

## Final thoughts

I still think this is a bit weird.

Not bad-weird. Just the sort of weird that makes you pause and go, "Right, that actually worked."

Hermes helped me migrate a real homelab, not a toy lab. It handled Proxmox, stood up the Kubernetes side, moved services, built dashboards, adjusted resources, wired in storage, and documented the result.

And it did it in a way that felt controlled, useful, and specific to my setup.

That's the part that matters to me.

Not that it's AI.

Not that it's flashy.

Just that it understands my homelab, does the work the right way, and leaves me with a setup that's easier to live with afterward.

That's the goal, really. Less manual busywork. Better structure. Fewer "I'll remember that later" moments.

And, somehow, a local AI that knows how to help without being handed the entire kingdom.
