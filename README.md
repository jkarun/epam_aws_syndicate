# epam_aws_syndicate


token: `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`

user name: `jkarun`

git path: `https://jkarun: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@github.com/jkarun/epam_aws_syndicate.git `

## setup process:
1. Setup project & navigate to newly created project folder in cmd
   ```syndicate generate project --name task02```
2. Setup environment variable to newly created project inside git repo
   ```setx SDCT_CONF C:\Users\arun_prasath\workspace\aws_tutorial\epam_aws_syndicate\task02\.syndicate-config-dev```
3. Setup syndicate configs by getting it from sandbox credentials popup
    ```syndicate generate config --name "dev" `
    --region "eu-central-1" `
    --bundle_bucket_name "syndicate-education-platform-custom-sandbox-artifacts-sbox02/134cb1e3/task02" `
    --prefix "cmtr-134cb1e3-" `
    --extended_prefix True `
    --iam_permissions_boundary "arn:aws:iam::905418349556:policy/eo_role_boundary" `
    --access_key "ASIA5FTZDTP2E6Y3MTZY" `
    --secret_key "BfYUPf3aR4zO6wyY69TJEz0fmcb6fmbnWZrIQRjb" `
    --session_token "IQoJb3JpZ2luX2VjEPX//////////wEaCXVzLWVhc3QtMSJGMEQCIFMq/cIxSBGyhvcNAjRAlIFdWam2UiTJlGUKe0cJo0X5AiA6KJMX4pS0F0vNaLrwhV6BxOLzJZVZa35gb+VYqjmuASrmAgj+//////////8BEAAaDDkwNTQxODM0OTU1NiIMp0zx7RtW5bXZiEx/KroCf7Xc3ToEPEDsr8NC3BLniB0ekZ4bcqvSod/VFwTlsZI+IANezJg+GWBtChcOdTyahr5Lvz8R0vCLuq7Pk0j0lI9GOOZ5ITTH8rA9w07+WLSVFYu0lkWGxT2NAmTRwpctDMMVEHEaFOfIlYKkFRIHt3tgCxc2XoTSZfVhAHq0G8RfgDAyhh3ZrHWuvauPHjVkwDh294/4ebp43xVqGx/g2C0tjI/nm3C9faYuKAnwjYPsyXiLsu6nx+qja/Ph00B6sHSdgcgnd1Al6xHuISMUSY0xgb/er83l/IXoMrcrfJHfPHcdS5taux0uzBR6tLh5oe5QuSE9pzRQoto0nMOHhsIf7WY55dlTszTPxXZwFxybrIlCv95W2g2jR2F7wLrdN/Pzl6fWe7rufj9Wkji1vzjKmywF6pt86uYwt7y1tgY6ngEoPQCG+ueN92k5aZ95MQ+mlfOu/lftI0QTkV/v1hReN9QgdRZQ0M/eagK5tWHxxq6fD3V6SoZA6COrP4mMrXBcjl4L6kR4AEbJUSynn2qP3rEwkbVC5ykkID9bP5Nj9Ff/xkl+7OVPqUl4yjs3uM0cTYvfGpHYERH5yt/cS4E9vtzPw5tareNp+yJUfVG6IdEHbZhOHyY3QLVQXSubcw=="```
4. Generate lambda function
   `syndicate generate lambda --name hello_world --runtime python`
5. Generate api gateway.
   a. Generate gateway api and stage name
      `syndicate generate meta api_gateway  --resource_name demo-api  --deploy_stage api --minimum_compression_size 0`
   b. Generate gateway resource
      `syndicate generate meta api_gateway_resource --api_name task3_api --path /hello --enable_cors true`
   c. Generate api method 
      `syndicate generate meta api_gateway_resource_method --api_name task3_api --path /hello --method GET --integration_type lambda --lambda_name cmtr-134cb1e3-hello_world --authorization_type AWS_IAM --api_key_required false`


task 4:

# create project
````syndicate generate project --name task04````
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

