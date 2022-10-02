from typing import Optional, Union

from django.core.handlers.wsgi import WSGIRequest
from django.http import (
    HttpResponse,
    HttpResponseNotFound,
    HttpResponseRedirect,
    Http404,
)
from django.shortcuts import render
from django.urls import reverse

# Create your views here.

monthly_challenges: dict = {
    "february": "Drink at least 2 litres of water every day!",
    "march": "Practice Django for at least 20 minutes every day!",
    "april": None,
}


def hello_django(req: WSGIRequest) -> HttpResponse:
    """
    Hello world program from Django. Any Django view function always
    gets an input of type `WSGIRequest`.
    """
    return HttpResponse(f"Hello Django from {req.path}!")


def january(req: Optional[WSGIRequest]) -> HttpResponse:
    """Define a challenge for January."""
    return HttpResponse("Eat no meat for the entire month!")


def get_supported_months() -> list:
    return list(monthly_challenges.keys())


def monthly_challenge_numeric(
    req: Optional[WSGIRequest], month: int
) -> Union[HttpResponseRedirect, HttpResponseNotFound]:
    supported_months: list = get_supported_months()

    if not (2 <= month <= 3):
        return HttpResponseNotFound(
            "<h3>This month is not yet supported with numeric index!</h3>"
        )

    redirect_month: str = supported_months[month - 2]
    return HttpResponseRedirect(reverse("month-name", args=[redirect_month]))


def monthly_challenge(
    req: Optional[WSGIRequest], month: str
) -> Union[HttpResponse, Http404]:
    """Define month-wise challenges."""
    try:
        selected_challenge: str = monthly_challenges[month]
        return render(
            req,
            "challenges/challenge.html",
            {"month": month, "text": selected_challenge},
        )
    except KeyError:
        raise Http404()


def index_page(req: Optional[WSGIRequest]) -> HttpResponse:
    """Index page with links to February and March challenges."""
    supported_months: list = get_supported_months()

    response: str = render(req, "challenges/index.html", {"months": supported_months})

    return HttpResponse(response)
