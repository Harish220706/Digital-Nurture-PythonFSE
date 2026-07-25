from django.http import HttpResponse


def hello_view(request):
    """Task 2, step 8: simple function-based view (FBV)."""
    return HttpResponse('Course Management API is running')
