from django.contrib.auth.models import AbstractUser
from django.db import models
import random

class User(AbstractUser):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=False)  
    confirmation_code = models.CharField(max_length=6, null=True, blank=True)
    code_created_at = models.DateTimeField(auto_now_add=True, null=True)
    
    def generate_confirmation_code(self):
        code = ''.join([str(random.randint(0, 9)) for _ in range(6)])
        self.confirmation_code = code
        self.save()
        return code
    
    def __str__(self):
        return self.username