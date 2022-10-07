from typing import Optional

from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

from book_outlet.models import Book


# Create your views here.
def index_page(req: Optional[WSGIRequest]) -> HttpResponse:
    """Renders the index page of our webpage."""
    books = Book.objects.all()
    return render(
        req,
        "book_outlet/index.html",
        {"books": books}
    )


def book_details(req: Optional[WSGIRequest], id_val: int) -> HttpResponse:
    """
    Renders the details of selected book.

    :param req: <TBD>
    :param id_val: Integer ID of the book whose details are to be displayed.
    :return:
    """
    # `pk` is a special argument that maps to the primary key defined
    # in our database.
    book: Optional[Book] = get_object_or_404(Book, pk=id_val)
    return render(
        req,
        "book_outlet/book_details.html",
        {"book": book}
    )
