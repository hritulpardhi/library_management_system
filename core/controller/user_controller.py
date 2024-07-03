import json
import traceback
from core.models.users import Users
from django.shortcuts import render
from django.http import JsonResponse

from core.models.books import Books
from core.models.borrow_book import BorrowBook


class UserController:
    def home(request):
        if request.method == "GET":
            context = {}
            return render(request, "user_management/home.html", context)
        
    def login(request):
        if request.method == "GET":
            context = {}
            return render(request, "user_management/login.html", context)
        elif request.method == "POST":
            request_data = json.loads(request.body.decode('utf-8'))
            print("request_data", request_data)
            try:
                user_obj = Users.objects.get(email=request_data.get("username"), password=request_data.get("password"))
                context = {
                    "user": user_obj,
                }
                return JsonResponse({'message': 'Login successful'})
            except Users.DoesNotExist:
                return JsonResponse({'error': 'Invalid credentials'}, status=401)
    
    # Hashing can be used to store the password to the DB and hash can be validated while loggin in as well.
    def register(request):
        try:
            if request.method == "GET":
                context = {}
                return render(request, "user_management/register.html", context)
            elif request.method == "POST":
                request_data = json.loads(request.body.decode('utf-8'))
                print("request_data", request_data)
                user_obj = Users.objects.create(
                    name=request_data.get("name"),
                    email=request_data.get("email"),
                    password=request_data.get("password"),
                    role=request_data.get("role"),
                )
                context = {
                    "user": user_obj,
                }
                return JsonResponse({'message': 'Registration successful'})

        except Exception as e:
            print("Exception:", traceback.format_exc())
            return JsonResponse({'error': str(e)}, status=500)
        
    def dashboard(request):
        try:
            if request.method == "GET":
                context = {}
                books_data = Books.objects.all()
                context["books"] = books_data
                borrow_data = BorrowBook.objects.filter(is_returned = False)
                context["borrow_data"] = borrow_data
                return render(request, "book_management/dashboard.html", context)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
