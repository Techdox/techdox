+++
title = "Umbrel: A Selfhosted Dashboard"
date = 2023-09-27T06:50:19+00:00
tags = ["selfhosting"]
featured = false
draft = false
description = "Umbrel: A Selfhosted Dashboard simplifies self-hosting. From effortless app deployment to user-friendly features, it's perfect for both newcomers and experienced users."
feature_image = "/content/images/2023/09/os-circle.webp"
+++

## Overview

  
Self-hosting can be intimidating, especially for newcomers to concepts like Docker, Linux, Networking, and storage. Many users who want to enter this space can feel overwhelmed by these services. This is where self-hosted dashboards come in – though I'm not sure if that's their official name, it's what I call them.

  
Self-hosted dashboards come in different forms, either as Docker containers or packaged within a Linux distribution like Debian. They simplify the process, eliminating the need to dive into the CLI, Linux, or Docker. Instead, users are presented with a dashboard that resembles something like ChromeOS, complete with an app store for self-hosted services.

![](/content/images/2023/09/image-1.png)

One such dashboard is Umbrel, which you can install using what they call "UmbrelOS." UmbrelOS can be installed either via the UmbrelOS ISO for Raspberry Pis or on top of a running instance of Ubuntu or Debian using their install script. 

![](/content/images/2023/09/image.png)

I covered Umbrel on a Raspberry Pi nearly a year ago, and if you're interested, you can check out that video below.

In this post, we will focus on installing Umbrel on top of a barebones Linux Mint Virtual Machine running in my Proxmox environment. Since Linux Mint is similar to Ubuntu, this should work smoothly.

## Installing UmbrelOS via the install script

![](/content/images/2023/09/Screenshot-2023-09-27-at-6.51.50-PM.png)

Now, let's proceed with the installation on our Linux Mint instance. Following the install instructions, all we need to run is: `curl -L `[`https://umbrel.sh`](https://umbrel.sh)` | bash`

            
                
                
                    
                        
                            
                        
                    
                
                
                    
                        
                            
                                
                            
                        
                        
                            
                                
                                
                            
                        
                        0:00
                        
                            /1:59
                        
                        
                        1×
                        
                            
                                
                            
                        
                        
                            
                                
                            
                        
                        
                    
                
            
            
        

As seen in the clip above, the install script executed successfully, installing Docker and any required Docker containers for Umbrel. It also provides the URL/IP to access our fresh Umbrel deployment.

  
So far, it seems that if you can install Debian or any derivative of Ubuntu, such as Linux Mint, and run a command in the terminal, you can self-host.

  
Now, let's go to the URL provided by the command line output.

![](/content/images/2023/09/image-4.png)

## **Using Umbrel**

The script worked as expected, and we are presented with the welcome page for Umbrel. Setting up a user is straightforward.

![](/content/images/2023/09/image-5.png)

![](/content/images/2023/09/image-6.png)

Here is where the magic happens. Umbrel and other dashboards simplify the entry into self-hosting. As you can see, Umbrel accommodates not only self-hosters but also Bitcoin enthusiasts.

![](/content/images/2023/09/image-7.png)

We are instructed to install our first app, and as I mentioned before, it resembles an app store in terms of ease of use. Let's make NextCloud our first app to deploy. It's as simple as clicking "install" and waiting. Once installed, we can open NextCloud and find our username and password.

![](/content/images/2023/09/image-8.png)

![](/content/images/2023/09/image-9.png)

            
                
                
                    
                        
                            
                        
                    
                
                
                    
                        
                            
                                
                            
                        
                        
                            
                                
                                
                            
                        
                        0:00
                        
                            /0:15
                        
                        
                        1×
                        
                            
                                
                            
                        
                        
                            
                                
                            
                        
                        
                    
                
            
            
        

Just like that, we have NextCloud up and running with just a few clicks. If we return to Umbrel, we can see our dashboard with our newly installed NextCloud application.

![](/content/images/2023/09/image-10.png)

The app store offers a wide range of applications to meet your needs. If something is missing, you can install Portainer from the app store and start deploying your own custom services using Docker with a user-friendly interface. Again, installing Portainer is as simple as a few clicks.

![](/content/images/2023/09/image-11.png)

![](/content/images/2023/09/image-12.png)

If you're interested in learning more about Portainer, visit the Portainer website at [https://portainer.io](https://portainer.io/) and check out the YouTube channel at [https://www.youtube.com/c/portainerio](https://www.youtube.com/c/portainerio).

Upon installing Portainer, you are prompted to change the password, which is good since the default password "changeme" is not secure.

![](/content/images/2023/09/image-13.png)

If we try to ignore this and move on... Well, no we need to change the password.

![](/content/images/2023/09/image-14.png)

Umbrel does a good job of keeping Portainer separate from the underlying containers running on the server, such as NextCloud, Portainer, and Umbrel, providing a clean environment for your custom deployments outside of Umbrel.

![](/content/images/2023/09/image-15.png)

##   
Conclusion

UmbrelOS makes self-hosting incredibly easy, whether you're a newcomer or an amateur in the self-hosting world. Your Umbrel deployment has room to grow alongside your experience in self-hosting.
