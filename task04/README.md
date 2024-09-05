# create project
````syndicate generate project --name task02````
then set project path
```setx SDCT_CONF C:\Users\arun_prasath\workspace\aws_tutorial\epam_aws_syndicate\task04\.syndicate-config-dev```
then config aws creds

# task releate commands and notes

## Resources Names

    Please note it is obligatory to stick to the following resources naming in order to pass the task:
        Lambda Function 1: sqs_handler
        SQS Queue: async_queue
        Lambda Function 2: sns_handler
        SNS Topic: lambda_topic

## Commands to create lambda
    `syndicate generate lambda --name sqs_handler --runtime python`
    `syndicate generate lambda --name sns_handler --runtime python`
    
    remove alais and versioning from lambda configs and add auth type in url config


## Commands to create sqs
    `syndicate generate meta sqs_queue  --resource_name async_queue`
    `syndicate generate meta sns_topic  --resource_name lambda_topic --region eu-central-1`



## Configure Lambda to be Triggered by the Queue:

Modify the Lambda function configuration to be triggered by the SQS queue using Syndicate.

## Implement the Logic of the 'SQS Handler' Function:

In the Lambda function code, implement the logic to print the content of the SQS message to CloudWatch Logs.

## Build and Deploy Project with the Syndicate Tool:

Use the aws-syndicate tool to build and deploy your project, including the 'SQS Handler' Lambda and the configured SQS queue.

