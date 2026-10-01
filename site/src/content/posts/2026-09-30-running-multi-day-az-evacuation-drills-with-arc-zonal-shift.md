---
title: "Running multi-day AZ evacuation drills with ARC Zonal Shift"
description: "Prove your multi-AZ architecture can sustain a real impairment. This post shows how to run a multi-day (48-72 hour) Availability Zone evacuation drill with ARC Zonal Shift across Amazon ECS, Amazon EKS, Amazon RDS for Po"
pubDate: 2026-09-30T19:01:57+00:00
addedAt: 2026-10-01T20:05:21.114227+00:00
source: "AWS Architecture"
category: company_eng
sourceUrl: "https://aws.amazon.com/blogs/architecture/running-multi-day-az-evacuation-drills-with-arc-zonal-shift/"
tags: ["observability", "postgresql"]
heat: 68
score: 0.92827
readMinutes: 1
image: "https://d2908q01vomqb2.cloudfront.net/fc074d501302eb2b93e2554793fcaf50b3bf7291/2026/08/24/ARCHBLOG-1571-1.png"
imageAlt: "Multi-tier architecture spanning three Availability Zones: an Application Load Balancer fronting Amazon ECS and a Network Load Balancer fronting Amazon EKS, with Amazon RDS for PostgreSQL and Amazon Aurora PostgreSQL databases, before evacuating AZ A."
---

Prove your multi-AZ architecture can sustain a real impairment. This post shows how to run a multi-day (48-72 hour) Availability Zone evacuation drill with ARC Zonal Shift across Amazon ECS, Amazon EKS, Amazon RDS for PostgreSQL, and Amazon Aurora PostgreSQL, with step-by-step CLI commands, prerequisites, observability metrics, and restore procedures.

*Reproduced from the AWS Architecture feed. No model was used to write this entry — follow the link for the full article.*
