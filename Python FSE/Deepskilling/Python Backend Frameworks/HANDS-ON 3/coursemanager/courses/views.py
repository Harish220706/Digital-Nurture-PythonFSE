from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Course, Student
from .serializers import CourseSerializer, StudentSerializer, EnrollmentSerializer


def hello_view(request):
    """Hands-On 1 FBV, kept for reference."""
    return HttpResponse('Course Management API is running')


# --- Task 1: plain APIView versions (kept for reference / learning) ---

class CourseListView(APIView):
    """GET: list all courses. POST: create a new course."""

    def get(self, request):
        courses = Course.objects.all()
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CourseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CourseDetailView(APIView):
    """GET/PUT/DELETE a single course by pk."""

    def get(self, request, pk):
        course = get_object_or_404(Course, pk=pk)
        return Response(CourseSerializer(course).data)

    def put(self, request, pk):
        course = get_object_or_404(Course, pk=pk)
        serializer = CourseSerializer(course, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        course = get_object_or_404(Course, pk=pk)
        course.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# --- Task 2: ViewSets (preferred - full CRUD in a few lines) ---

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    @action(detail=True, methods=['get'])
    def students(self, request, pk=None):
        """GET /api/courses/{id}/students/ -> students enrolled in this course."""
        course = self.get_object()
        student_ids = course.enrollment_set.values_list('student_id', flat=True)
        students = Student.objects.filter(id__in=student_ids)
        return Response(StudentSerializer(students, many=True).data)


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class EnrollmentViewSet(viewsets.ModelViewSet):
    from .models import Enrollment
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer
