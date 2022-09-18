from typing import Optional

from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect


# Create your views here.

monthly_challenges: dict = {
    "february": "Drink at least 2 litres of water every day!",
    "march": "Practice Django for at least 20 minutes every day!"
}


def hello_django(req: WSGIRequest):
    """
    Hello world program from Django. Any Django view function always
    gets an input of type `WSGIRequest`.
    """
    return HttpResponse(f"Hello Django from {req.path}!")


def january(req: Optional[WSGIRequest]):
    """Define a challenge for January."""
    return HttpResponse("Eat no meat for the entire month!")


def monthly_challenge_numeric(req: Optional[WSGIRequest], month: int):
    supported_months: list = list(monthly_challenges.keys())

    if not (2 <= month <= 3):
        return HttpResponseNotFound("This month is not yet supported with numeric index!")

    redirect_month: str = supported_months[month - 2]
    return HttpResponseRedirect(f"/challenges/{redirect_month}")


def monthly_challenge(req: Optional[WSGIRequest], month: str):
    """Define month-wise challenges."""
    try:
        selected_challenge: str = monthly_challenges[month]
    except KeyError:
        return HttpResponseNotFound("This month is not yet supported!")

    return HttpResponse(selected_challenge)
