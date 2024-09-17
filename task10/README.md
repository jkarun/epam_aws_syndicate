
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

Hints:

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
    ```
        1. Add cognito user pool to the lambda function dependencies
        The next key-value pair to the lambda configuration(file lambda_config.json)
        
        "dependencies": [
          {
            "resource_name": "${booking_userpool}",
            "resource_type": "cognito_idp"
          }
        ]
        
        2. Define lambda environment variables for Cognito UserPool ID and Client ID
        The next key-value pair to the lambda configuration(file lambda_config.json)
        
        "env_variables": {
          "cup_id": {
          "resource_name": "${booking_userpool}",
          "resource_type": "cognito_idp",
          "parameter": "id"
          },
        "cup_client_id": {
          "resource_name": "${booking_userpool}",
          "resource_type": "cognito_idp",
          "parameter": "client_id"
          }
        }
    '''
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

