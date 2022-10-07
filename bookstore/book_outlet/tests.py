from django.http import HttpResponse, Http404
from django.test import TestCase

from book_outlet import views
from book_outlet.models import Book


# Create your tests here.
class TestBook(TestCase):
    def setUp(self) -> None:
        self.sample_book = Book(
            title="Tell Me Lies",
            author="Carola Lovering",
            rating=4,
            is_nyt_bestseller=False
        )
        self.sample_book.save()

    def test_constructor(self):
        """Test the constructor."""
        self.assertEqual(Book.objects.all()[0].title, self.sample_book.title)
        self.assertEqual(Book.objects.all()[0].author, self.sample_book.author)
        self.assertEqual(Book.objects.all()[0].rating, self.sample_book.rating)
        self.assertEqual(
            Book.objects.all()[0].is_nyt_bestseller,
            self.sample_book.is_nyt_bestseller
        )

    def test_str_repr(self):
        expected: str = "Tell Me Lies by Carola Lovering"
        self.assertEqual(str(self.sample_book), expected)

    def tearDown(self) -> None:
        self.sample_book.delete()


class TestView(TestCase):
    def setUp(self) -> None:
        self.book_1 = Book(
            title="Tell Me Lies",
            author="Carola Lovering",
            rating=4,
            is_nyt_bestseller=False
        )
        self.book_1.save()

        self.book_2 = Book(
            title="Mystic River",
            author="Dennis Lehane",
            rating=3,
            is_nyt_bestseller=True
        )
        self.book_2.save()

    def test_index_page(self):
        """
        Test to check that the index page contains links to all books
        in the database.
        """
        res: HttpResponse = views.index_page(req=None)
        self.assertContains(
            response=res,
            text=f'<a href="">{self.book_1.title}</a>',
            html=True
        )
        self.assertContains(
            response=res,
            text=f'<a href="">{self.book_2.title}</a>',
            html=True
        )

    def test_book_details(self):
        """
        Test to check that all the relevant book details are shown on page.
        """
        res: HttpResponse = views.book_details(req=None, id_val=1)
        self.assertContains(
            response=res,
            text=f'<h1>{self.book_1.title}</h1>',
            html=True
        )
        self.assertContains(
            response=res,
            text=f'<h2>{self.book_1.author}</h2>',
            html=True
        )
        self.assertContains(
            response=res,
            text=(f'<p>The book has a rating {self.book_1.rating} but '
                  f'is not a New York Times bestseller.</p>'),
            html=True
        )

        res: HttpResponse = views.book_details(req=None, id_val=2)
        self.assertContains(
            response=res,
            text=(f'<p>The book has a rating {self.book_2.rating} and '
                  f'is a New York Times bestseller.</p>'),
            html=True
        )

        with self.assertRaises(Http404):
            _ = views.book_details(req=None, id_val=3)

    def tearDown(self) -> None:
        self.book_1.delete()
        self.book_2.delete()
