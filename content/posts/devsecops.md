+++
title = "DevSecOps"
date = 2023-03-28T06:29:17+00:00
tags = []
description = "Security can't be a surprise at production time. Thoughts from the Cloud Native Summit on shifting from DevOps to DevSecOps and bringing security in from day one."
featured = false
draft = false
feature_image = "https://images.unsplash.com/photo-1667372335962-5fd503a8ae5b?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=MnwxMTc3M3wwfDF8c2VhcmNofDh8fGRldm9wc3xlbnwwfHx8fDE2Nzk5NzcyNjY&ixlib=rb-4.0.3&q=80&w=2000"
+++

I was very fortunate enough to be given a pass to go to the Native Cloud Summit here in Wellington by my work and it was an amazing two days, it allowed me to get an idea of what was happening in the industry and where my thinking and others within my teams thinking aligned with the industry and it allowed me to see that we are currently all facing the same issue, Security and DevOps.

You would have heard the term DevOps thrown around left and right if you work in the cloud and rightly so, it’s becoming the standard for how we design and deploy our cloud environments as well as setting organisation standards, but it seems the industry has an issue with working in where security comes into play, so I thought I would write up my thoughts on this topic.

There’s a common theme in the Cloud space where a project seems to be going along smoothly and things are being deployed to Dev and Test environments without issues and then it comes to deploying to Production and then all the wheels on the projects come to a screaming halt… Security has just been bought in and they are not happy, and they give you a report on their finding of all the things that need to be fixed before your production release can go live…. Say goodbye to that deadline target.

There needs to be a mind shift in the industry where security needs to be seen as much as a project as everyone else who is bought in at the start, security needs to be in the design talks, the build talks and deployment/handover talks so that there is no longer this “Surprised Pikachu face” when they give you the big NO for the production deployment build.

We tend to view security as a blocker or at least a pain in our backside when it comes to projects, but if we take a step back and see what point we bring them into a project, I think we can see where the problem is.

Now, I am not saying every project is like this, but again there seems to be a pretty big gap between Devs and engineers working with security teams on projects and I may be preaching to the choir here, but I guess the point of this blog post is about changing our view of DevOps to be more DevSecOps.

Everything we do, we do we should do it with security in mind from day one, be that we are implementing secure pipeline tools such as SNYK that scan our code and prevent vulnerabilities from entering our builds from day one to having our security team in with us during the very early discussions.

Typing this out, it seems so logical that it doesn’t need to be spoken about but again, I was very surprised how many of us out there has this issue, and it’s time for a mental thinking change.

{{< racknerd >}}

TL: DR DevOps rarely involves security teams during the initial phases of a project where that thinking needs a massive mind shift where they are involved throughout the entire process, just as much as anything else. I see this solving a lot of issues with project deployments.
