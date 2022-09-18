from unittest.mock import patch

from django.contrib.messages import get_messages
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.test import TestCase

from challenges import views


# Create your tests here.
class TestBasics(TestCase):
    @patch("django.core.handlers.wsgi.WSGIRequest")
    def test_hello_django(self, mock_wsgirequest):
        """
        Test the hello world function for Django. Creating a simple WSGIRequest
        object is an involved process which is unknown to Django beginners as
        we do not even understand what WSGI stands for. Hence, we have mocked
        this class.
        """
        req: WSGIRequest = mock_wsgirequest()
        req.path = "/challenges/hello"
        res: HttpResponse = views.hello_django(req)
        assert res.content.decode("utf-8") == f"Hello Django from {req.path}!"

    def test_january(self):
        """Test for the right message from January URL."""
        res: HttpResponse = views.january(None)
        assert res.content.decode("utf-8") == "Eat no meat for the entire month!"

    def test_monthly_challenge(self):
        """
        Test for the right messages for February and March URL. In case any
        other month is provided, a message saying that the month is not
        supported is shown.
        """
        res: HttpResponse = views.monthly_challenge(req=None, month="february")
        assert res.content.decode("utf-8") == "Drink at least 2 litres of water every day!"

        res: HttpResponse = views.monthly_challenge(req=None, month="march")
        assert res.content.decode("utf-8") == "Practice Django for at least 20 minutes every day!"

        res: HttpResponse = views.monthly_challenge(req=None, month="april")
        assert res.content.decode("utf-8") == "This month is not yet supported!"

    def test_monthly_challenge_numeric(self):
        """
        Test to check that index inputs for February and March are redirected
        to the right URL/function and unsupported inputs are notified likewise.
        """
        res: HttpResponse = views.monthly_challenge_numeric(req=None, month=2)
        self.assertRedirects(
            response=res,
            expected_url="/challenges/february",
            status_code=302,
            target_status_code=200,
            fetch_redirect_response=False
        )

        res: HttpResponse = views.monthly_challenge_numeric(req=None, month=3)
        self.assertRedirects(
            response=res,
            expected_url="/challenges/march",
            status_code=302,
            target_status_code=200,
            fetch_redirect_response=False
        )

        res: HttpResponse = views.monthly_challenge_numeric(req=None, month=1)
        assert res.content.decode("utf-8") == "This month is not yet supported with numeric index!"

