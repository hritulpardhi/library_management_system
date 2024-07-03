import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from core.models.books import Books

class BookController:
    @csrf_exempt
    def add_book(request):
        try:
            if request.method == "POST":
                request_data = json.loads(request.body.decode('utf-8'))
                print("request_data", request_data)
                book_obj = Books.objects.create(
                    title=request_data.get("title"),
                    author=request_data.get("author"),
                    genre=request_data.get("genre"),
                    is_available=request_data.get("is_available"),
                )
                context = {
                    "book": {
                        "id": book_obj.id,
                        "title": book_obj.title,
                        "author": book_obj.author,
                        "genre": book_obj.genre,
                        "is_available": book_obj.is_available,
                    }
                }
                return JsonResponse(context)
        except Exception as e:
            return JsonResponse({'error': str(e)})

    @csrf_exempt
    def get_book(request, id):
        try:
            book_obj = Books.objects.get(id=id)
            response_data = {
                "id": book_obj.id,
                "title": book_obj.title,
                'author': book_obj.author,
                'genre': book_obj.genre,
                'is_available': book_obj.is_available,
            }
            return JsonResponse({"response_data": response_data})
        except Exception as e:
            return JsonResponse({'error': str(e), 'message': 'Book not found!'})

    @csrf_exempt
    def update_book(request, id):
        try:
            book_obj = Books.objects.get(id=id)
            if request.method == "PUT":
                request_data = json.loads(request.body.decode('utf-8'))
                print("request_data", request_data)
                book_obj.title = request_data.get("title")
                book_obj.author = request_data.get("author")
                book_obj.genre = request_data.get("genre")
                book_obj.is_available = request_data.get("is_available")
                book_obj.save()
                response_data = {
                    "id": id,
                    "title": book_obj.title,
                    'author': book_obj.author,
                    'genre': book_obj.genre,
                    'is_available': book_obj.is_available,
                    'message': 'Book data updated successfully'
                }
            else:
                response_data = {
                    "message": "Unable to update the book. Please send PUT request to update the book!"
                }
            return JsonResponse({"response_data": response_data})
        except Exception as e:
            return JsonResponse({'error': str(e), 'message': 'Book not found!'})

    @csrf_exempt
    def get_all_books(request):
        try:
            if request.method == "POST":    
                request_data = json.loads(request.body.decode('utf-8'))
            page = request_data.get('page', 1)
            per_page = request_data.get('per_page', 10)
            books_list = Books.objects.all()
            paginator = Paginator(books_list, per_page)
            try:
                books = paginator.page(page)
            except PageNotAnInteger:
                books = paginator.page(1)
            except EmptyPage:
                books = paginator.page(paginator.num_pages)
            books_data = []
            for book in books:
                books_data.append({
                    "id": book.id,
                    "title": book.title,
                    "author": book.author,
                    "genre": book.genre,
                    "is_available": book.is_available
                })

            response_data = {
                "books": books_data,
                "page": page,
                "total_pages": paginator.num_pages,
                "total_books": paginator.count
            }

            return JsonResponse(response_data, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e), 'message': 'Something went wrong!'}, status=500)
