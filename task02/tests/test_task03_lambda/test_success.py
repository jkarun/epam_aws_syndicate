from tests.test_task03_lambda import Task03LambdaLambdaTestCase


class TestSuccess(Task03LambdaLambdaTestCase):

    def test_success(self):
        self.assertEqual(self.HANDLER.handle_request(dict(), dict()), 200)

