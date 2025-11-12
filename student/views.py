from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.conf import settings
from django.db.models import Count, Avg, Max
from django.contrib.auth import logout
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import UserSerializer
from exam.models import Exam
from .models import ExamAttempt, StudentProfile

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
        return redirect('/login/')

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


def custom_logout_view(request):
    """
    Custom logout view that handles both JWT tokens and sessions.
    Clears JWT cookies and session data, then redirects to login page.
    """
    # Logout the user from Django's session
    logout(request)
    
    # Create response to redirect to login page
    response = HttpResponseRedirect(reverse('login'))
    
    # Clear JWT cookies
    response.delete_cookie('jwt')
    response.delete_cookie('access_token')
    response.delete_cookie('refresh_token')
    
    # Clear any other authentication cookies
    response.delete_cookie('sessionid')
    
    return response


class MyExamsView(TemplateView):
    template_name = 'my_exams.html'
    
    def dispatch(self, request, *args, **kwargs):
        jwt_auth = JWTAuthentication()
        try:
            validated_token = jwt_auth.get_validated_token(request.COOKIES.get('jwt', ''))
            request.user = jwt_auth.get_user(validated_token)
        except Exception:
            pass
            
        if not request.user.is_authenticated:
            return redirect('/login/')
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        student = self.request.user.studentprofile
        
        # Get all exams
        all_exams = Exam.objects.all()
        
        # Get exam attempts for each exam
        exam_data = []
        for exam in all_exams:
            attempts = ExamAttempt.objects.filter(student=student, exam=exam).order_by('-attempt_number')
            latest_attempt = attempts.first() if attempts.exists() else None
            
            # Calculate next attempt number
            next_attempt = (latest_attempt.attempt_number + 1) if latest_attempt else 1
            
            # Get best score
            best_attempt = attempts.order_by('-score').first()
            best_score = best_attempt.score if best_attempt else None
            
            exam_data.append({
                'exam': exam,
                'attempted': attempts.exists(),
                'attempt_count': attempts.count(),
                'latest_attempt': latest_attempt,
                'best_score': best_score,
                'next_attempt': next_attempt
            })
        
        context['exam_data'] = exam_data
        return context


class ResultsView(TemplateView):
    template_name = 'results.html'
    
    def dispatch(self, request, *args, **kwargs):
        jwt_auth = JWTAuthentication()
        try:
            validated_token = jwt_auth.get_validated_token(request.COOKIES.get('jwt', ''))
            request.user = jwt_auth.get_user(validated_token)
        except Exception:
            pass
            
        if not request.user.is_authenticated:
            return redirect('/login/')
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        student = self.request.user.studentprofile
        
        # Get all attempts ordered by date
        all_attempts = ExamAttempt.objects.filter(
            student=student
        ).select_related('exam').order_by('-date_taken')
        
        # Group by exam
        exams_dict = {}
        for attempt in all_attempts:
            exam_id = attempt.exam.id
            if exam_id not in exams_dict:
                exams_dict[exam_id] = {
                    'exam': attempt.exam,
                    'attempts': [],
                    'best_score': 0,
                    'best_attempt': None
                }
            
            exams_dict[exam_id]['attempts'].append(attempt)
            
            # Track best score
            if attempt.score > exams_dict[exam_id]['best_score']:
                exams_dict[exam_id]['best_score'] = attempt.score
                exams_dict[exam_id]['best_attempt'] = attempt
        
        # Convert to list and sort by most recent attempt
        exam_results = []
        for exam_data in exams_dict.values():
            exam_data['attempt_count'] = len(exam_data['attempts'])
            exam_data['latest_attempt'] = exam_data['attempts'][0] if exam_data['attempts'] else None
            exam_results.append(exam_data)
        
        # Sort by latest attempt date
        exam_results.sort(key=lambda x: x['latest_attempt'].date_taken if x['latest_attempt'] else None, reverse=True)
        
        context['exam_results'] = exam_results
        context['total_attempts'] = all_attempts.count()

        # Ads config: show only for non-premium students
        is_premium = bool(getattr(student, 'is_premium', False))
        context['show_ads'] = (not is_premium)
        context['adsense_client'] = getattr(settings, 'ADSENSE_CLIENT', '')
        context['adsense_slot_results'] = getattr(settings, 'ADSENSE_SLOT_RESULTS', '')
        
        return context


