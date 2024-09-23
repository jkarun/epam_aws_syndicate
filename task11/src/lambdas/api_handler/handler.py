from commons.log_helper import get_logger
from commons.abstract_lambda import AbstractLambda

_LOG = get_logger('ApiHandler-handler')

import boto3
import json
import uuid
import os
import random
from decimal import Decimal


# Custom encoder for Decimal objects
class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)  # Convert Decimal to float
        return super(DecimalEncoder, self).default(obj)


class ApiHandler(AbstractLambda):

    def __init__(self):
        self.cognito = boto3.client('cognito-idp')
        self.cognito_client = self.cognito
        self.dynamodb = boto3.resource('dynamodb')
        self.user_pool_id = os.getenv('cup_id')
        self.client_id = os.getenv('cup_client_id')
        self.tables_table = self.dynamodb.Table(os.environ.get('tables', "test1"))
        self.reservations_table = self.dynamodb.Table(os.environ.get('reservations', "test2"))

    def is_valid_email(self, email):
        # Regex pattern for validating email
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        return re.match(email_regex, email)

    def is_valid_password(self, password):
        # Password must contain alphanumeric characters and at least one of $%^*, minimum length 12
        password_regex = r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[$%^*])[A-Za-z\d$%^*]{12,}$'
        return re.match(password_regex, password)

    def signup(self, event):
        body = json.loads(event['body'])
        first_name = body.get('firstName')
        last_name = body.get('lastName')
        email = body.get('email')
        password = body.get('password')

        # Validate email and password
        if not self.is_valid_email(email):
            return {
                'statusCode': 400,
                'body': json.dumps({'message': 'Invalid email format'}),
                "isBase64Encoded": True
            }

        if not self.is_valid_password(password):
            return {
                'statusCode': 400,
                'body': json.dumps({'message': 'Password does not meet the required criteria'}),
                "isBase64Encoded": True
            }

        try:
            response = self.cognito_client.sign_up(
                ClientId=self.client_id,
                Username=email,
                Password=password,
                UserAttributes=[
                    {
                        'Name': 'email',
                        'Value': email
                    },
                    {
                        'Name': 'given_name',
                        'Value': first_name
                    },
                    {
                        'Name': 'family_name',
                        'Value': last_name
                    },
                ],
            )
            _LOG.info(f'signup api response:\n{str(response)}')

            if response and response['UserConfirmed'] == False:
                # Automatically confirm the user after sign-up
                confirm_resp = self.cognito_client.admin_confirm_sign_up(
                    UserPoolId=self.user_pool_id,
                    Username=email
                )
                _LOG.info(f'confirm api response:\n{str(confirm_resp)}')
                response['UserConfirmed'] = True

            return {
                'statusCode': 200,
                'body': json.dumps({'message': 'Sign-up process is successful', 'body': response}),
                "isBase64Encoded": True
            }

        except Exception as e:
            return {
                'statusCode': 400,
                'body': json.dumps({'message': 'Bad request', 'error': str(e)}),
                "isBase64Encoded": True
            }

    def signin(self, event):
        body = json.loads(event['body'])
        email = body.get('email')
        password = body.get('password')

        try:
            auth_params = {
                'USERNAME': email,
                'PASSWORD': password
            }
            # Step 1: Initiate the authentication
            response = self.cognito.admin_initiate_auth(
                UserPoolId=os.environ.get('cup_id'),
                ClientId=os.environ.get('cup_client_id'),
                AuthFlow='ADMIN_NO_SRP_AUTH', AuthParameters=auth_params)

            _LOG.info(f'authentication response:\n{str(response)}')

            new_password = None
            # Step 2: Check if a challenge is triggered
            if 'ChallengeName' in response and response['ChallengeName'] == 'NEW_PASSWORD_REQUIRED':
                _LOG.info('setting new password')
                # User needs to set a new password
                new_password = password + str(random.randrange(1, 100))
                if password:
                    # Step 3: Respond to the new password required challenge
                    challenge_response = self.cognito.respond_to_auth_challenge(
                        ClientId=self.client_id,
                        ChallengeName='NEW_PASSWORD_REQUIRED',
                        Session=response['Session'],
                        ChallengeResponses={
                            'USERNAME': email,
                            'NEW_PASSWORD': new_password
                        }
                    )
                    _LOG.info(f'challenge_response:\n{str(challenge_response)}')
                    # Return the access token after successfully setting a new password
                    return challenge_response['AuthenticationResult']['AccessToken']
                else:
                    return "New password is required. Please provide a new password."

            access_token = response['AuthenticationResult']['IdToken']

            return {
                'statusCode': 200,
                'body': json.dumps({'accessToken': access_token, 'new_password': new_password}),
                "isBase64Encoded": True
            }
        except Exception as e:
            _LOG.error('error in signin...')
            _LOG.error(e)
            return {
                'statusCode': 400,
                'body': json.dumps({'message': 'Bad request', 'error': str(e)}),
                "isBase64Encoded": True
            }

    def get_tables(self, event):
        try:
            response = self.tables_table.scan()
            _LOG.info(f'scan table resposne:\n{response}')
            return {
                'statusCode': 200,
                'body': json.dumps({'tables': response['Items']}, cls=DecimalEncoder)
            }
        except Exception as e:
            _LOG.error('error in scan tables....')
            _LOG.error(e)
            return {
                'statusCode': 400,
                'body': json.dumps({'message': 'Bad request', 'error': str(e)})
            }

    def create_table(self, event):
        body = json.loads(event['body'])
        id = body.get('id')
        number = body.get('number')
        places = body.get('places')
        is_vip = body.get('isVip')
        min_order = body.get('minOrder')

        try:
            _LOG.info('create table start...')
            resp = self.tables_table.put_item(
                Item={
                    'id': id,
                    'number': number,
                    'places': places,
                    'isVip': is_vip,
                    'minOrder': min_order
                }
            )

            _LOG.info(f'create table response"\n{resp}')
            return {
                'statusCode': 200,
                'body': json.dumps({'id': id})
            }
        except Exception as e:
            _LOG.error('error in create table')
            _LOG.error(e)
            return {
                'statusCode': 400,
                'body': json.dumps({'message': 'Bad request', 'error': str(e)})
            }

    def get_table_by_id(self, table_id):
        try:
            _LOG.info(f'get_table_by_id: {table_id} type of {type(table_id)}')
            response = self.tables_table.get_item(
                Key={
                    'id': int(table_id)
                }
            )
            _LOG.info(f'get table by id response:\n{response}')
            if 'Item' in response:
                return {
                    'statusCode': 200,
                    'body': json.dumps(response['Item'], cls=DecimalEncoder)
                }
            else:
                return {
                    'statusCode': 404,
                    'body': json.dumps({'message': 'Table not found'})
                }
        except Exception as e:
            _LOG.error(e)
            return {
                'statusCode': 400,
                'body': json.dumps({'message': 'Bad request', 'error': str(e)})
            }

    def create_reservation(self, event):
        body = json.loads(event['body'])
        table_number = body.get('tableNumber')
        client_name = body.get('clientName')
        phone_number = body.get('phoneNumber')
        date = body.get('date')
        slot_time_start = body.get('slotTimeStart')
        slot_time_end = body.get('slotTimeEnd')
        reservation_id = str(uuid.uuid4())

        try:
            # Step 1: Check if the table exists in the Tables table
            table_check_response = self.tables_table.scan(
                FilterExpression="#n = :table_number",
                ExpressionAttributeNames={"#n": "number"},  # Alias for reserved keyword 'number'
                ExpressionAttributeValues={":table_number": table_number}
            )

            if not table_check_response['Items']:
                return {
                    'statusCode': 400,
                    'body': json.dumps({
                        'message': f'Table with number {table_number} does not exist.'
                    })
                }

            # Step 2: Check for existing reservations on the same table and date
            existing_reservations = self.reservations_table.scan(
                FilterExpression="#tn = :table_number AND #d = :date",
                ExpressionAttributeNames={
                    "#tn": "tableNumber",  # Alias for 'tableNumber'
                    "#d": "date"  # Alias for 'date'
                },
                ExpressionAttributeValues={
                    ":table_number": table_number,
                    ":date": date
                }
            )

            # Step 3: Validate if the time slot overlaps with any existing reservations
            for reservation in existing_reservations['Items']:
                existing_start = reservation['slotTimeStart']
                existing_end = reservation['slotTimeEnd']

                if (slot_time_start < existing_end and slot_time_end > existing_start):
                    return {
                        'statusCode': 400,
                        'body': json.dumps({
                            'message': 'Time conflict: The table is already reserved for this time slot.'
                        })
                    }

            # Step 4: Create the reservation if no conflicts
            self.reservations_table.put_item(
                Item={
                    'id': reservation_id,
                    'tableNumber': table_number,
                    'clientName': client_name,
                    'phoneNumber': phone_number,
                    'date': date,
                    'slotTimeStart': slot_time_start,
                    'slotTimeEnd': slot_time_end
                }
            )
            return {
                'statusCode': 200,
                'body': json.dumps({'reservationId': reservation_id})
            }

        except Exception as e:
            return {
                'statusCode': 400,
                'body': json.dumps({'message': 'Bad request', 'error': str(e)})
            }

    def get_reservations(self, event):
        try:
            response = self.reservations_table.scan()
            _LOG.info(f'get_reservations response"\n{response}')
            return {
                'statusCode': 200,
                'body': json.dumps({'reservations': response['Items']}, cls=DecimalEncoder)
            }
        except Exception as e:
            _LOG.error('error in get reservation')
            _LOG.error(e)
            return {
                'statusCode': 400,
                'body': json.dumps({'message': 'Bad request', 'error': str(e)})
            }

    def validate_request(self, event) -> dict:
        pass

    def handle_request(self, event, context):
        """
        Explain incoming event here
        """
        _LOG.info(f'lambda input event:\n{str(event)}')
        route_key = f"{event['httpMethod']} {event['resource']}"
        response = {}

        if route_key == 'POST /signup':
            response = self.signup(event)
        elif route_key == 'POST /signin':
            response = self.signin(event)
        elif route_key == 'GET /tables':
            response = self.get_tables(event)
        elif route_key == 'POST /tables':
            response = self.create_table(event)
        elif route_key == 'GET /tables/{tableId}':
            table_id = event['pathParameters']['tableId']
            response = self.get_table_by_id(table_id)
        elif route_key == 'POST /reservations':
            response = self.create_reservation(event)
        elif route_key == 'GET /reservations':
            response = self.get_reservations(event)
        else:
            return {
                'statusCode': 400,
                'body': json.dumps({'message': 'Invalid route'}),
                'headers': {
                    "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Methods": "*",
                    "Accept-Version": "*",
                    'Content-Type': 'application/json'
                }
            }

        # Add CORS headers to the response
        if response and response.get('statusCode') == 200:
            response['headers'] = {
                "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "*",
                "Accept-Version": "*",
                'Content-Type': 'application/json'
            }
        else:
            # Ensure CORS headers are included even in non-200 responses
            response['headers'] = {
                "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "*",
                "Accept-Version": "*",
                'Content-Type': 'application/json'
            }
        return response


HANDLER = ApiHandler()


def lambda_handler(event, context):
    return HANDLER.lambda_handler(event=event, context=context)
