from commons.log_helper import get_logger
from commons.abstract_lambda import AbstractLambda
from meteo_api.weather_forecast import WeatherForecast

_LOG = get_logger('ApiHandler-handler')


class ApiHandler(AbstractLambda):

    def validate_request(self, event) -> dict:
        pass

    def handle_request(self, event, context):
        """
        Explain incoming event here
        """
        response = {
            'headers': {
                "Content-Type": "application/json"
            }
        }
        try:
            weather_api = WeatherForecast()
            api_resp = weather_api.get_weather()
            response['statusCode'] = 200
            response['body'] = api_resp
        except Exception as e:
            _LOG.error(e)
            response['statusCode'] = 500
            response['body'] = str(e)


HANDLER = ApiHandler()


def lambda_handler(event, context):
    return HANDLER.lambda_handler(event=event, context=context)
