---
title: "AI coding agents on Amazon EC2 Mac: How Cognition scales Devin for macOS"
description: "Cognition gave its AI software engineer, Devin, a cloud Mac. Each Devin session gets a fresh macOS VM on Amazon EC2 Mac bare metal hosts, so Devin can build, run, and test iOS and macOS apps."
pubDate: 2026-11-20T01:10:14+00:00
addedAt: 2026-11-20T03:48:26.613582+00:00
source: "AWS Architecture"
category: company_eng
sourceUrl: "https://aws.amazon.com/blogs/architecture/ai-coding-agents-on-amazon-ec2-mac-how-cognition-scales-devin-for-macos/"
tags: ["tech"]
heat: 52
score: 0.8454
readMinutes: 1
image: "https://d2908q01vomqb2.cloudfront.net/fc074d501302eb2b93e2554793fcaf50b3bf7291/2026/11/19/ARCHBLOG-1783-1.png"
imageAlt: "Architecture diagram. Inside an AWS Region, an EC2 Mac Dedicated Host runs two macOS guest VMs, one for each active Devin session. Each guest contains Xcode tools, the iOS Simulator with the app under test, a live view, and an accessibility tree. On the host, a VM manager runs the guests, a snapshot process connects guest disks to snapshot storage, and an Ethernet gateway passes guest traffic to packet filter rules and proxies that allow traffic to approved internet destinations. Also inside the Region, outside the host, the Devin agent on Amazon EC2 connects to the accessibility tree, snapshot storage in Amazon S3 holds session snapshots, and an Auto Scaling group allocates and releases hosts. Outside the Region, the user connects to the live view."
hnPoints: 0
hnComments: 0
buzz: 0
---

Cognition gave its AI software engineer, Devin, a cloud Mac. Each Devin session gets a fresh macOS VM on Amazon EC2 Mac bare metal hosts, so Devin can build, run, and test iOS and macOS apps. Learn how Cognition built it with disk snapshots, a user-space network gateway, prepared guest images, and accessibility-based control.

*Reproduced from the AWS Architecture feed. No model was used to write this entry — follow the link for the full article.*
