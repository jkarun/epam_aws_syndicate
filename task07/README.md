The Goal Of This Task is...

Deploy a Lambda Function, CloudWatch Rule, and S3 bucket. The application must generate 10 random UUIDs every minute and store them in the S3 bucket within a new file.
Example:

Execution at 12:02

The file with lambda execution start time created in S3 bucket with
the following content:

File Name: ISO time of execution start

File Name Example: "2024-01-01T00:00:00.000Z"

{
    "ids": [
        "9bae6daa-2f72-45d3-ad58-1221de19caaa",
        ... and 9 more
    ]
}

DO NOT FORGET TO CLEAN RESOURCES TO AVOID CHARGES
Resources Names

Please note it is obligatory to stick to the following resources naming in order to pass the task:

    Lambda Function: uuid_generator
    CloudWatch Rule: uuid_trigger
    S3 Bucket: uuid-storage

AWS-Syndicate aliases usage

    In case of usage of AWS-syndicate aliases for deployment of the task-related resources please make sure that you are using the next key-value pair:
    target_bucket: uuid-storage
