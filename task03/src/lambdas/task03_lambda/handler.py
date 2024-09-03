from commons.log_helper import get_logger
from commons.abstract_lambda import AbstractLambda
import json

_LOG = get_logger('Task03Lambda-handler')


class Task03Lambda(AbstractLambda):

    def validate_request(self, event) -> dict:
        pass
        
    def handle_request(self, event, context):
        """
        Explain incoming event here
        """
        _LOG.info(event)
        path = event.get('rawPath', '')
        method = event.get('requestContext', {}).get('http', {}).get('method', '')
        _LOG.info(f'path: {path}')
        _LOG.info(f'method: {method}')

        if path == '/hello' and method == 'GET':
            response = {
                "statusCode": 200,
                "headers": {
                    "Content-Type": "application/json"
                },
                "body": json.dumps({
                    "statusCode": 200,
                    "message": "Hello from Lambda"})
            }
            _LOG.info('response:')
            _LOG.info(response)
            return response
    

HANDLER = Task03Lambda()


def lambda_handler(event, context):
    return HANDLER.lambda_handler(event=event, context=context)
