from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(default="Not Provided", max_length=50)
    rating = models.IntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5)
        ]
    )
    is_nyt_bestseller = models.BooleanField(default=False)

    def __str__(self):
        print_title: str = f"{self.title} by {self.author}"
        if self.is_nyt_bestseller:
            print_title = f"{print_title} [NY Times Bestseller]"

        return print_title
