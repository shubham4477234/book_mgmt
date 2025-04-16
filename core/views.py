from django.shortcuts import render

# Create your views here.

from rest_framework import viewsets
from .models import Book, Student
from .serializers import BookSerializer, StudentSerializer
from rest_framework.permissions import IsAdminUser
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def perform_create(self, serializer):
        serializer.save(uploaded_by=self.request.user)

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.filter(is_student=True)
    serializer_class = StudentSerializer
    permission_classes = [IsAdminUser]

# def home_screen(request):
#     return HttpResponse("Welcome to the Book Management System!")
from django.http import HttpResponse

def home_screen(request):
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Book Management System</title>
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background-color: #f4f6f9;
                margin: 0;
                padding: 0;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
            }
            .container {
                background-color: #ffffff;
                padding: 40px 60px;
                border-radius: 12px;
                box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
                text-align: center;
            }
            h1 {
                color: #333333;
                margin-bottom: 10px;
            }
            p {
                color: #666666;
                font-size: 18px;
                margin-top: 0;
            }
            .btn {
                margin-top: 20px;
                display: inline-block;
                background-color: #4CAF50;
                color: white;
                padding: 12px 24px;
                text-decoration: none;
                border-radius: 6px;
                transition: background-color 0.3s ease;
                font-size: 16px;
            }
            .btn:hover {
                background-color: #45a049;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>📚 Welcome to the Book Management System</h1>
            <p>Manage your books efficiently with a simple and intuitive interface.</p>
            <a href="/admin/" class="btn">Go to Admin Panel</a>
            <a href="/accounts/login/" class="btn">Go to Student Panel</a>
        </div>
    </body>
    </html>
    """
    return HttpResponse(html_content)

###------------------------------------------------------------------------------------------------------------------------------------------------------------------
###------------------------------------------------------------------------------------------------------------------------------------------------------------------


from django.shortcuts import render, get_object_or_404
from .models import Book
from django.http import FileResponse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template import Template, Context

@login_required
def student_book_list(request):
    if hasattr(request.user, 'is_student') and request.user.is_student:
        books = Book.objects.all()

        html_string = """
        <!DOCTYPE html>
        <html>
        <head><title>Book Library</title></head>
        <body>
            <h2>Welcome Student!</h2>
            <ul>
                {% for book in books %}
                    <li>
                        <strong>{{ book.title }}</strong> by {{ book.author }}
                        {% if book.file %}
                            - <a href="/api/student/book/{{ book.id }}/download/">Download</a>
                        {% else %}
                            - No file available
                        {% endif %}
                    </li>
                {% endfor %}
            </ul>
        </body>
        </html>
        """

        template = Template(html_string)
        context = Context({'books': books})
        return HttpResponse(template.render(context))
    else:
        return render(request, 'unauthorized.html')


@login_required
def student_download_book(request, book_id):
    if hasattr(request.user, 'is_student') and request.user.is_student:
        book = get_object_or_404(Book, id=book_id)
        return FileResponse(book.file.open('rb'), as_attachment=True)
    else:
        return render(request, 'unauthorized.html')


from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import Template, Context
from django.middleware.csrf import get_token

def custom_login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            next_url = request.GET.get('next', '/')
            return redirect(next_url)
        else:
            error_message = "Invalid username or password"
    else:
        error_message = None

    csrf_token = get_token(request)

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Login</title>
    </head>
    <body>
        <h2>Login</h2>
        {'<p style="color:red;">' + error_message + '</p>' if error_message else ''}
        <form method="post">
            <input type="hidden" name="csrfmiddlewaretoken" value="{csrf_token}">
            <p><label>Username:</label><input type="text" name="username" required></p>
            <p><label>Password:</label><input type="password" name="password" required></p>
            <button type="submit">Login</button>
        </form>
    </body>
    </html>
    """
    return HttpResponse(html_content)
