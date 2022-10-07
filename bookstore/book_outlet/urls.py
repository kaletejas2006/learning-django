from django.urls import path

from book_outlet import views

urlpatterns: list = [
    path("", views.index_page, name="index"),
    path("<int:id_val>", views.book_details, name="book-details")
]
