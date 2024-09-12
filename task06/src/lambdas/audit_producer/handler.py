from commons.log_helper import get_logger
from commons.abstract_lambda import AbstractLambda

_LOG = get_logger('AuditProducer-handler')

import json
import os
import uuid
import boto3
from datetime import datetime


class AuditProducer(AbstractLambda):

    def validate_request(self, event) -> dict:
        pass

    def handle_request(self, event, context):
        """
        Explain incoming event here
        """
        _LOG.info("Event:\n%s", str(event))
        req_obj = {}

        if event:
            dynamodb_obj = event.get('Records', [])
            dynamodb_obj = dynamodb_obj[0].get('dynamodb', {})
            mod_time = dynamodb_obj.get('ApproximateCreationDateTime', None)
            if not mod_time:
                dt = datetime.now()
                mod_time = dt.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
            else:
                mod_time = datetime.fromtimestamp(mod_time).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'

            key_name = dynamodb_obj.get('NewImage', {}).get('key', {}).get('S', 'CACHE_TTL_SEC')
            value = dynamodb_obj.get('NewImage', {}).get('value', {})

            if not value:
                new_val = dynamodb_obj.get('NewImage', {}).get('key', {})
                if new_val and new_val.get('S', False):
                    value = new_val.get('S')
                else:
                    value = value.get('N', 888)
            else:
                value = dynamodb_obj.get('NewImage', {}).get('key', {}).get('S', 777)

            req_obj = {
                "id": str(uuid.uuid1()),
                "itemKey": 'CACHE_TTL_SEC',
                "modificationTime": mod_time,
                "newValue": {
                    "key": 'CACHE_TTL_SEC',
                    "value": value
                },
            }

        dt = datetime.now()
        # Convert to ISO 8601 format with milliseconds (e.g., 2024-01-01T00:00:00.000Z)
        iso_format_with_ms = dt.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'

        obj = {
            'id': str(uuid.uuid1()),
            # "principalId": event.get('principalId', 1),
            "createdAt": iso_format_with_ms,
            'body': req_obj
        }
        _LOG.info('put_item request object')
        _LOG.info(obj)

        dynamodb = boto3.resource('dynamodb', region_name=os.environ.get('region', "eu-central-1"))
        table_name = os.environ.get('table_name', "Audit")

        try:
            config_table_obj = dynamodb.Table(os.environ.get('config_table', "Configuration"))
            config_table = config_table_obj.get_item(Key={"key": {'S': '1005'}})
            _LOG.info('config table get_item response')
            _LOG.info(config_table)
        except Exception as e:
            _LOG.error('error occurred during get_item call')
            _LOG.error(str(e))

        table = dynamodb.Table(table_name)
        response = table.put_item(Item=obj)
        _LOG.info('put item response\n')
        _LOG.info(response)

        return {
            "statusCode": 201,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps(response, indent=4)
        }


HANDLER = AuditProducer()


def lambda_handler(event, context):
    return HANDLER.lambda_handler(event=event, context=context)
