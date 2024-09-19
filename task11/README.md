
Guide for task - Open API Specification, Documenting
Step 1: Set Up the Project

    Copy the Project

Copy the 'Task 10' project folder and rename the copy to 'Task 11'.

    cp -R task10/ task11/

Don't include syndicate configuration directory named ".syndicate-config-..." and the project state file .syndicate when you copy 'task10' project.

Change the current working directory to "task11"

    cd task11/

Generate Syndicate Configuration:
The command with all filled-in parameters can be found in the "Sandbox credentials" pop-up window of the task definition

syndicate generate config

Remember to set the environment variable SDCT_CONF pointing to the project configuration as mentioned in the result of the generate_config command
Don't forget to add the task-related syndicate aliases(the next key-pair values in the file syndicate_aliases.yml):

tables_table: Tables
reservations_table: Reservations
booking_userpool: simple-booking-userpool

    Adjust Java Dependencies for Java Runtime


Step 2: Enable CORS

    Ensure CORS is enabled for all resources in your API.
    Include the necessary CORS headers in all responses from your lambda functions:

{
 "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
 "Access-Control-Allow-Origin": "*",
 "Access-Control-Allow-Methods": "*",
 "Accept-Version": "*"
}

Step 3: Update API Gateway Resource

    Rename the API Gateway resource from 'task10_api' to 'task11_api' in the deployment_resources.json file.

Step 4: Build and Deploy Project with the Syndicate Tool:

Build a bundle and deploy the project to AWS using the Syndicate CLI.

syndicate build

syndicate deploy

Step 5: Export API Gateway Resource

    Use the following command to export the API Gateway resource to OpenAPI Specification v3. This command will generate a file named '$api-id_oas_v3.json' containing Task 11's API in OpenAPI Specification v3 format(the file will be placed in the export subdirectory of your project directory):

syndicate export --resource_type api_gateway --dsl oas_v3

Step 6: Update Deployment Resources

    Open the deployment_resources.json file in the project 'Task 11'.
    Remove the resource named 'task11_api' of type 'api_gateway'. From now your API Gateway will be managed by the syndicate via open API specification.

Step 7: Update OAS File

Make your API gateway well-documented by editing previously exported OpenAPI specification file:
- Add request and response schemas to the OpenAPI specification.
- Document possible errors thrown.
- Add summary and description to resource methods.

DEPLOYING NEW ENVIRONMENT CONTAINING API DEFINITION OASv3

1. Security Schema for OAS Document(file '$api-id_oas_v3.json'):

Please, take a look at the 'x-amazon-apigateway-authorizer' object and it's 'providerARNS' property - it contains the ARN of the target Cognito UserPool.

As you are provisioning the new environment, we consider the Cognito UserPool does not exist yet and we don't know the actual ARN. The identifier of the User Pool is the combination of the deployment region and a unique ID of the pool. That is why the ARN can't be generated before it is created.

Because the Cognito UserPool is also defined in the Syndicate's deployment resources file, replace the 'providerARNs' property with the following one:

"x-syndicate-cognito-userpool-names": ["${booking_userpool}"]

Here, we're setting up the security rules for the API Gateway when we deploy it from scratch, using an OAS file that Syndicate exported from another environment:

"securitySchemes": {  
    "authorizer": {  
    "type": "apiKey",  
    "name": "Authorization",  
    "in": "header",  
    "x-amazon-apigateway-authtype": "cognito_user_pools",  
    "x-amazon-apigateway-authorizer": {  
        "x-syndicate-cognito-userpool-names": ["${booking_userpool}"],
    "type": "cognito_user_pools"  
    }  
  }  
}  

During the 'syndicate deploy' command execution the syndicate will create resources in configured AWS Account according to defined priorities: Cognito UserPool will be created before the API Gateway. This allows Syndicate to create the Cognito UserPool, obtain it's ARN and replace the 'x-syndicate-cognito-userpool-names' property with the expected 'providerARNs' and the actual ARN of the UserPool referenced in the value.

1.2 Build the bundle

syndicate build

1.3 Update API Gateway

syndicate update -resources task11_api

Step 8: Add an S3 bucket for hosting Swagger UI

    Add the S3 bucket resource with website hosting configured to your Syndicate deployment resources file.

syndicate generate meta s3_bucket --resource_name api-ui-hoster --static_website_hosting True

Step 9: Add Swagger UI Resource

    Add the 'Swagger UI' resource to your Syndicate deployment resources file.

syndicate generate swagger_ui --name task11_api_ui --path_to_spec path/to/oas_v3.json --target_bucket api-ui-hoster

Step 10: Build and Deploy

    Build the Syndicate Bundle with the following command and deploy new resources to the AWS Account:

syndicate build

syndicate deploy -resources api-ui-hoster -resources task11_api_ui

Step 11: Test Application

    Use an API client (Postman, Insomnia) to test each API resource, including signup, signin, fetching tables, fetching a specific table, making reservations, and fetching reservations.

Step 12: Access Swagger UI

    Find the Bucket website endpoint in aws-syndicate deployment logs or by navigating to the S3 Service in the AWS Management Console.
    Select the bucket specified for Swagger UI hosting.
    Navigate to Properties.
    Find the Static website hosting pane (located at the bottom of the page).
    Verify API Documentation:
    - Check if every API Endpoint (resources & methods) is carefully described.
    - Ensure that request & response models, authentication, and possible errors are documented accurately.




syndicate generate swagger_ui --name task11_api_ui --path_to_spec export/q3vn5ox60i_oas_v3.json --target_bucket api-ui-hoster