# from django.db import models

# Create your models here.

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import Group, Permission

class Student(AbstractUser):
    is_student = models.BooleanField(default=True)
    groups = models.ManyToManyField(
        Group,
        related_name='student_groups',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups'
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='student_permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions'
    )

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)



# class Book(models.Model):
#     title = models.CharField(max_length=255)
#     author = models.CharField(max_length=255)
#     published_date = models.DateField()
#     pdf = models.FileField(upload_to='books/', null=True, blank=True)  # <-- Add null=True, blank=True


