---
title: "How Clario technology detects PHI/PII in DICOM images using Amazon Bedrock"
description: "Clario, part of Thermo Fisher Scientific, uses Amazon Bedrock and Amazon Textract to automatically detect protected health information (PHI) and personally identifiable information (PII) across thousands of DICOM image s"
pubDate: 2026-08-19T14:29:31+00:00
addedAt: 2026-09-11T10:12:15.526655+00:00
source: "AWS Architecture"
category: company_eng
sourceUrl: "https://aws.amazon.com/blogs/architecture/how-clario-automates-phi-pii-detection-in-dicom-images-using-amazon-bedrock/"
tags: ["tech"]
heat: 47
score: 0.27461
readMinutes: 1
image: "https://d2908q01vomqb2.cloudfront.net/fc074d501302eb2b93e2554793fcaf50b3bf7291/2026/08/03/ARCHBLOG-1466-1.png"
imageAlt: "Architecture diagram showing DICOM images uploaded to Amazon S3, requests routed through Amazon API Gateway to detection on Amazon EKS using Amazon Textract and Amazon Bedrock, with metadata stored in Amazon RDS"
---

Clario, part of Thermo Fisher Scientific, uses Amazon Bedrock and Amazon Textract to automatically detect protected health information (PHI) and personally identifiable information (PII) across thousands of DICOM image slices in clinical trials, covering both metadata tags and text burned into the image pixels.

*Reproduced from the AWS Architecture feed. No model was used to write this entry — follow the link for the full article.*
