from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.db.models import Count, Avg
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import UserSerializer
from exam.models import Exam
from .models import ExamAttempt

class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


class UserDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


from rest_framework_simplejwt.authentication import JWTAuthentication
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

class DashboardView(TemplateView):
    template_name = 'dashboard.html'
    
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
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)
    
    def handle_no_permission(self):
        from django.shortcuts import redirect
        return redirect('/')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        student = self.request.user.studentprofile
        
        # Get upcoming exams (all exams not yet attempted)
        attempted_exam_ids = ExamAttempt.objects.filter(
            student=student
        ).values_list('exam_id', flat=True)
        
        context['upcoming_exams'] = Exam.objects.exclude(
            id__in=attempted_exam_ids
        ).order_by('id')[:5]  # Show 5 upcoming exams
        
        # Get recent attempts
        context['recent_attempts'] = ExamAttempt.objects.filter(
            student=student
        ).select_related('exam')[:5]  # Show 5 recent attempts
        
        # Get performance stats
        attempts = ExamAttempt.objects.filter(student=student)
        context['total_exams_taken'] = attempts.values('exam').distinct().count()
        context['average_score'] = attempts.aggregate(Avg('score'))['score__avg'] or 0
        
        return context