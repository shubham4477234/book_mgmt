# students.py (or admin.py if you're registering models for admin panel)
from django.contrib import admin  # Not student
from .models import Student, Book

admin.site.register(Book)
admin.site.register(Student)
