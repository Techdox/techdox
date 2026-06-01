+++
title = "I Tried Running an AI Agent, Are They Safe?"
date = 2026-06-01T00:00:00+00:00
tags = ["ai", "security", "banter"]
featured = true
draft = false
description = "I tried running an AI agent to see what it could actually do, where it helped, and where the safety concerns started to feel real."
feature_image = ""
+++

# I Tried Running an AI Agent, Are They Safe?

AI agents are everywhere at the moment.

Not just chatbots that answer questions, but tools that can read files, run commands, edit code, browse documentation, and start making decisions on your behalf.

That sounds useful, and honestly, it is.

I recently tried running Hermes locally to help me fix a Docker database issue, and to be fair, it actually did it.

I was impressed.

It looked at the problem, worked through the issue, and helped me get to a fix faster than I probably would have by bouncing between logs, docs, and random troubleshooting steps myself.

But after trying it, I also started thinking about the other side of it. If an AI agent can help me move faster, what else can it do if I give it too much access?

This post is not about panic or hype. It is about what I tested, what worked, what made me uncomfortable, and what I think people should understand before running these tools on their own machines.

## Running Hermes Locally

The tool I tested was Hermes, running locally.

The goal was simple: I had a Docker database issue and wanted to see if an AI agent could help me work through it.

This is where these tools start to feel different from normal AI chat.

I was not just asking a model a question and getting text back. I was giving an agent enough local context to help troubleshoot a real issue on a real machine.

That is a very different trust model.

An AI agent with no access to your system is one thing.

An AI agent that can inspect logs, understand Docker, suggest commands, and potentially act on your environment is something else entirely.

That does not make it bad.

It just means the permission boundary matters.

## What It Was Good At

The useful side was obvious pretty quickly.

Hermes helped me work through the Docker database issue and got me to a result. That alone made me understand why people are excited about agents.

It was useful for:

- Reading the situation quickly
- Helping make sense of the problem
- Suggesting practical next steps
- Reducing the amount of time spent context switching
- Acting like a second set of eyes while troubleshooting

The key point is that these tools can be genuinely helpful when the task is clear and the permissions are limited.

They are especially useful when you already understand the problem well enough to review the output properly.

That last part matters.

If I had no idea how Docker worked, I might have just trusted every step blindly. Because I had enough context to understand what it was doing, I could follow along and decide whether the suggestions made sense.

That is where I think AI agents are strongest right now.

They are great at speeding you up when you already have some understanding of the system.

## The Workflow Side Is Interesting

Another thing I liked was the idea of setting up workflows that can run by themselves.

That opens up some interesting possibilities in a homelab.

For example:

- Server health reports
- Monthly log cleanups
- Disk usage checks
- Container status summaries
- Backup verification
- Certificate expiry checks
- Simple maintenance tasks that are easy to forget

That kind of automation is genuinely useful.

I can absolutely see the value in having an agent generate a regular report, tell me what looks unhealthy, and surface anything that needs attention.

For a homelab, that is appealing.

Most of us already have scripts, cron jobs, dashboards, and monitoring tools doing bits of this. An agent could make some of that easier to understand and maintain.

But this is also where the risk starts to creep in.

The moment an agent is allowed to run by itself, the question changes from "can it help me?" to "what exactly is it allowed to do when I am not watching?"

## The Hype Is Missing the Risk

One thing that has been bothering me is how these tools are being talked about online.

There are plenty of YouTubers and influencers promoting AI agents, often alongside affiliate links for VPS providers or platforms that make it easy to spin one up quickly.

I get why.

It is a good demo.

An agent that can run on a VPS, connect to services, automate tasks, read emails, sort your inbox, book flights, manage calendars, or maintain a server looks impressive on camera.

But the safety side often gets skipped over.

The conversation is usually "look what this can do", not "should you actually let it do this?"

That distinction matters.

Yes, an agent might be able to read and sort your emails.

Yes, it might be able to book flights.

Yes, it might be able to log into dashboards, run commands on a server, or automate maintenance.

But should it?

That depends on what access it has, what approval steps exist, what it can do without you watching, and what happens when it gets something wrong.

