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

        for record in event['Records']:
            # Check if the event is an INSERT or MODIFY
            if record['eventName'] == 'INSERT':
                self.handle_insert(record['dynamodb'])
            elif record['eventName'] == 'MODIFY':
                self.handle_modify(record['dynamodb'])

    def handle_insert(self, dynamodb_record):
        # Extract the new item from the event
        _LOG.info('inside handle_insert method')
        new_image = dynamodb_record['NewImage']

        dynamodb = boto3.resource('dynamodb')
        audit_table = dynamodb.Table(os.environ.get('table_name', "Audit"))

        # Create a new audit entry for the inserted itemconfiguration_table = dynamodb.Table('Configuration')
        audit_item = {
            'id': str(uuid.uuid4()),
            'itemKey': new_image['key']['S'],
            'modificationTime': datetime.utcnow().isoformat(),
            'newValue': {
                'key': new_image['key']['S'],
                'value': int(new_image['value']['N'])  # Assuming the value is a number
            }
        }

        # Save the audit entry to the Audit table
        resp = audit_table.put_item(Item=audit_item)
        _LOG.info(resp)


    def handle_modify(self, dynamodb_record):
        # Extract the old and new images from the event
        _LOG.info('inside handle_modify method')

        old_image = dynamodb_record['OldImage']
        new_image = dynamodb_record['NewImage']

        dynamodb = boto3.resource('dynamodb')
        audit_table = dynamodb.Table(os.environ.get('table_name', "Audit"))

        # Check for changes and track updated attributes
        if old_image['value']['N'] != new_image['value']['N']:
            audit_item = {
                'id': str(uuid.uuid4()),
                'itemKey': new_image['key']['S'],
                'modificationTime': datetime.utcnow().isoformat(),
                'updatedAttribute': 'value',
                'oldValue': int(old_image['value']['N']),
                'newValue': int(new_image['value']['N'])
            }

            # Save the audit entry to the Audit table
            resp = audit_table.put_item(Item=audit_item)
            _LOG.info(resp)



HANDLER = AuditProducer()


def lambda_handler(event, context):
    return HANDLER.lambda_handler(event=event, context=context)
