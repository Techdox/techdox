+++
title = "Question Everything - Road to CKA"
date = 2025-12-07T06:58:37+00:00
tags = ["kubernetes", "certification"]
featured = false
draft = false
description = "Diving into Kubernetes for the CKA made me realise how fast config drift happens when editing live resources. A DaemonSet lab sparked a deeper understanding of why GitOps matters and why a single source of truth is essential."
feature_image = "https://images.unsplash.com/photo-1667372459607-2cfe842fdc4b?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3wxMTc3M3wwfDF8c2VhcmNofDZ8fGt1YmVybmV0ZXN8ZW58MHx8fHwxNzY1MDkwNjQyfDA&ixlib=rb-4.1.0&q=80&w=2000"
+++

The last few days I have been diving deep into learning Kubernetes for the CKA exam, at the moment I am doing the Kubernetes Fundamentals LFS258 course and I am making sure to go through it slow and really question why things are the way they are.  
  
Working in this space I'm always checking my learnings with real world examples and knowing those real world usecases really help in my understanding of Kubernetes rather than following the lab steps blindly. For example, I deployed a DaemonSet via a manifest that the lab provided but in the next few steps it would get you to run a kubectl edit ds command to make a live update to the Daemon set that was running, but then it got me thinking. Didn't I just deploy this via a YAML file, isn't that now out of date and not the source of truth?   
  
I guess the lab is just teaching you how you can go about editing things on the fly but this is why I am glad I am taking my time as it makes me realise how quickly in a production environment someones Kubernetes deployments could drift if people are making edits via the kubectl edit and then via the manifest which has now drifted.   
  
This is a key reason why I am looking to become experianced in the Kubernetes space so I can become aware of these issues, no doubt in a actual well created setup this would be managed via GitOps which is the source of truth but this now gives reasons and answers to why GitOps etc. The source of truth is always important and with how complicated Kubernetes is this is ever more important and I have only looked at the surface.
