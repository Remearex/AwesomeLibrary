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

def book_detail(request, book_title):
    book = get_object_or_404(Book, title=book_title)
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

def book_update(request, book_title):
    book = get_object_or_404(Book, title=book_title)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('book_list')
        else:
            print(form.errors)  # Print form errors for debugging
    else:
        form = BookForm(instance=book)
    return render(request, 'book_form.html', {'form': form})

def book_delete(request, book_title):
    book = get_object_or_404(Book, title=book_title)
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
    
def author_delete(request, author_name):
    author = get_object_or_404(Author, name=author_name)
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
    
def genre_delete(request, genre_name):
    genre = get_object_or_404(Genre, name=genre_name)
    # no need to check the request type since we only send post requests to this endpoint
    genre.delete()
    return redirect('genre_list')

# search functions

def search(request):
    if request.method == 'POST':
        search_category = request.POST.get('search_category')
        search_mode = request.POST.get('search_mode')
        raw_input = request.POST.get('raw_input')
        input = list(map(lambda x: x.strip(), raw_input.split(',')))
        if search_category == 'Titles':
            query_result = search_books_by_title(search_mode, input)
        elif search_category == 'Authors':
            query_result = search_books_by_author(search_mode, input)
        else:
            query_result = search_books_by_genre(search_mode, input)
        return render(request, 'search_results.html', {'books': query_result})
    return render(request, 'search_books.html')

def search_books_by_title(search_mode, input):
    if search_mode == 'contains_all':
        query_result = Book.objects.all()
        for title in input:
            query_result = query_result.filter(title__icontains=title)
        return query_result
    else:
        query_result = Book.objects.none()
        for title in input:
            query_result = query_result.union(Book.objects.filter(title__icontains=title))
        return query_result

def search_books_by_author(search_mode, input):
    if search_mode == 'contains_all':
        query_result = Book.objects.all()
        for name in input:
            query_result = query_result.filter(authors__name__icontains=name)
        return query_result
    else:
        query_result = Book.objects.none()
        for name in input:
            query_result = query_result.union(Book.objects.filter(authors__name__icontains=name))
        return query_result

def search_books_by_genre(search_mode, input):
    if search_mode == 'contains_all':
        query_result = Book.objects.all()
        for name in input:
            query_result = query_result.filter(genres__name__icontains=name)
        return query_result
    else:
        query_result = Book.objects.none()
        for name in input:
            query_result = query_result.union(Book.objects.filter(genres__name__icontains=name))
        return query_result