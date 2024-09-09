from datetime import datetime

from commons.log_helper import get_logger
from commons.abstract_lambda import AbstractLambda

import json
import os
import uuid
import boto3

_LOG = get_logger('ApiHandler-handler')


class ApiHandler(AbstractLambda):

    def validate_request(self, event) -> dict:
        pass

    def handle_request(self, event, context):
        """
        Explain incoming event here
        """
        _LOG.info(event)
        dt = datetime.now()
        # Convert to ISO 8601 format with milliseconds (e.g., 2024-01-01T00:00:00.000Z)
        iso_format_with_ms = dt.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'

        obj = {
            'id': uuid.uuid1(),
            "principalId": 10,
            "createdAt": iso_format_with_ms,
            'body': event
        }
        _LOG.info(obj)
        dynamodb = boto3.resource('dynamodb', region_name=os.environ.get('region', "eu-central-1"))
        table_name = os.environ.get('table_name', "Events")

        table = dynamodb.Table(table_name)

        response = table.put_item(Item=obj)

        return {
            "statusCode": 201,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps(response, indent=4)
        }


HANDLER = ApiHandler()


def lambda_handler(event, context):
    return HANDLER.lambda_handler(event=event, context=context)
