---
title: "How United Airlines streams database changes to Apache Iceberg with Amazon Data Firehose"
description: "United Airlines built a near-real-time change data capture pipeline that replicates reference data from Amazon Aurora MySQL to open Apache Iceberg tables using AWS DMS, Amazon Kinesis Data Streams, and Amazon Data Fireho"
pubDate: 2026-11-18T20:37:39+00:00
addedAt: 2026-11-19T22:43:39.042308+00:00
source: "AWS Architecture"
category: company_eng
sourceUrl: "https://aws.amazon.com/blogs/architecture/how-united-airlines-streams-database-changes-to-apache-iceberg-with-amazon-data-firehose/"
tags: ["aws"]
heat: 64
score: 0.92627
readMinutes: 1
image: "https://d2908q01vomqb2.cloudfront.net/fc074d501302eb2b93e2554793fcaf50b3bf7291/2026/11/16/ARCHBLOG-1326-1.png"
imageAlt: "Architecture diagram of the near-real-time CDC pipeline inside the AWS Cloud, with seven numbered steps. Inside a VPC, AWS DMS Serverless (1) reads binlog changes from Amazon Aurora MySQL, using source endpoint credentials from AWS Secrets Manager. DMS writes the change events to Amazon Kinesis Data Streams (2). Amazon Data Firehose (3) reads the stream and invokes an AWS Lambda transform function (4), which returns transformed records. Firehose writes Parquet data files to an Apache Iceberg table in Amazon S3 (5) and commits each snapshot to the AWS Glue Data Catalog (6). The query engines, Amazon Athena and Amazon Redshift Serverless (7), read data files from S3 and look up table metadata in the Data Catalog. A legend distinguishes solid data-flow arrows from dashed metadata and credential arrows."
hnPoints: 0
hnComments: 0
buzz: 0
---

United Airlines built a near-real-time change data capture pipeline that replicates reference data from Amazon Aurora MySQL to open Apache Iceberg tables using AWS DMS, Amazon Kinesis Data Streams, and Amazon Data Firehose. This post shows how to reproduce the serverless, multi-engine analytics pattern with AWS CloudFormation.

*Reproduced from the AWS Architecture feed. No model was used to write this entry — follow the link for the full article.*
