from  django.db import models
from core.models.base_model import BaseModel

class Books(BaseModel):
    title = models.CharField(db_index=True, max_length=255, unique=True)
    author = models.EmailField(max_length=255)
    genre = models.CharField(max_length=255)
    is_available = models.BooleanField(default=True)
    
    class Meta:
        managed = True
        db_table = 'books'