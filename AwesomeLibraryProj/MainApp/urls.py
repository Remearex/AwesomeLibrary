from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page, name='home_page'),
    path('books/', views.book_list, name='book_list'),
    path('books/create/', views.book_create, name='book_create'),
    path('books/<int:book_id>/', views.book_detail, name='book_detail'),
    path('books/<int:book_id>/update/', views.book_update, name='book_update'),
    path('books/<int:book_id>/delete/', views.book_delete, name='book_delete'),
    path('author_list', views.author_list, name='author_list'),
    path('author_create', views.author_create, name='author_create'),
    path('author_delete/<str:author_name>/', views.author_delete, name='author_delete'),
    path('genre_list', views.genre_list, name='genre_list'),
    path('genre_create', views.genre_create, name='genre_create'),
    path('genre_delete/<str:genre_name>/', views.genre_delete, name='genre_delete'),
    path('search', views.search, name='search'),
    path('search/books/', views.search_books_by_title, name='search_books_by_title'),
    path('search/books/by_author/', views.search_books_by_author, name='search_books_by_author'),
    path('search/books/by_genre/', views.search_books_by_genre, name='search_books_by_genre'),
]