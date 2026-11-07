---
title: "Amutable Foundations: A Technical Overview"
description: "Lennart Poettering, Michael Vogt, and Joaquim Rocha have put together a detailed overview of what the Amutable Operating System (AOS) and associated infrastructure will look like. The image-based OS approach enables us t"
pubDate: 2026-11-07T09:32:56+00:00
addedAt: 2026-11-07T09:48:57.905379+00:00
source: "LWN.net"
category: devops_linux
sourceUrl: "https://lwn.net/Articles/1105934/"
tags: ["linux", "python"]
heat: 97
score: 1.08973
readMinutes: 1
hnPoints: 0
hnComments: 0
buzz: 0
---

Lennart Poettering, Michael Vogt, and Joaquim Rocha have put together a detailed overview of what the Amutable Operating System (AOS) and associated infrastructure will look like. The image-based OS approach enables us to enforce some very strict but powerful security properties, which elevate the security posture of the system substantially above traditional Linux systems. Specifically, let's highlight seven major essential security properties of AOS here: No Shell + No SSH + No Language Interpreters . By default AOS does not install a UNIX shell, nor makes remote access via SSH available on the nodes. Moreover, we do not install any of the usual language interpreters (Python, Perl, …) by default. For most nodes a shell or interpreted language support is not required and it removes a whole class of attacks. Signed Images Only . On AOS only images that come with Verity data signed by a s

*Reproduced from the LWN.net feed. No model was used to write this entry — follow the link for the full article.*
