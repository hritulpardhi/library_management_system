from django.urls import path

from .controller.user_controller import UserController
from .controller.book_controller import BookController
from .controller.borrow_controller import BorrowController


urlpatterns = [
    path('', UserController.home, name="home"),
    path("login/", UserController.login, name="login"),
    path("register/", UserController.register, name="register"),
    path("dashboard/", UserController.dashboard, name="dashboard"),
    path("books/add/", BookController.add_book, name="add_book"),
    path("books/id/<int:id>", BookController.get_book, name="add_book"),
    path("books/all/", BookController.get_all_books, name="get_all_books"),
    path("books/update/<int:id>", BookController.update_book, name="update_book"),
    path("books/borrow/<int:id>", BorrowController.borrow_book, name="borrow_book"),
    path("books/return/<int:id>", BorrowController.return_book, name="return_book"),
]