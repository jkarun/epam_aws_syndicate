# conda env
   `conda activate aws_syndicate_venv`

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
   `syndicate generate lambda --name api_handler --runtime python`
5. Generate api gateway.
   a. Generate gateway api and stage name
      `syndicate generate meta api_gateway  --resource_name demo-api  --deploy_stage api --minimum_compression_size 0`
   b. Generate gateway resource
      `syndicate generate meta api_gateway_resource --api_name task3_api --path /hello --enable_cors true`
   c. Generate api method 
      `syndicate generate meta api_gateway_resource_method --api_name task3_api --path /hello --method GET --integration_type lambda --lambda_name cmtr-134cb1e3-hello_world --authorization_type AWS_IAM --api_key_required false`


## task 4:

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


## Commands to create sqs and sns
    `syndicate generate meta sqs_queue  --resource_name async_queue`
    `syndicate generate meta sns_topic  --resource_name lambda_topic --region eu-central-1`



## Configure Lambda to be Triggered by the Queue:

Modify the Lambda function configuration to be triggered by the SQS queue using Syndicate.

## Implement the Logic of the 'SQS Handler' Function:

In the Lambda function code, implement the logic to print the content of the SQS message to CloudWatch Logs.

## Build and Deploy Project with the Syndicate Tool:

Use the aws-syndicate tool to build and deploy your project, including the 'SQS Handler' Lambda and the configured SQS queue.

syndicate generate meta iam_role --resource_name sqs_handler-role --principal_service lambda --predefined_policies AWSLambdaSQSQueueExecutionRole 


## task05 AWS Lambda + DynamoDB Integration 

This task involves deploying a Lambda function, an API Gateway, and a DynamoDB table named 'Events.' 
The goal is to create an API endpoint that saves incoming events to the 'Events' table in DynamoDB. 
The API must expose a /events POST resource.

Resources Names

Please note it is obligatory to stick to the following resources naming in order to pass the task:
    - Lambda Function: api_handler

API Gateway:
    - API Name: task5_api
    - Stage Name: api

Resources:
    - /events POST
    - DynamoDB Table: Events 

AWS-Syndicate aliases usage

    In case of usage of AWS-syndicate aliases for deployment of the task-related resources please make sure that you are using the next key-value pair:
    target_table: Events

### task 05 commands
    `syndicate generate project --name task05`
    `syndicate generate lambda --name api_handler --runtime python`
    `setx SDCT_CONF C:\Users\arun_prasath\workspace\aws_tutorial\epam_aws_syndicate\task05\.syndicate-config-dev`

    Generate api gateway.
       a. Generate gateway api and stage name
          `syndicate generate meta api_gateway  --resource_name task10_api  --deploy_stage api --minimum_compression_size 0`
       b. Generate gateway resource
          `syndicate generate meta api_gateway_resource --api_name task5_api --path /events --enable_cors true`
       c. Generate api method 
          `syndicate generate meta api_gateway_resource_method --api_name task5_api --path /events --method POST --integration_type lambda --lambda_name api_handler --authorization_type AWS_IAM --api_key_required false`
    
    Create dynamo db
        syndicate generate meta dynamodb --resource_name Events --hash_key_name Id --hash_key_type N --sort_key_name Category --sort_key_type S --read_capacity 1 --write_capacity 1 

## task 06
Resources Names

Please note it is obligatory to stick to the following resources naming in order to pass the task:

    Lambda Function: audit_producer
    DynamoDB Table 1: Configuration
    DynamoDB Table 2: Audit

AWS-Syndicate aliases usage

    In case of usage of AWS-syndicate aliases for deployment of the task-related resources please make sure that you are using the next key-value pair:
    target_table: Audit


### Commands
    project creation: 
        syndicate generate project --name task06
    
    lambda:
        syndicate generate lambda --name audit_producer --runtime python
        
    dynamo db:
        syndicate generate meta dynamodb --resource_name Configuration --hash_key_name id --hash_key_type S --read_capacity 1 --write_capacity 1 
        syndicate generate meta dynamodb --resource_name Audit --hash_key_name id --hash_key_type S --read_capacity 1 --write_capacity 1 



## task07 

### Resources Names

    Please note it is obligatory to stick to the following resources naming in order to pass the task:
    
        Lambda Function: uuid_generator
        CloudWatch Rule: uuid_trigger
        S3 Bucket: uuid-storage
    
### commands of task07
    lambda: 
        syndicate generate lambda --name uuid_generator --runtime python
    
    S3 bucket:
        syndicate generate meta s3_bucket --resource_name uuid-storage --location eu-central-1 

    cloud watch rule:
        syndicate generate meta cloudwatch_event_rule --resource_name uuid_trigger --rule_type schedule --expression "rate(10 minute)" --region eu-central-1 


