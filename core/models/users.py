from  django.db import models
from core.models.base_model import BaseModel

class Users(BaseModel):
    name = models.CharField(max_length=128)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    role = models.CharField(max_length=64)
    
    class Meta:
        managed = True
        db_table = 'users'