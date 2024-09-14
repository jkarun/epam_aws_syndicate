from commons.log_helper import get_logger
from commons.abstract_lambda import AbstractLambda
from decimal import Decimal

import requests

_LOG = get_logger('Processor-handler')

import json
import os
import uuid
import boto3
from datetime import datetime


class Processor(AbstractLambda):

    def validate_request(self, event) -> dict:
        pass

    def handle_request(self, event, context):
        """
        Explain incoming event here
        """
        response = {
            'statusCode': 200,
            'headers': {
                "Content-Type": "application/json"
            },
            'body': {}
        }
        try:
            base_url = "https://api.open-meteo.com/v1/forecast"
            latitude = 52.52
            longitude = 13.41
            params = {
                'latitude': latitude,
                'longitude': longitude,
                'current_weather': 'true',
                'hourly': 'temperature_2m,relative_humidity_2m,wind_speed_10m'
            }
            api_response = requests.get(base_url, params=params)
            api_response.raise_for_status()  # Check for HTTP request errors
            data = api_response.json()
            response['body'] = data
            self.handle_insert(data)
        except Exception as e:
            _LOG.error(e)
            response['statusCode'] = 500
            response['body'] = str(e)
        return response

    def handle_insert(self, dynamodb_record):
        _LOG.info('inside handle_insert method')

        dynamodb = boto3.resource('dynamodb')
        db_table = dynamodb.Table(os.environ.get('table_name', "Weather"))

        db_item = {
            'id': str(uuid.uuid4()),
            'forecast': self.convert_float_to_decimal(dynamodb_record)
        }
        try:
            _LOG.info('performing insert...')
            resp = db_table.put_item(Item=db_item)
            _LOG.info(resp)
        except Exception as e:
            _LOG.error('error in db insert action')
            _LOG.error(e)

    def convert_float_to_decimal(self, data):
        """Recursively converts float values to Decimal."""
        if isinstance(data, list):
            return [self.convert_float_to_decimal(item) for item in data]
        elif isinstance(data, dict):
            return {k: self.convert_float_to_decimal(v) for k, v in data.items()}
        elif isinstance(data, float):
            return Decimal(str(data))
        return data


HANDLER = Processor()


def lambda_handler(event, context):
    return HANDLER.lambda_handler(event=event, context=context)
