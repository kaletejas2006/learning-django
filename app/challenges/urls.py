from django.urls import path

from challenges import views

urlpatterns: list = [
    path("hello", views.hello_django),
    path("january", views.january),
    path("<int:month>", views.monthly_challenge_numeric),
    path("<str:month>", views.monthly_challenge)
]