from django.shortcuts import render, get_object_or_404, redirect
from .models import Book, Author, Genre
from .forms import BookForm

# home page

def home_page(request):
    return render(request, 'home_page.html')

# CRUD operations on books

class MasterItem:
    def __init__(self, book_, author_names_, genre_names_):
        self.book = book_
        self.author_names = author_names_
        self.genre_names = genre_names_

def book_list(request):
    books = Book.objects.all()
    book_author_names = []
    book_genre_names = []
    master_list = []
    for book in books:
        authors = list(Author.objects.filter(books__id__icontains=book.id))
        genres = list(Genre.objects.filter(books__id__icontains=book.id))
        author_names = list(map(lambda x: x.name, authors))
        genre_names = list(map(lambda x: x.name, genres))
        print(author_names)
        print(genre_names)
        book_author_names.append(author_names)
        book_genre_names.append(genre_names)
    for i in range(len(books)):
        master_list.append(MasterItem(books[i], book_author_names[i], book_genre_names[i]))
    print(master_list)
    return render(request, 'book_list.html', {'master_list': master_list})

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
    # Get the existing book instance from the database or return a 404 error if not found
    book = get_object_or_404(Book, id=book_id)

    if request.method == 'POST':
        # If the form is submitted, process the data
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('book_list')  # Redirect to the book list after successful update
        else:
            print("Form errors:", form.errors)  # Print form errors for debugging
            print("POST data:", request.POST)   # Print request POST data for debugging
    else:
        # If the request is a GET, show the form with the existing book's data
        form = BookForm(instance=book)

    return render(request, 'book_form.html', {'form': form, 'id': book_id})

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
    else:
        print("request isn't post")
    return redirect('author_list')
    
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
    else:
        print("request isn't post")
    return redirect('genre_list')
    
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