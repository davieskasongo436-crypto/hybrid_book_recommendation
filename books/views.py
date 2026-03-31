from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Book
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def book_list(request):
    # Handle search
    query = request.GET.get('q')
    books = Book.objects.all()
    if query:
        books = books.filter(title__icontains=query) | books.filter(author__icontains=query)

    # Add pagination
    paginator = Paginator(books, 10)  # 10 books per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'books/book_list.html', {
        'page_obj': page_obj,
        'query': query
    })


def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    books = list(Book.objects.all())

    # TF-IDF matrix from descriptions
    descriptions = [b.description for b in books]
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(descriptions)

    # Find similarity scores
    idx = books.index(book)
    cosine_sim = cosine_similarity(tfidf_matrix[idx], tfidf_matrix).flatten()

    # Get top 3 similar books (excluding itself)
    similar_indices = cosine_sim.argsort()[-4:-1][::-1]  # last 3, excluding itself
    recommendations = [books[i] for i in similar_indices if books[i] != book]

    return render(request, 'books/book_detail.html', {
        'book': book,
        'recommendations': recommendations
    })
