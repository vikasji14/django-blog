from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    """
    Custom user model that extends the default Django user model.
    """
    email = models.EmailField(unique=True,null=False, blank=False)  # Ensure email is unique
    
    
    def __str__(self):
        return self.username  # or self.email, or any other field you prefer