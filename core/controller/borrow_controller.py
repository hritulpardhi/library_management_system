import json
import traceback
from datetime import datetime, timedelta
from django.db import transaction
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from core.models.books import Books
from core.models.users import Users
from core.models.borrow_book import BorrowBook

class BorrowController:
    @csrf_exempt
    @transaction.atomic
    def borrow_book(request, id):
        try:
            book = Books.objects.select_for_update().get(id=id)
            print("Book object found", book.__dict__)
            if book.is_available:
                request_data = json.loads(request.body.decode('utf-8'))
                user_obj = Users.objects.get(email=request_data.get('user_mail'))
                if not user_obj:
                    return JsonResponse({"message": "User not found."}, status=404)
                return_date = datetime.now() + timedelta(days=7)
                formatted_return_date = return_date.strftime('%Y-%m-%d %H:%M:%S')
                BorrowBook.objects.create(
                    book=book,
                    user=user_obj,
                    return_date=return_date
                )
                book.is_available = False
                book.save()
                return JsonResponse({
                    "message": f"Book : {book.title} borrowed successfully, your return date is {formatted_return_date}.",
                    "return_date": formatted_return_date
                }, status=200)
            else:
                print("Book not available")
                borrow_book_obj = BorrowBook.objects.filter(book=book).first()
                if borrow_book_obj:
                    formatted_borrowed_return_date = borrow_book_obj.return_date.strftime('%Y-%m-%d %H:%M:%S')
                    return JsonResponse({
                        "message": f"Book : {book.title} is already borrowed by {borrow_book_obj.user.name}. Return date is {formatted_borrowed_return_date}."
                    }, status=200)
                return JsonResponse({"message": "Book is not available for borrowing."}, status=400)
        except Exception as e:
            print("Exception:", traceback.format_exc())
            return JsonResponse({"message": "Something went wrong", "error": str(e)}, status=404)

    @csrf_exempt
    @transaction.atomic
    def return_book(request, id):
        try:
            book = Books.objects.select_for_update().get(id=id)
            if not book.is_available:
                borrow_book_obj = BorrowBook.objects.filter(book=book).first()
                if borrow_book_obj:
                    borrow_book_obj.is_returned = True
                    book.is_available = True
                    borrow_book_obj.save()
                    book.save()
                    return JsonResponse({"message": f"Book : {book.title} returned successfully."}, status=200)
                return JsonResponse({"message": "Book is not borrowed."}, status=400)
            return JsonResponse({"message": "Book is already available."}, status=400)
        except Exception as e:
            return JsonResponse({"message": "Something went wrong.", "error": str(e)}, status=404)
