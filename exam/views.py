from django.shortcuts import render
from rest_framework import generics
from exam.models import Exam
from .serializers import (
    ExamSerializer,
    TestPaperSerializer,
    QuestionTypeMCQSerializer,
    QuestionTypeNumericalSerializer,
    QuestionTypeMSQSerializer,
)
# Create your views here.


class ExamListView(generics.ListAPIView):
    queryset = Exam.objects.all()
    serializer_class = ExamSerializer
    permission_classes = []  # Add appropriate permissions  

class ExamDetailView(generics.RetrieveAPIView):
    queryset = Exam.objects.all()
    serializer_class = ExamSerializer
    permission_classes = []  # Add appropriate permissions  
    lookup_field = 'id'

class TestPaperDetailView(generics.RetrieveAPIView):
    queryset = Exam.objects.all()
    serializer_class = TestPaperSerializer
    permission_classes = []  # Add appropriate permissions  
    lookup_field = 'id'

class QuestionTypeMCQDetailView(generics.RetrieveAPIView):
    queryset = Exam.objects.all()
    serializer_class = QuestionTypeMCQSerializer
    permission_classes = []  # Add appropriate permissions  
    lookup_field = 'id'

class QuestionTypeNumericalDetailView(generics.RetrieveAPIView):
    queryset = Exam.objects.all()
    serializer_class = QuestionTypeNumericalSerializer
    permission_classes = []  # Add appropriate permissions  
    lookup_field = 'id'

class QuestionTypeMSQDetailView(generics.RetrieveAPIView):
    queryset = Exam.objects.all()
    serializer_class = QuestionTypeMSQSerializer
    permission_classes = []  # Add appropriate permissions  
    lookup_field = 'id'

def add_exam(request):
    return render(request, 'exam/add_exam.html')

def add_test_paper(request):
    return render(request, 'exam/add_test_paper.html')

def view_exams(request):
    return render(request, 'exam/view_exams.html')

def view_test_papers(request):
    return render(request, 'exam/view_test_papers.html')
