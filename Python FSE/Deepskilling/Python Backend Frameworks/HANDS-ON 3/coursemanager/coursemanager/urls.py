"""
coursemanager URL Configuration
Delegates /api/ to the courses app so URL config stays modular.
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('courses.urls')),
]