## task08 lambda with layers
    command to create layer
         syndicate generate lambda_layer --name "meteo_api_layer" --runtime "python" --link_with_lambda "api_handler"


# task10 Serverless API + Cognito Integration
```
The Goal Of This Task is...

To deploy a serverless API with the specified resources using AWS Lambda, DynamoDB for data storage, and Amazon Cognito for user authentication. The task is to create the API service for Tables Booking at your favorite restaurant.

The following API resources must be defined:

1. /signup POST

    Request:

     {
         "firstName": // string
         "lastName": // string
         "email": // email validation
         "password": // alphanumeric + any of "$%^*", 12+ chars
     }

    Response:

STATUS CODE:

    200 OK (Sign-up process is successful)
    400 Bad Request (There was an error in the request.)

PLEASE NOTE: To prevent email quota errors during verification when integrating with Cognito UserPool:
For Java:

For Python:

For Node.js:

2. /signin POST

    Request:

     {
         "email": // email
         "password": // alphanumeric + any of "$%^*", 12+ chars
     }

    Response:

     {
         "accessToken": // string
     }

STATUS CODE:

    200 OK (The request has succeeded. The server has processed the sign-in request, and the provided credentials (email and password) were valid. The response contains an $access token, which will be used for subsequent authenticated requests.)
    400 Bad Request (There was an error in the request.)

AWS User Pool tokens have different roles: the identity token (ID token) authenticates users to resource servers, and the access token authorizes API operations. For example, use the ID token to call an API with Cognito as the authorizer in AWS API Gateway, and the access token to allow users to modify attributes; their headers are similar, but they use different keys. Essentially, in the case of Cognito the ID token should be used as value of accessToken in the /signin response.

3. /tables GET

    Headers:
    Authorization: Bearer $accessToken
    Request: {}
    Response:

     {
         "tables": [
             {
                 "id": // int
                 "number": // int, number of the table
                 "places": // int, amount of people to sit at the table
                 "isVip": // boolean, is the table in the VIP hall
                 "minOrder": // optional. int, table deposit required to book it
             },
             ...
         ]
     }

STATUS CODE:

    200 OK (The request has succeeded. The server has processed the request and has returned a list of tables as specified in the response body. Each table includes details such as its ID, number, capacity, whether it's in the VIP hall, and optionally, the minimum order required to book it.)
    400 Bad Request (There was an error in the request.)

4. /tables POST

    Headers:
    Authorization: Bearer $accessToken
    Request:

     {
         "id": // int
         "number": // int, number of the table
         "places": // int, amount of people to sit at the table
         "isVip": // boolean, is the table in the VIP hall
         "minOrder": // optional. int, table deposit required to book it
     }

    Response:

{
  "id": $table_id // int, id of the created table
}

STATUS CODE:

    200 OK (The request has succeeded. The server has successfully created a new table based on the information provided in the request body. The response contains the ID of the newly created table.)
    400 Bad Request (There was an error in the request.)

5. /tables/{tableId} GET

    Headers:
    Authorization: Bearer $accessToken
    Request: {}
    Response:

     {
         "id": // int
         "number": // int, number of the table
         "places": // int, amount of people to sit at the table
         "isVip": // boolean, is the table in the VIP hall
         "minOrder": // optional. int, table deposit required to book it
     }

STATUS CODE:

    200 OK (The request has succeeded. The server has processed the request and has returned information about the table specified by {tableId}. The response body contains details such as the table's ID, number, capacity, whether it's in the VIP hall, and optionally, the minimum order required to book it.)
    400 Bad Request (There was an error in the request.)

6. /reservations POST

    Headers:
    Authorization: Bearer $accessToken
    Request:

     {
         "tableNumber": // int, number of the table
         "clientName": //string
         "phoneNumber": //string
         "date": // string in yyyy-MM-dd format
         "slotTimeStart": // string in "HH:MM" format, like "13:00",
         "slotTimeEnd": // string in "HH:MM" format, like "15:00"
     }

    Response:

     {
         "reservationId": // string uuidv4
     }

STATUS CODE:

    200 OK (The reservation was successfully created. The server has processed the request, and a new reservation has been successfully added to the system.)
    400 Bad Request (There was an error in the request. Possible reasons include invalid input, table not found, or conflicting reservations.)

7. /reservations GET

    Headers:
    Authorization: Bearer $accessToken
    Request: {}
    Response:

     {
         "reservations": [
             {
                 "tableNumber": // int, number of the table
                 "clientName": //string
                 "phoneNumber": //string
                 "date": // string in yyyy-MM-dd format
                 "slotTimeStart": // string in "HH:MM" format, like "13:00",
                 "slotTimeEnd": // string in "HH:MM" format, like "15:00"
             }
         ]
     }

STATUS CODE:

    200 OK (The request has succeeded. The server has provided a list of reservations as specified in the response body.)
    400 Bad Request (There was an error in the request.)

Resources Names

Please note it is obligatory to stick to the following resources naming in order to pass the task:
- Lambda Function: api_handler
- Cognito UserPool: simple-booking-userpool

API Gateway:

    API Name: task10_api
    Stage Name: api

Resources:

    /signup POST
    /signin POST
    /tables POST
    /tables GET
    /reservations POST

    /reservations GET

    DynamoDB Table 1: Tables
    DynamoDB Table 2: Reservations

AWS-Syndicate Aliases Usage

In case of usage of AWS-syndicate aliases for deployment of the task-related resources please make sure that you are using the next key-value pairs:
- tables_table: Tables
- reservations_table: Reservations
- booking_userpool: simple-booking-userpool
```
## task10 guide

