from django.test import TestCase

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
