from  django.db import models
from core.models.base_model import BaseModel
from core.models.books import Books
from core.models.users import Users

class BorrowBook(BaseModel):
    book = models.ForeignKey(Books, related_name='borrow_book', on_delete=models.CASCADE)
    user = models.ForeignKey(Users, related_name='borrow_user', on_delete=models.CASCADE)
    borrowed_at = models.DateTimeField(auto_now_add=True)
    return_date = models.DateTimeField(null=True, blank=True)
    is_returned = models.BooleanField(default=False)
    
    class Meta:
        managed = True
        db_table = 'borrow_book'