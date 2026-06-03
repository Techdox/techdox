+++
title = "The Importance of Not Dismissing Docker Swarm: Ensuring Your Application Can Truly Scale"
date = 2023-08-07T00:30:00+00:00
tags = ["banter", "docker"]
featured = false
draft = false
description = "Explore Docker Swarm as a practical tool for testing application scalability before diving into Kubernetes complexities."
feature_image = "https://images.unsplash.com/photo-1542293787938-c9e299b880cc?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3wxMTc3M3wwfDF8c2VhcmNofDEyfHxwb2QlMjBvZiUyMHdoYWxlc3xlbnwwfHx8fDE2OTEzNTYxMjd8MA&ixlib=rb-4.0.3&q=80&w=2000"
+++

Since running my YouTube channel and being part of the self-hosting community, I have seen a question come up quite a bit. Now, the question is very valid, but I don't completely agree with the typical answer.

The question is usually something like, "How do I make my containers highly available?" or "What is the next step after Docker?"

These are valid questions because as we grow our use-cases within Docker and our services need to scale, we naturally start looking for the next solution. What tends to happen is that people will Google or ask online for advice, and the answer often leans towards Kubernetes.

However, I want to remind everyone not to forget about Docker Swarm.

![](/content/images/2023/08/Distracted-Boyfriend-copy-1.jpg)

It's easy to get caught up in the hype of Kubernetes, and how could you not? It's everywhere, and it seems like everyone is using it in some way. Plus, every cloud provider has a solution for it.

What I want to express here is that I personally don't believe Kubernetes is the logical next step when moving from a typical standalone Docker environment. Let me explain why using an example.

My website consists of two Docker containers: Ghost for the front-end and a MySQL database for the back-end – simple enough, right? Now, let's say my site starts to get some serious traffic, and my Docker environment with a single container is not up to scratch. There are reports of users not being able to reach the website, or it's becoming very slow.

After a day, my site is back to normal, but now I'm asking myself, "How do I scale this, so next time this doesn't happen again?"

The next logical step is to test how well my application can scale. Deploying a Kubernetes environment just to start testing my application's scalability doesn't make sense to me. Before I can even get to testing application scaling, I first need to do the following:

1. Understand the fundamentals of Kubernetes
2. Prepare an environment to run Kubernetes on
3. Figure out how to get my Docker containers into Kubernetes – Do I need to use Helm charts? What are Helm charts?
4. Set up storage in Kubernetes
5. ...and the list goes on.

I see this happen a lot, especially in the self-hosting community. The next logical step here is not to set up a new environment and learn an entirely new service like Kubernetes before understanding how my application can scale. Using Kubernetes just for testing that is a huge overkill, and that's where Swarm comes in.

Docker Swarm is already in your Docker environment and can be set up with a simple command.

```
docker swarm init`
```

You can use the commands you're familiar with from using Docker already, and your compose files are still valid and can be tweaked to use Docker Swarm features.

The main advantage here is that I can test how my application scales right here. I can start right away with a horizontal scaling approach for my application without worrying about any infrastructure provisioning or implementing a new service I don't know.

I can focus on creating my application in Swarm, which will allow me to scale out my application and see what needs work. Since my website setup is not stateless and I do require a MySQL database, I can start working on what needs to be implemented to support scaling – Do I need to look at another solution instead, etc.

{{< racknerd >}}

The key point I'm trying to explain is that rather than jumping straight to Kubernetes from Docker, use Swarm as a tool in your kit to ensure the applications you want to scale out can actually do it and get familiar with the concepts of using an orchestrator.

Sticking with Swarm allows you to focus on the main point: "Can my application scale?"

Let me know yout thoughts on this!
