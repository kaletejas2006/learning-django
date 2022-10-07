from unittest.mock import patch

from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse, Http404
from django.test import TestCase
from django.urls import reverse

from challenges import views


# Create your tests here.
class TestChallenges(TestCase):
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
        self.assertContains(
            response=res, text="<title>February's Challenge</title>", html=True
        )
        self.assertContains(
            response=res, text="<h1>Challenge for the month of February</h1>", html=True
        )
        self.assertContains(
            response=res,
            text="<h3>Drink at least 2 litres of water every day!</h3>",
            html=True,
        )

        res: HttpResponse = views.monthly_challenge(req=None, month="march")
        self.assertContains(
            response=res, text="<title>March's Challenge</title>", html=True
        )
        self.assertContains(
            response=res, text="<h1>Challenge for the month of March</h1>", html=True
        )
        self.assertContains(
            response=res,
            text="<h3>Practice Django for at least 20 minutes every day!</h3>",
            html=True,
        )

        res: HttpResponse = views.monthly_challenge(req=None, month="april")
        self.assertContains(
            response=res, text="<title>April's Challenge</title>", html=True
        )
        self.assertContains(
            response=res, text="<h1>Challenge for the month of April</h1>", html=True
        )
        self.assertContains(
            response=res, text="<h3>No challenge for this month. Enjoy!</h3>", html=True
        )

        with self.assertRaises(Http404):
            _ = views.monthly_challenge(req=None, month="may")

    def test_monthly_challenge_numeric(self):
        """
        Test to check that index inputs for February and March are redirected
        to the right URL/function and unsupported inputs are notified likewise.
        """
        res: HttpResponse = views.monthly_challenge_numeric(req=None, month=2)
        self.assertRedirects(
            response=res,
            expected_url=reverse("month-name", args=["february"]),
            status_code=302,
            target_status_code=200,
            fetch_redirect_response=False,
        )

        res: HttpResponse = views.monthly_challenge_numeric(req=None, month=3)
        self.assertRedirects(
            response=res,
            expected_url=reverse("month-name", args=["march"]),
            status_code=302,
            target_status_code=200,
            fetch_redirect_response=False,
        )

        res: HttpResponse = views.monthly_challenge_numeric(req=None, month=1)
        assert (
            res.content.decode("utf-8")
            == "<h3>This month is not yet supported with numeric index!</h3>"
        )

    def test_index_page(self):
        """
        Test that the index page of challenges contains links
        to the month of February and March.
        """
        res: HttpResponse = views.index_page(req=None)
        index_url: str = reverse("index")
        february_url: str = reverse("month-name", args=["february"])
        march_url: str = reverse("month-name", args=["march"])
        self.assertContains(
            response=res,
            text=f'<header><nav><a href="{index_url}">All Challenges</a></nav></header>',
            html=True,
        )
        self.assertContains(
            response=res, text="<title>All Challenges</title>", html=True
        )
        self.assertContains(
            response=res,
            text=f'<li><a href="{february_url}">' f"February</a></li>",
            html=True,
        )
        self.assertContains(
            response=res,
            text=f'<li><a href="{march_url}">' f"March</a></li>",
            html=True,
        )
