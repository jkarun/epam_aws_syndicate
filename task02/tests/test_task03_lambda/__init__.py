import unittest
import importlib
from tests import ImportFromSourceContext

with ImportFromSourceContext():
    LAMBDA_HANDLER = importlib.import_module('lambdas.task03_lambda.handler')


class Task03LambdaLambdaTestCase(unittest.TestCase):
    """Common setups for this lambda"""

    def setUp(self) -> None:
        self.HANDLER = LAMBDA_HANDLER.Task03Lambda()

