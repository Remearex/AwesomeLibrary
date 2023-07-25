from django.shortcuts import render, get_object_or_404, redirect
from .models import Book, Author, Genre
from .forms import BookForm

# home page

def home_page(request):
    return render(request, 'home_page.html')

# CRUD operations on books

def book_list(request):
    books = Book.objects.all()
    return render(request, 'book_list.html', {'books': books})

def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    return render(request, 'book_detail.html', {'book': book})

def book_create(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm()
    return render(request, 'book_form.html', {'form': form})

def book_update(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm(instance=book)
    return render(request, 'book_form.html', {'form': form})

def book_delete(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        book.delete()
        return redirect('book_list')
    return render(request, 'book_confirm_delete.html', {'book': book})

# author create and delete

def author_list(request):
    authors = Author.objects.all()
    return render(request, 'author_list.html', {'authors': authors})

def author_create(request):
    if request.method == 'POST':
        author_name_ = request.POST.get('author_name')
        author = Author()
        author.name = author_name_
        author.save()
        return redirect('author_list')
    else:
        return render(request, 'author_create.html')
    
def author_delete(request, author_id):
    author = get_object_or_404(Author, id=author_id)
    # no need to check the request type since we only send post requests to this endpoint
    author.delete()
    return redirect('author_list')
    
# genre create and delete

def genre_list(request):
    genres = Genre.objects.all()
    return render(request, 'genre_list.html', {'genres': genres})

def genre_create(request):
    if request.method == 'POST':
        genre_name_ = request.POST.get('genre_name')
        genre = Genre()
        genre.name = genre_name_
        genre.save()
        return redirect('genre_list')
    else:
        return render(request, 'genre_create.html')
    
def genre_delete(request, genre_id):
    genre = get_object_or_404(Genre, id=genre_id)
    # no need to check the request type since we only send post requests to this endpoint
    genre.delete()
    return redirect('genre_list')

# search functions

def search(request):
    return render(request, 'search_books.html')

def search_books_by_title(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        books = Book.objects.filter(title__icontains=title)
        return render(request, 'search_results.html', {'books': books})
    return render(request, 'search_books.html')

def search_books_by_author(request):
    if request.method == 'POST':
        author_name = request.POST.get('author_name')

        # select all books who is related to an author whose name contains author_name

        books = Book.objects.filter(authors__name__icontains=author_name)
        return render(request, 'search_results.html', {'books': books})
    return render(request, 'search_books.html')

def search_books_by_genre(request):
    if request.method == 'POST':
        genre_name = request.POST.get('genre_name')

        # select all books who is related to a genre whose name contains genre_name

        books = Book.objects.filter(genres__name__icontains=genre_name)
        return render(request, 'search_results.html', {'books': books})
    return render(request, 'search_books.html')