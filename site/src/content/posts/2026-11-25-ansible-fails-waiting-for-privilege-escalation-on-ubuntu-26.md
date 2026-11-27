---
title: "Ansible Fails waiting for privilege escalation on Ubuntu 26"
description: "I've slowly been moving my servers from Ubuntu 22 and 24 to 26 this year, and noticed my Ansible automation starts failing if I have password protection for sudo use: $ ansible-playbook main.yml -K BECOME password: PLAY "
pubDate: 2026-11-25T21:43:00+00:00
addedAt: 2026-11-25T21:47:51.717332+00:00
source: "Jeff Geerling"
category: deep_dives
sourceUrl: "https://www.jeffgeerling.com/blog/2026/ansible-fails-become-ubuntu2604/"
tags: ["ansible", "privilege-escalation", "rust"]
heat: 100
score: 1.82691
readMinutes: 1
hnPoints: 1
hnComments: 0
buzz: 11
---

I've slowly been moving my servers from Ubuntu 22 and 24 to 26 this year, and noticed my Ansible automation starts failing if I have password protection for sudo use: $ ansible-playbook main.yml -K BECOME password: PLAY [Security] ******************************************************* TASK [Gathering Facts] *********************************************************************** fatal: [my-server.local]: FAILED! = msg: 'Timeout (12s) waiting for privilege escalation prompt: ' Apparently Ubuntu's been rewriting system utilities in Rust, and the sudo-rs version that ships on Ubuntu 26.04 has some incompatiblities with the sudo I've used on servers for 20+ years.

*Reproduced from the Jeff Geerling feed. No model was used to write this entry — follow the link for the full article.*
