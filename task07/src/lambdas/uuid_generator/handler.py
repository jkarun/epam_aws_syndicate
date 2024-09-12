import os

from commons.log_helper import get_logger
from commons.abstract_lambda import AbstractLambda

_LOG = get_logger('UuidGenerator-handler')

import json
import uuid
import boto3
from datetime import datetime


class UuidGenerator(AbstractLambda):

    def validate_request(self, event) -> dict:
        pass

    def handle_request(self, event, context):
        """
        Explain incoming event here
        """
        uuids = [str(uuid.uuid4()) for _ in range(10)]

        # Get current time in ISO 8601 format
        timestamp = datetime.utcnow().strftime('%Y-%m-%dT00:00:00.000Z')

        # Create the file content
        file_content = {
            "ids": uuids
        }

        # Create a file name with the execution start time
        file_name = f"{timestamp}.json"

        # Initialize S3 client
        s3 = boto3.client('s3')
        bucket_name = os.environ.get('target_bucket', 'cmtr-134cb1e3-uuid-storage')
        # Upload the file to S3
        s3.put_object(
            Bucket=bucket_name,
            Key=file_name,
            Body=json.dumps(file_content),
            ContentType='application/json'
        )

        return {
            'statusCode': 200,
            'body': json.dumps(f"File {file_name} created successfully in {bucket_name}")
        }


HANDLER = UuidGenerator()


def lambda_handler(event, context):
    return HANDLER.lambda_handler(event=event, context=context)