Guide for task - Serverless API + Cognito Integration
Step 1. Generate Project:

    Use aws-syndicate to generate a new project. This will set up the basic structure needed for your serverless API deployment.

syndicate generate project --name task10

Change the current working directory to "task10"

    cd task10/

Use aws-syndicate to generate a config for your project.
    This will set up configuration files syndicate.yml and syndicate_aliases.yml that may be edited later.
    The command with all filled-in parameters can be found in the "Sandbox credentials" pop-up window of the task definition

    syndicate generate config

If you plan to deploy your project to the Sandbox account please use the whole command or parameters from the page with the task definition.

Remember to set the environment variable SDCT_CONF pointing to the project configuration as mentioned in the result of the generate_config command
Step 3. Generate Lambda:

Inside your project, use aws-syndicate to generate a Lambda function. This step will create the necessary files and configurations.

    syndicate generate lambda --name api_handler --runtime java|nodejs|python

For Node.js Runtime

    Set up correct permissions for the lambda function by editing the IAM policy of the IAM role attached to the lambda. The role and the policy can be found in the file deployment_resources.json.

The policy with enough permissions level:

    "lambda-basic-execution": {
        "policy_content": {
          "Statement": [
            {
              "Action": [
                "logs:CreateLogGroup",
                "logs:CreateLogStream",
                "logs:PutLogEvents",
                "dynamodb:GetItem",
                "dynamodb:Query",
                "dynamodb:PutItem",
                "dynamodb:Batch*",
                "dynamodb:DeleteItem",
                "dynamodb:Scan",
                "cognito-idp:DescribeUserPool",
                "cognito-idp:GetUser",
                "cognito-idp:ListUsers",
                "cognito-idp:AdminCreateUser",
                "cognito-idp:AdminInitiateAuth",
                "cognito-idp:GetIdentityProviderByIdentifier",
                "cognito-idp:ListUserPools",
                "cognito-idp:ListUserPoolClients",
                "cognito-idp:AdminRespondToAuthChallenge",
                "cognito-idp:AdminConfirmSignUp"
              ],
              "Effect": "Allow",
              "Resource": "*"
            }
          ],
          "Version": "2012-10-17"
        },
        "resource_type": "iam_policy"
      }

Step 4. Generate Cognito Metadata:

    Use aws-syndicate to generate metadata for Amazon Cognito Userpool to handle user authentication.

syndicate generate meta cognito_user_pool --resource_name simple-booking-userpool

    Configure the user pool app client by editing the cognito user pool definition in the file deployment_resources.json.

Minimal enough client configuration

    "client": {
          "client_name": "client-app",
          "generate_secret": false,
          "explicit_auth_flows": [
            "ALLOW_ADMIN_USER_PASSWORD_AUTH",
            "ALLOW_CUSTOM_AUTH",
            "ALLOW_USER_SRP_AUTH",
            "ALLOW_REFRESH_TOKEN_AUTH"
          ]
        }
      }

Step 5. Generate API Gateway metadata

Use aws-syndicate to generate metadata for API Gateway to handle user requests.

    syndicate generate meta api_gateway --resource_name task10_api --deploy_stage api

Generate API Gateway authorizer metadata

Use aws-syndicate to generate metadata for the API Gateway authorizer to couple the Cognito User Pool with the API Gateway.

    syndicate generate meta api_gateway_authorizer --api_name task10_api --name authorizer --type COGNITO_USER_POOLS --provider_name simple-booking-userpool

Generate API Gateway resources(paths) and methods metadata