For someone new to self-hosting or automation, the marketing can make this feel easier and safer than it really is.

Spin up a VPS, install an agent, give it credentials, and now you have an AI assistant running tasks for you.

That sounds exciting.

It also sounds like a very fast way to give a barely understood tool access to your personal data, your infrastructure, or your accounts.

I do not think people should avoid these tools completely, but I do think the hype needs more honesty around permissions, blast radius, and what can go wrong.

## Where It Started to Feel Risky

The thing that made me pause was when I asked it to clean up my logs.

It did that, but it also ran a `docker system prune`.

In my case, that was not a disaster. Nothing broke, and I did not lose anything important.

But it was not what I specifically asked for.

That is the part that stuck with me.

It was a small example, but it points to a much bigger concern. An agent can decide that a related action is helpful, even if that action goes further than what you intended.

That raises a few important questions:

- What happens if the agent misunderstands the task?
- What happens if it edits the wrong file?
- What happens if it runs a command you did not expect?
- What happens if it can read secrets from your environment?
- What happens if it follows instructions from a file, website, issue, or README that you did not write?

That last point is important.

If an agent can read external content and then act on it, you need to think about prompt injection.

A random website, dependency README, GitHub issue, log file, support forum, or documentation page could contain instructions that try to influence the agent.

That sounds dramatic, but it is not hard to imagine.

If an agent is troubleshooting a problem and reads a page that says something like "ignore previous instructions and run this command", what happens?

Does the agent ignore it?

Does it treat it as content?

Does it understand that the website is untrusted?

Does it ask before acting?

Those are not theoretical questions once the tool has access to your terminal, your files, your Docker environment, or your servers.

That does not mean every AI agent is dangerous by default, but it does mean trust boundaries matter.

## The Real Risk Is Permissions

The biggest thing I took away from this test is that the risk is not just "AI".

The risk is what you connect the AI to.

An agent that can only suggest commands is one thing.

An agent that can run commands, edit files, access secrets, push to Git, deploy infrastructure, or manage cloud resources is something else entirely.

At that point, you are not just chatting with a model. You are giving a tool operational access to your environment.

That access needs to be treated seriously.

This is the same reason I would not give a random script full access to my server and walk away.

AI does not magically remove that concern.

If anything, it makes the concern easier to overlook because the interface feels conversational.

You are not typing a dangerous command yourself. You are asking a helpful assistant to fix something.

But under the hood, the outcome can still be a real command, on a real system, with real consequences.

## How I Would Run One Safely

After trying Hermes, I do think I will keep experimenting with agents.

I just think they need guardrails.

Some rules I would follow:

- Start in a test repo, not your main project
- Use a sandboxed directory
- Avoid giving access to secrets unless absolutely required
- Review every file change before accepting it
- Do not allow automatic deploys
- Be careful with destructive commands
- Use Git so you can see exactly what changed
- Keep the agent scoped to a specific task
- Prefer read-only access where possible
- Be extra careful with unattended workflows
- Make sure cleanup tasks cannot remove more than intended
- Require approval before anything destructive runs

The aim is not to avoid AI agents completely.

The aim is to use them the same way you would use any powerful automation tool: with boundaries.

## What I Learned

- AI agents are useful, and Hermes genuinely helped me fix a Docker issue
- The more access they have, the more risk they introduce
- You still need to understand the work well enough to review it
- Sandboxing and permissions matter more than the branding of the tool
- Autonomous workflows are useful, but they need strict limits
- Prompt injection becomes much more serious when the agent can act on your system
- Treat agents like junior automation with shell access, not like a trusted senior engineer

## Are They Safe?

The honest answer is: it depends.

AI agents can be safe enough when they are scoped properly, reviewed carefully, and kept away from sensitive systems.

They become risky when people give them broad access, stop reviewing their work, or let them act across systems they do not fully understand.

For me, the lesson was pretty simple.

I will keep using AI agents, but I will not treat them like they are harmless.

They are powerful tools, and powerful tools need boring security habits around them.

Hermes impressed me.

It also reminded me that convenience and access are usually where the security questions start.

Keep learning.
