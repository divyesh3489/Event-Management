from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin
import uuid
from django.utils import timezone

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        if not password:
            raise ValueError('The Password field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        user = self.create_user(email, password, **extra_fields)
        user.is_staff = True
        user.is_superuser = True
        user.is_verified = True
        user.save(using=self._db)
        return user

    def delete_user(self, email):
        try:
            user = self.get(email=email)
            user.is_active = False
            user.deleted_at = timezone.now()
            user.save()
            return True
        except:
            print(f"User with email {email} does not exist.")
            return False

class ActiveUserManager(models.Manager):
    def active(self):
        return self.filter(is_active=True)

class User(AbstractUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) 
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    objects = UserManager()
    active_objects = ActiveUserManager()
    USERNAME_FIELD = 'email'
    
    REQUIRED_FIELDS = []
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    username = None


    