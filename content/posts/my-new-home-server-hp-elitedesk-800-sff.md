+++
title = "My New Home Server - HP EliteDesk 800 SFF"
date = 2023-08-29T09:45:53+00:00
tags = []
description = "Why I upgraded my homelab from Raspberry Pis and a Zimaboard to a second-hand HP EliteDesk 800 SFF — the specs, the $300 NZD price tag, and what it unlocks."
featured = false
draft = false
feature_image = "https://images.unsplash.com/photo-1484557052118-f32bd25b45b5?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3wxMTc3M3wwfDF8c2VhcmNofDIxfHxzZXJ2ZXJ8ZW58MHx8fHwxNjkzMjk0NDkwfDA&ixlib=rb-4.0.3&q=80&w=2000"
+++

Since I launched my YouTube channel and Blog about 2 years ago (my blog has seen its fair share of creations and destructions over that time), all my content has revolved around self-hosting. To be honest, I initially ventured into the cloud space, but over time, I discovered my true calling in the self-hosting realm.

Up until now, my go-to systems have been single-board computers like Raspberry Pis and my trusty Zimaboard. And truth be told, they've served me remarkably well. They've empowered me to host my website, maintain a private NextCloud instance, and keep my self-hosting documents neatly organized on Bookstack. I never really yearned for more until recently, when I started to envision using my Raspberry Pi and Zimaboard for more intensive content creation, involving frequent OS changes and the avoidance of any 'production' workloads. This realization led me down the path of acquiring something more dedicated to my self-hosting journey.

And so, with open arms, I welcome my 'new' second-hand HP EliteDesk 800 SFF into the fold.

The genesis of this decision traces back to a conversation I had on my work Slack chat. I was seeking recommendations for home servers, being somewhat entrenched in the single-board realm for a while, blissfully unaware of the server landscape. My initial inclination leaned towards a rack server, a choice quickly deemed overkill by my insightful colleagues. They pointed me towards the EliteDesk, a suggestion that eventually set me back $300 NZD, but oh boy, was it worth it!

Allow me to share the impressive specifications this machine boasts right out of the box:

- Intel Core i7-7700 CPU – the cream of the crop in terms of processing power.
- 16GB of RAM.
- A 256GB SSD.
[HP EliteDesk 800 G3 Small Form Factor Business PC Specifications | HP® Customer SupportSpecifications page for HP EliteDesk 800 G3 Small Form Factor Business PC.

![](https://support.hp.com/hp-portal-theme-static/themes/Portal8.0/images/favicon.ico)

IBM Logo

![](https://support.hp.com/static/hp-portal-theme-static/themes/Portal8.0/hp/images/hp-logo-modal.gif)

](https://support.hp.com/nz-en/document/c05369814)

But wait, there's room for more! I have plans to expand the memory to a whopping 64GB this weekend – a prospect that's got me quite pumped. And that's not all on the upgrade front. I've also given the storage situation a considerable boost:

- A 500GB Samsung SSD 980 NVME takes care of the Root and Boot partitions.
- A 1TB SSD now hosts the Home partition.
- The 256GB SSD that came with the EliteDesk has been reborn as an NFS share aptly named 'dump,' which I use to share files across my home network and my lab environment.

The beauty of having a dedicated home server is the newfound flexibility and growth potential it grants me. I envision sticking with this setup for a good while. As I hinted earlier, my Raspberry Pi's and Zimaboard can now be unleashed for more varied content creation. This entails experimenting with different distributions and services, a prospect that excites me to no end.

{{< racknerd >}}

If you're as intrigued as I am and want to delve deeper, I invite you to check out the video below. It provides a visual tour of my new setup and its capabilities.

Feel free to let me know your thoughts, and if you'd like to see more content like this, don't hesitate to reach out. Happy self-hosting, folks!
