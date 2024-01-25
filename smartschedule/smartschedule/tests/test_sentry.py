from django.test import TestCase

class SentryTest(TestCase):

    def test_error_sent_to_sentry(self):
        with self.assertRaises(ZeroDivisionError):
            1 / 0
