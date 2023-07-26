from django.test import TestCase
from django.urls import reverse
from .models import Author, Genre, Book

class BookCRUDTests(TestCase):

    def setUp(self):
        self.author1 = Author.objects.create(name='Author 1')
        self.author2 = Author.objects.create(name='Author 2')
        self.author3 = Author.objects.create(name='Author 3')
        self.genre1 = Genre.objects.create(name='Genre 1')
        self.genre2 = Genre.objects.create(name='Genre 2')
        self.genre3 = Genre.objects.create(name='Genre 3')
        self.book1 = Book.objects.create(title='Book 1', pages=200, published_by='Publisher 1', quote='Quote 1')
        self.book2 = Book.objects.create(title='Book 2', pages=250, published_by='Publisher 2', quote='Quote 2')
        self.book3 = Book.objects.create(title='Book 3', pages=300, published_by='Publisher 3', quote='Quote 3')
        self.book4 = Book.objects.create(title='Book 4', pages=350, published_by='Publisher 4', quote='Quote 4')
        self.book1.authors.add(self.author1, self.author2)
        self.book1.genres.add(self.genre1)
        self.book2.authors.add(self.author2)
        self.book2.genres.add(self.genre1, self.genre2)
        self.book3.authors.add(self.author3)
        self.book3.genres.add(self.genre1, self.genre3)
        self.book4.authors.add(self.author1, self.author3)
        self.book4.genres.add(self.genre1, self.genre2, self.genre3)


    def test_book_list_view(self):
        response = self.client.get(reverse('book_list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(set(response.context['books']), set([self.book1, self.book2, self.book3, self.book4]))

    def test_book_detail_view(self):
        response = self.client.get(reverse('book_detail', args=[self.book1.id]))
        self.assertEqual(response.context['book'], self.book1)

    def test_book_create_view(self):
        data = {
            'title': 'New Book',
            'pages': 300,
            'published_by': 'Publisher 3',
            'quote': 'Quote 3',
            'authors': [self.author1.pk, self.author2.pk],
            'genres': [self.genre1.pk, self.genre2.pk],
        }
        response = self.client.post(reverse('book_create'), data)
        self.assertTrue(Book.objects.filter(title='New Book').exists())

    def test_book_update_view(self):
        data = {
            'title': 'Updated title',
            'pages': 220,
            'published_by': 'Updated Publisher',
            'quote': 'Updated Quote',
            'authors': [self.author2.pk],
            'genres': [self.genre2.pk],
        }
        response = self.client.post(reverse('book_update', args=[self.book1.pk]), data)

        # Refresh the book instance from the database
        self.book1.refresh_from_db()

        # Compare the updated attributes of the book
        self.assertEqual(self.book1.title, 'Updated title')
        self.assertEqual(self.book1.pages, 220)
        self.assertEqual(self.book1.published_by, 'Updated Publisher')
        self.assertEqual(self.book1.quote, 'Updated Quote')

        # Compare the authors and genres using their primary keys
        self.assertListEqual(list(self.book1.authors.values_list('name', flat=True)), [self.author2.name])
        self.assertListEqual(list(self.book1.genres.values_list('name', flat=True)), [self.genre2.name])

    def test_book_delete_view(self):
        response = self.client.post(reverse('book_delete', args=[self.book2.id]))
        self.assertEqual(response.status_code, 302)  # Should redirect after successful delete
        self.assertFalse(Book.objects.filter(id=self.book2.id).exists())

    def test_search_books_by_title(self):
        response = self.client.post(reverse('search'), 
                                    {'search_category': 'Titles',
                                     'search_mode': 'contains_all',
                                     'raw_input': 'Book 1 ,  Book 2'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(set(response.context['books']), set([]))

        response = self.client.post(reverse('search'), 
                                    {'search_category': 'Titles',
                                     'search_mode': 'contains_any',
                                     'raw_input': 'Book 1 ,  Book 2'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(set(response.context['books']), set([self.book1, self.book2]))

    def test_search_books_by_author(self):
        response = self.client.post(reverse('search'), 
                                    {'search_category': 'Authors',
                                     'search_mode': 'contains_all',
                                     'raw_input': '  Author 1 ,  Author 2 '})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(set(response.context['books']), set([self.book1]))

        response = self.client.post(reverse('search'), 
                                    {'search_category': 'Authors',
                                     'search_mode': 'contains_any',
                                     'raw_input': '  Author 2 ,  Author 3 '})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(set(response.context['books']), set([self.book1, self.book2, self.book3, self.book4]))

    def test_search_books_by_genre(self):
        response = self.client.post(reverse('search'), 
                                    {'search_category': 'Genres',
                                     'search_mode': 'contains_all',
                                     'raw_input': '  Genre 1 ,  Genre 3 '})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(set(response.context['books']), set([self.book3, self.book4]))

        response = self.client.post(reverse('search'), 
                                    {'search_category': 'Genres',
                                     'search_mode': 'contains_any',
                                     'raw_input': '  Genre 2 ,  Genre 3 '})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(set(response.context['books']), set([self.book2, self.book3, self.book4]))