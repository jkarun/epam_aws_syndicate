from commons.log_helper import get_logger
from commons.abstract_lambda import AbstractLambda
import requests

_LOG = get_logger('ApiHandler-handler')


class ApiHandler(AbstractLambda):

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
        except Exception as e:
            _LOG.error(e)
            response['statusCode'] = 500
            response['body'] = str(e)

        return response


HANDLER = ApiHandler()


def lambda_handler(event, context):
    return HANDLER.lambda_handler(event=event, context=context)
