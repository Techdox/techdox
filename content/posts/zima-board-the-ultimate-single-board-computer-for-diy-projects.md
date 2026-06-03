+++
title = "ZimaBoard: The Ultimate Single Board Computer for DIY Projects?"
date = 2023-03-30T04:30:15+00:00
tags = ["zimaboard", "selfhosting", "automation"]
featured = false
draft = false
description = "The ZimaBoard is a low-cost single-board server that combines the expandability of an x86 single-board computer with the power of a micro server. "
feature_image = "/content/images/2023/03/Zima-Board_1.8.1.jpg"
+++

Self-hosting and lightweight single-board computing tend to go hand in hand, which is why Raspberry Pis and NUCs are so popular among the self-hosting community. As a self-hoster myself, I'm always on the lookout for the next best thing to host my services on. That's why I was delighted when IceWhale, the creators of ZimaBoard, asked if I would be willing to review it. I was more than happy to oblige!

## Zima Board

ZimaBoard is a low-cost single board server that is tailor-made for the creative and tech-savvy individuals. This cutting-edge device boasts the expandability of an x86 single-board computer (SBC) coupled with the power of a micro server, making it a versatile option for makers and geeks alike.

Unlike the Raspberry Pi and other SBC's the ZimaBoard is based on the x86 architecture which really opens the door for performance and support, we normally see a lot of IoT and SBC's based on ARM and now ARM is not bad and can tend to be pretty powerful as we have seen with the Raspberry Pi 4's but this post is not a comparison between The ZimaBoard and the Raspberry Pi, that is planned for another day.

## ZimaBoard Specs

 The ZimaBoard brings three versions to the table;

![None](/content/images/2023/03/image-20.png)

ZimaBoard 216, ZimaBoard 432 and ZimaBoard 832.

- CPU: Intel Celeron N3350 Dual Core 1.1-2.4GHz (216 Model), or                    Intel Celeron N3450 Quad Core 1.1-2.2GHz (432 & 832 Model)
- RAM: 2G/4G/8G LPDDR4
- Onboard Storage: 16GB/32GB eMMC
- HDD/SSD: 2x SATA 6.0 Gb/s Ports
- LAN: 2x GbE LAN Ports
- USB: 2x USB 3.0
- PCle: 1x PCle 2.0 4x
- Display: 1x Mini-DisplayPort 1.2 4k@60Hz
- TDP: 6W
- Dimensions: (W x D x H) 138.7 x 81.4 x 34.9 mm
- Weight: 278g
- Other Feature: Passive Cooling
- Intel VT-d, VT-x, AES-NI
- Support 4K video transcoding
- H.264 (AVC), H.265 (HEVC), MPEG-2, VC-1
- Pre-installed OS: CasaOS (Based on Debian)
- Compatible OS: Linux / Windows / OpenWrt / pfSense / Android / Libreelec

The Zimaboard I have is the 832 model which comes with a Intel Celeron N3450 Quad Core rated @ 2.2Ghz and 8GB of Memory, that is some serious power and what's even more crazy is that it has two Sata connections and a PCIe slot on the side of the case for any extensions you please, I am immediately thinking of a NVMe expansion for this. 

Looking at the Zimaboard website, they have a good collection of cards for the Zimaboard.

![None](/content/images/2023/03/image-21.png)

## Zimaboard Initial Setup

The setup for the ZimaBoard is straightforward since it uses the CasaOS software on top of Debian to provide a modern, user-friendly experience. If you're not familiar with CasaOS, I have a video on it here.

IceWhale is also the creator of CasaOS, so it makes sense why it comes pre-packaged with the ZimaBoard. However, you're welcome to replace the OS and install whatever you want, as that's the joy of self-hosting. But as a general management center for your ZimaBoard and Docker, it's a pretty good option.

Since CasaOS is already installed, the setup process involves plugging the ZimaBoard into power and an Ethernet cable, then heading to casaos.local, where you'll see a sign-up screen. After that, you're good to go!

I have made a video on the initial setup and an overview of the ZimaBoard here.

{{< racknerd >}}

## Final Thoughts

I'm already pretty impressed with the Zimaboard and plan to put it through its paces over the coming weeks and months from testing different OS's and software to see how it goes as a everyday server for self-hosting.

Stay tuned for more!
