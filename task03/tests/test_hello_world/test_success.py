from tests.test_hello_world import HelloWorldLambdaTestCase
import json

class TestSuccess(HelloWorldLambdaTestCase):

    def test_success(self):
        response = {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps({
                "statusCode": 200,
                "message": "Hello from Lambda"})
        }
        response = {
            "statusCode": 200,
            "message": "Hello from Lambda"
        }
        sample_lambda_event = {'version': '2.0', 'routeKey': '$default', 'rawPath': '/hello', 'rawQueryString': '',
                               'headers': {'x-real-ip': '103.98.209.92',
                                           'x-amzn-tls-cipher-suite': 'TLS_AES_128_GCM_SHA256',
                                           'x-amzn-tls-version': 'TLSv1.3',
                                           'x-amzn-trace-id': 'Root=1-66cdd736-4ffdfb2c17e919f029040f91',
                                           'x-forwarded-proto': 'https',
                                           'host': 'g5p2q4w6xfiqal5g2bmcfcfnxy0pvknc.lambda-url.eu-central-1.on.aws',
                                           'x-forwarded-port': '443', 'x-forwarded-for': '64.227.21.251',
                                           'accept-encoding': 'deflate, gzip', 'accept': '*/*',
                                           'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:129.0) Gecko/20100101 Firefox/129.0'},
                               'requestContext': {'accountId': 'anonymous', 'apiId': 'g5p2q4w6xfiqal5g2bmcfcfnxy0pvknc',
                                                  'domainName': 'g5p2q4w6xfiqal5g2bmcfcfnxy0pvknc.lambda-url.eu-central-1.on.aws',
                                                  'domainPrefix': 'g5p2q4w6xfiqal5g2bmcfcfnxy0pvknc',
                                                  'http': {'method': 'GET', 'path': '/hello', 'protocol': 'HTTP/1.1',
                                                           'sourceIp': '64.227.21.251',
                                                           'userAgent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:129.0) Gecko/20100101 Firefox/129.0'},
                                                  'requestId': 'c67d6060-6c61-47bb-b264-70162e49f38c',
                                                  'routeKey': '$default', 'stage': '$default',
                                                  'time': '27/Aug/2024:13:40:06 +0000', 'timeEpoch': 1724766006169},
                               'isBase64Encoded': False}
        self.assertEqual(self.HANDLER.handle_request(sample_lambda_event, dict()), response)