class SettingsView(TemplateView):
    template_name = 'settings.html'
    
    def dispatch(self, request, *args, **kwargs):
        jwt_auth = JWTAuthentication()
        try:
            validated_token = jwt_auth.get_validated_token(request.COOKIES.get('jwt', ''))
            request.user = jwt_auth.get_user(validated_token)
        except Exception:
            pass
            
        if not request.user.is_authenticated:
            return redirect('/login/')
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = self.request.user.studentprofile
        context['user'] = self.request.user
        return context


@csrf_exempt
@require_http_methods(["POST"])
def update_profile(request):
    """Update student profile"""
    jwt_auth = JWTAuthentication()
    try:
        validated_token = jwt_auth.get_validated_token(request.COOKIES.get('jwt', ''))
        user = jwt_auth.get_user(validated_token)
    except Exception:
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'Authentication required'}, status=401)
        user = request.user
    
    try:
        import json
        data = json.loads(request.body)
        profile = user.studentprofile
        
        # Update profile fields
        if 'first_name' in data:
            profile.first_name = data['first_name']
        if 'last_name' in data:
            profile.last_name = data['last_name']
        if 'email' in data:
            profile.email = data['email']
            user.email = data['email']  # Also update user email
        if 'phone_number' in data:
            profile.phone_number = data['phone_number']
        if 'date_of_birth' in data:
            profile.date_of_birth = data['date_of_birth']
        if 'course_enrolled' in data:
            profile.course_enrolled = data['course_enrolled']
        if 'address' in data:
            profile.address = data['address']
        
        profile.save()
        user.save()
        
        return JsonResponse({'success': True, 'message': 'Profile updated successfully'})
    except Exception as e:
        # Log the error for debugging
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f'Profile update error: {str(e)}')
        return JsonResponse({'error': 'Failed to update profile'}, status=400)


@csrf_exempt
@require_http_methods(["GET"])
def dashboard_data(request):
    """Get real-time dashboard data for graphs"""
    jwt_auth = JWTAuthentication()
    try:
        validated_token = jwt_auth.get_validated_token(request.COOKIES.get('jwt', ''))
        user = jwt_auth.get_user(validated_token)
    except Exception:
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'Authentication required'}, status=401)
        user = request.user
    
    try:
        student = user.studentprofile
        
        # Get exam attempts ordered by date
        attempts = ExamAttempt.objects.filter(student=student).order_by('date_taken')
        
        # Prepare scores over time data
        score_labels = []
        score_data = []
        for attempt in attempts[:10]:  # Last 10 attempts
            score_labels.append(attempt.date_taken.strftime('%m/%d'))
            score_data.append(float(attempt.score))
        
        # Get subject/exam distribution data
        exam_stats = {}
        for attempt in attempts:
            exam_name = attempt.exam.name
            if exam_name not in exam_stats:
                exam_stats[exam_name] = {'count': 0, 'total_score': 0}
            exam_stats[exam_name]['count'] += 1
            exam_stats[exam_name]['total_score'] += float(attempt.score)
        
        # Calculate average scores per exam
        subject_labels = []
        subject_data = []
        for exam_name, stats in list(exam_stats.items())[:4]:  # Top 4 exams
            subject_labels.append(exam_name)
            avg_score = stats['total_score'] / stats['count']
            subject_data.append(round(avg_score, 1))
        
        return JsonResponse({
            'scores': {
                'labels': score_labels,
                'data': score_data
            },
            'subjects': {
                'labels': subject_labels,
                'data': subject_data
            }
        })
    except Exception as e:
        # Log the error for debugging
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f'Dashboard data error: {str(e)}')
        return JsonResponse({'error': 'Failed to load dashboard data'}, status=400)