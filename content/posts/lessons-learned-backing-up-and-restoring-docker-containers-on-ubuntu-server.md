+++
title = "Lessons Learned: Backing Up and Restoring Docker Containers on Ubuntu Server"
date = 2023-05-10T08:30:31+00:00
tags = ["selfhosting", "zimaboard", "docker"]
featured = false
draft = false
description = "I recently decided to back up and restore a containers on my Zimaboard running Ubuntu Server. What started as a way to correct a mistake in my partitioning turned into a great learning opportunity for me."
feature_image = "https://images.unsplash.com/photo-1637778352878-f0b46d574a04?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=MnwxMTc3M3wwfDF8c2VhcmNofDR8fGRvY2tlcnxlbnwwfHx8fDE2ODM3MDc0MTg&ixlib=rb-4.0.3&q=80&w=2000"
+++

I've been setting up containers on my Zimaboard, which is running the latest version of Ubuntu Server as of writing this. I realized that I had installed all the partitions onto the internal eMMC storage instead of the SSD I had installed. This gave me an opportunity to learn how to back up and restore containers using only Docker commands.

I run Bookstack, which has been deployed using docker-compose. As you can see, it contains the main Bookstack container with a MariaDB database and two volumes for the configuration of both containers.
[

![image.png](https://bookstack.elzim.xyz/uploads/images/gallery/2023-05/scaled-1680-/image.png)

](https://bookstack.elzim.xyz/uploads/images/gallery/2023-05/image.png)

My plan was to back up the compose file, the two volumes, and run a backup of the SQL database as well, just in case the volumes did not work correctly on the new containers. I grabbed these files and folders and added them to a new folder called "backups."
[

![image.png](https://bookstack.elzim.xyz/uploads/images/gallery/2023-05/scaled-1680-/UD2image.png)

](https://bookstack.elzim.xyz/uploads/images/gallery/2023-05/UD2image.png)

I used FileZilla to pull the backups from my server onto my MacBook and reinstalled Ubuntu on the correct drive this time. During the install, I noticed an option to install Docker, which I selected, thinking it would make things quicker. However, this turned out to be the root of my problem, as I'll explain later.

After the installation, I checked that Docker was installed and everything looked good. I installed docker-compose via apt, as I needed it for my installation. Then, I set up my compose file to ensure the mappings were correct for the volumes on the new server and copied over the volumes from my MacBook.

According to what I read on the internet, the volumes and compose file should be enough to back up and run my Bookstack, so I didn't bother running the SQL backup I had made. I ran the "docker-compose up -d" command to spin up my containers. The two containers spun up, and I waited for my Bookstack to come up, but it didn't. Something was broken.

Normally, Bookstack is quick to start up, so I checked the database, and everything looked fine. However, the Bookstack container failed to reach the database. I jumped into the container and checked if I could reach the database via ping, but no luck. I then jumped into the database container and tried to hit it, but also had no luck.
[

![image.png](https://bookstack.elzim.xyz/uploads/images/gallery/2023-05/scaled-1680-/kZ5image.png)

](https://bookstack.elzim.xyz/uploads/images/gallery/2023-05/kZ5image.png)

I tried tearing it all down, removing the volumes, and starting fresh using the SQL database backup instead. However, the same issue persisted. After about 20 minutes of troubleshooting, I started to think that maybe it was Docker itself that was causing the issue. I knew docker-compose was set up correctly, but how was Docker itself set up? It turns out that Docker was installed by snap.  

I don't know if the issue was caused by Docker being installed by snap and compose being installed by apt, but I decided to remove EVERYTHING related to Docker, and reinstalled everything via apt. I removed the volumes and started fresh, running the compose up, and finally, Bookstack was up and running again!

However, when I tried to get my volumes back in, the same error occurred again where the database was not connecting. I blew it all away again, confirmed I had a running base Bookstack working, and then ran the SQL backup. Finally, everything was working!

I did have to reset my MFA on my Bookstack account as it was broken, but this was a straightforward fix. I had to get into the container and run the command to reset my MFA.
[

![image.png](https://bookstack.elzim.xyz/uploads/images/gallery/2023-05/scaled-1680-/EmDimage.png)

](https://bookstack.elzim.xyz/uploads/images/gallery/2023-05/EmDimage.png)

{{< racknerd >}}

This was a great way to gain more experience with backing up and restoring containers. I would love to hear your thoughts on what my issue was and how you would have gone about fixing it.
