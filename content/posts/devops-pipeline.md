+++
title = "My Azure DevOps Terraform Pipeline"
date = 2023-02-01T06:33:00+00:00
tags = []
description = "How I deploy Terraform through Azure DevOps pipelines: feature branches, validation runs, Infracost cost estimates on every PR, and a gated merge to main."
featured = false
draft = false
feature_image = "https://images.unsplash.com/photo-1631624215749-b10b3dd7bca7?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=MnwxMTc3M3wwfDF8c2VhcmNofDE0fHxJVCUyMGRldm9wc3xlbnwwfHx8fDE2Nzk5ODUyNDY&ixlib=rb-4.0.3&q=80&w=2000"
+++

When it comes to deploying Terraform via Pipelines your choices are almost limitless, you can go about it in so many ways, I personally have been deploying a lot of work based projects via Azure DevOps which has led me to also use it for personal projects.

## Pipeline Setup

![None](/content/images/2023/03/image-15.png)

The pipeline setup I use is pretty basic and I won’t go into the weeds of the yaml file etc, but I will cover what it’s doing and how I deploy it.

## The Process

So as you can see from the diagram above, it’s a rather simple concept. Work is done on the feature branch then pushed to Azure DevOps, the Terraform pipeline it run to check it’s correct and working and then a PR is raised to merge it into the main branch.

When this PR is raised, the Infracost pipeline is triggered which this will show you the estimated cost changes

![None](/content/images/2023/03/image-16.png)

Once the PR is approved, the full pipeline can be deployed, which looks like this.

![None](/content/images/2023/03/image-17.png)

{{< racknerd >}}

## Final notes

This is a pretty high level view on how I am deploying Terraform + Infracost with Azure DevOps and I aim to do a walkthrough on the actual pipeline files, but I’m looking to make it a bit more simple first before I do that.
