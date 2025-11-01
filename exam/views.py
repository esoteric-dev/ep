from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework import generics
from rest_framework_simplejwt.authentication import JWTAuthentication
from exam.models import Exam, TestPaper, Question_type_mcq, Question_type_msq, Question_type_numerical
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


class LandingPageView(TemplateView):
    template_name = 'landing.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get upcoming exams (limit to 4 for display)
        context['upcoming_exams'] = Exam.objects.all()[:4]
        return context


class InstructionView(TemplateView):
    template_name = 'instructions.html'
    
    def dispatch(self, request, *args, **kwargs):
        # Try JWT authentication first
        jwt_auth = JWTAuthentication()
        try:
            validated_token = jwt_auth.get_validated_token(request.COOKIES.get('jwt', ''))
            request.user = jwt_auth.get_user(validated_token)
        except Exception:
            # If JWT auth fails, fall back to session auth
            pass
            
        # Check if user is authenticated through any means
        if not request.user.is_authenticated:
            return redirect('/login/')
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        exam_id = self.kwargs.get('exam_id')
        exam = get_object_or_404(Exam, id=exam_id)
        
        # Get total questions count from all test papers
        total_questions = 0
        for test_paper in exam.test_papers.filter(is_active=True):
            total_questions += test_paper.total_questions
        
        context['exam'] = exam
        context['total_questions'] = total_questions
        return context


class ExamView(TemplateView):
    template_name = 'exam.html'
    
    def dispatch(self, request, *args, **kwargs):
        # Try JWT authentication first
        jwt_auth = JWTAuthentication()
        try:
            validated_token = jwt_auth.get_validated_token(request.COOKIES.get('jwt', ''))
            request.user = jwt_auth.get_user(validated_token)
        except Exception:
            # If JWT auth fails, fall back to session auth
            pass
            
        # Check if user is authenticated through any means
        if not request.user.is_authenticated:
            return redirect('/login/')
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        exam_id = self.kwargs.get('exam_id')
        exam = get_object_or_404(Exam, id=exam_id)
        language = self.request.GET.get('language', 'English')
        
        # Get the first active test paper for this exam
        test_paper = exam.test_papers.filter(is_active=True).first()
        
        if test_paper:
            # Get all questions from the test paper
            mcq_questions = Question_type_mcq.objects.filter(test_paper=test_paper).order_by('question_number')
            msq_questions = Question_type_msq.objects.filter(test_paper=test_paper).order_by('question_number')
            numerical_questions = Question_type_numerical.objects.filter(test_paper=test_paper).order_by('question_number')
            
            # Combine all questions with their types
            all_questions = []
            for q in mcq_questions:
                all_questions.append({
                    'id': q.id,
                    'type': 'mcq',
                    'number': q.question_number,
                    'text': q.question_text,
                    'image': q.question_image,
                    'options': {
                        'A': q.option_a,
                        'B': q.option_b,
                        'C': q.option_c,
                        'D': q.option_d
                    },
                    'correct_option': q.correct_option,
                    'marks': q.marks,
                    'negative_marks': q.negative_marks
                })
            
            for q in msq_questions:
                all_questions.append({
                    'id': q.id,
                    'type': 'msq',
                    'number': q.question_number,
                    'text': q.question_text,
                    'image': q.question_image,
                    'options': {
                        'A': q.option_a,
                        'B': q.option_b,
                        'C': q.option_c,
                        'D': q.option_d
                    },
                    'correct_options': q.correct_options,
                    'marks': q.marks,
                    'negative_marks': q.negative_marks
                })
            
            for q in numerical_questions:
                all_questions.append({
                    'id': q.id,
                    'type': 'numerical',
                    'number': q.question_number,
                    'text': q.question_text,
                    'image': q.question_image,
                    'correct_answer': q.correct_answer,
                    'marks': q.marks,
                    'negative_marks': q.negative_marks
                })
            
            # Sort questions by question number
            all_questions.sort(key=lambda x: x['number'])
            
            context['test_paper'] = test_paper
            context['questions'] = all_questions
        else:
            context['test_paper'] = None
            context['questions'] = []
        
        context['exam'] = exam
        context['language'] = language
        context['duration_minutes'] = int(exam.duration.total_seconds() / 60)
        
        return context