Use aws-syndicate to generate metadata for the API Gateway resources(paths) needed for the task.

signin

    syndicate generate meta api_gateway_resource --api_name task10_api --path /signin --enable_cors true
    syndicate generate meta api_gateway_resource_method --api_name task10_api --path /signin --method POST --integration_type lambda --lambda_name api_handler

signup

    syndicate generate meta api_gateway_resource --api_name task10_api --path /signup --enable_cors true
    syndicate generate meta api_gateway_resource_method --api_name task10_api --path /signup --method POST --integration_type lambda --lambda_name api_handler

tables

    syndicate generate meta api_gateway_resource --api_name task10_api --path /tables --enable_cors true
    
    syndicate generate meta api_gateway_resource_method --api_name task10_api --path /tables --method GET --integration_type lambda --lambda_name api_handler --authorization_type CUSTOM --authorizer_name authorizer
    
    syndicate generate meta api_gateway_resource_method --api_name task10_api --path /tables --method POST --integration_type lambda --lambda_name api_handler --authorization_type CUSTOM --authorizer_name authorizer

tables/{tableId}

    syndicate generate meta api_gateway_resource --api_name task10_api --path /tables/{tableId} --enable_cors true
    
    syndicate generate meta api_gateway_resource_method --api_name task10_api --path /tables/{tableId} --method GET --integration_type lambda --lambda_name api_handler --authorization_type CUSTOM --authorizer_name authorizer

reservations

    syndicate generate meta api_gateway_resource --api_name task10_api --path /reservations --enable_cors true
    
    syndicate generate meta api_gateway_resource_method --api_name task10_api --path /reservations --method GET --integration_type lambda --lambda_name api_handler --authorization_type CUSTOM --authorizer_name authorizer
    
    syndicate generate meta api_gateway_resource_method --api_name task10_api --path /reservations --method POST --integration_type lambda --lambda_name api_handler --authorization_type CUSTOM --authorizer_name authorizer

**Hints:**

To simplify the task solving we recommend using API Gateway proxy integration. With this integration type, API Gateway simply passes the entire request and response between the frontend and the backend.
To enable proxy integration add the next key pair to the definition of every resource methods:

    "enable_proxy": true

Please be aware of the response model format requirements with proxy integration

      {
        statusCode: "...",            // a valid HTTP status code
        headers: { 
            custom-header: "..."      // any API-specific custom header
        },
        body: "...",                  // a JSON string.
        isBase64Encoded:  true|false  // for binary support
      }

More details about API Gateway integrations can be found here
Step 6. Generate DynamoDB Table Metadata:

Use aws-syndicate to generate metadata for a DynamoDB table to store information about tables and reservations.

Tables

    syndicate generate meta dynamodb --resource_name Tables --hash_key_name id --hash_key_type S

Reservations

    syndicate generate meta dynamodb --resource_name Reservations --hash_key_name id --hash_key_type S

Step 7. Configure syndicate aliases:

    To pass resource names to the solution code we strongly recommend using the syndicate aliases
    To use the task-related aliases:
    add the next key pairs to the file syndicate_aliases.yml

tables_table: Tables
reservations_table: Reservations
booking_userpool: simple-booking-userpool

In the file deployment_resources.json rename your resources the next way:
"Tables" -> "${tables_table}"
"Reservations" -> "${reservations_table}"
simple-booking-userpool -> "${booking_userpool}"
Configure the lambda environment variables according to the programming language, see details here

Step 8. Configure Resolving of Cognito User Pool ID and Client ID to Lambda Environment variables
For Python and NodeJS

For Java

As a result, during deployment, the Syndicate will set the Cognito UserPool ID and Client ID as values of according environment variables.

More details about dynamic parameters for environment variables:

    Python/NodeJS
    Java

AWS-syndicate project examples:

    Python
    NodeJS
    Java

Step 9. Implement the Logic of the Function:

In the Lambda function code, implement the logic for each API resource according to the provided specifications in the task definition.
Include the necessary Cognito authentication checks for authenticated resources.

Step 10. Build and Deploy Project with the Syndicate Tool:

Use the aws-syndicate tool to build and deploy your project, including the Lambda function, DynamoDB table, and Cognito configuration.

    syndicate build

    syndicate deploy

Step 11. Test the Application:

Use an API client (Postman, Insomnia) to test each API resource, including signup, signin, fetching tables, fetching a specific table, making reservations, and fetching reservations.

Step 12. Clean Resources:

After testing, use the aws-syndicate tool or AWS Management Console to delete the resources (Lambda function, DynamoDB table, and Cognito configuration) to avoid charges.

    syndicate clean

