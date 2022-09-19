from typing import Optional, Union

from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.urls import reverse

# Create your views here.

monthly_challenges: dict = {
    "february": "Drink at least 2 litres of water every day!",
    "march": "Practice Django for at least 20 minutes every day!"
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
        req: Optional[WSGIRequest],
        month: int
) -> Union[HttpResponseRedirect, HttpResponseNotFound]:
    supported_months: list = get_supported_months()

    if not (2 <= month <= 3):
        return HttpResponseNotFound("<h3>This month is not yet supported with numeric index!</h3>")

    redirect_month: str = supported_months[month - 2]
    return HttpResponseRedirect(reverse("month-name", args=[redirect_month]))


def monthly_challenge(
        req: Optional[WSGIRequest],
        month: str
) -> Union[HttpResponse, HttpResponseNotFound]:
    """Define month-wise challenges."""
    try:
        selected_challenge: str = monthly_challenges[month]
        response: str = f"<h3>{selected_challenge}</h3>"
    except KeyError:
        return HttpResponseNotFound("<h3>This month is not yet supported!</h3>")

    return HttpResponse(response)


def index_page(req: Optional[WSGIRequest]) -> HttpResponse:
    """Index page with links to February and March challenges."""
    supported_months: list = get_supported_months()

    month_list: str = ""
    month: str
    for month in supported_months:
        month_url: str = reverse("month-name", args=[month])
        month_list_item: str = (f'<li><a href="{month_url}">'
                                f'{month.capitalize()}</a></li>')
        month_list += month_list_item

    response: str = f"<ul>{month_list}</ul>"

    return HttpResponse(response)
