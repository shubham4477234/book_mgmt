"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
# from django.urls import path

# urlpatterns = [
#     path('admin/', admin.site.urls),
# ]


from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from core.views import home_screen, student_book_list, student_download_book, custom_login_view
from core import views



urlpatterns = [
    path('', home_screen),  # root URL will now show welcome message
    path('admin/', admin.site.urls),
    path('api/', include('core.urls')),  # <-- assuming your app is named 'core'

    # 👇 Student book view and download
    path('student/books/', student_book_list, name='student_book_list'),
    path('student/books/download/<int:book_id>/', student_download_book, name='student_download_book'),

    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/login/', custom_login_view, name='login'),

]

# Add this to serve media files (PDFs) in development
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
