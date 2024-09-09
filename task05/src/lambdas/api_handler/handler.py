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
        obj = {
            'id': str(uuid.uuid1()),
            'event': str(event)
        }

        dynamodb = boto3.resource('dynamodb', region_name=os.environ.get('region'))
        table_name = os.environ.get('table_name')

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
