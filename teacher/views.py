from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.db.models import Count, Avg, Sum, Q
from django.utils import timezone
from datetime import timedelta
import json
import os
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

try:
    import pandas as pd
    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False

from teacher.models import TeacherProfile
from exam.models import Exam, TestPaper, Question_type_mcq, Question_type_msq, Question_type_numerical
from student.models import ExamAttempt, StudentProfile


class TeacherLoginView(TemplateView):
    """Teacher login page"""
    template_name = 'teacher/login.html'
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            try:
                if hasattr(request.user, 'teacherprofile'):
                    return redirect('teacher-dashboard')
            except:
                pass
        return super().dispatch(request, *args, **kwargs)


@require_http_methods(["POST"])
@csrf_exempt
def teacher_login_api(request):
    """API endpoint for teacher login"""
    try:
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return JsonResponse({'success': False, 'error': 'Username and password required'}, status=400)
        
        user = authenticate(request, username=username, password=password)
        
        if user is None:
            return JsonResponse({'success': False, 'error': 'Invalid credentials'}, status=401)
        
        # Check if user is a teacher
        try:
            teacher_profile = user.teacherprofile
        except TeacherProfile.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Access denied. Teacher account required.'}, status=403)
        
        login(request, user)
        return JsonResponse({'success': True, 'redirect': '/teacher/dashboard/'})
    
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


class TeacherDashboardView(LoginRequiredMixin, TemplateView):
    """Teacher dashboard with analytics"""
    template_name = 'teacher/dashboard.html'
    
    def dispatch(self, request, *args, **kwargs):
        # Check if user is a teacher
        try:
            request.user.teacherprofile
        except:
            return redirect('/login/')
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Total exams created
        total_exams = Exam.objects.count()
        context['total_exams'] = total_exams
        
        # Total test papers
        total_test_papers = TestPaper.objects.count()
        context['total_test_papers'] = total_test_papers
        
        # Total questions
        total_mcq = Question_type_mcq.objects.count()
        total_msq = Question_type_msq.objects.count()
        total_numerical = Question_type_numerical.objects.count()
        context['total_questions'] = total_mcq + total_msq + total_numerical
        context['mcq_count'] = total_mcq
        context['msq_count'] = total_msq
        context['numerical_count'] = total_numerical
        
        # Total students
        total_students = StudentProfile.objects.count()
        context['total_students'] = total_students
        
        # Total exam attempts
        total_attempts = ExamAttempt.objects.count()
        context['total_attempts'] = total_attempts
        
        # Average score across all attempts
        avg_score = ExamAttempt.objects.aggregate(Avg('percentage'))['percentage__avg'] or 0
        context['average_score'] = round(avg_score, 2)
        
        # Recent exam attempts (last 10)
        recent_attempts = ExamAttempt.objects.select_related('exam', 'student').order_by('-id')[:10]
        context['recent_attempts'] = recent_attempts
        
        # Exam performance data (top 5 exams by attempts)
        exam_stats = ExamAttempt.objects.values('exam__name').annotate(
            attempt_count=Count('id'),
            avg_score=Avg('percentage')
        ).order_by('-attempt_count')[:5]
        context['exam_stats'] = exam_stats
        
        # Recent exams created
        recent_exams = Exam.objects.order_by('-id')[:5]
        context['recent_exams'] = recent_exams
        
        return context


class CreateExamView(LoginRequiredMixin, TemplateView):
    """Page to create a new exam"""
    template_name = 'teacher/create_exam.html'
    
    def dispatch(self, request, *args, **kwargs):
        try:
            request.user.teacherprofile
        except:
            return redirect('/login/')
        return super().dispatch(request, *args, **kwargs)


@csrf_exempt
@require_http_methods(["POST"])
@login_required
def create_exam_api(request):
    """API endpoint to create a new exam"""
    try:
        # Check if user is a teacher
        try:
            request.user.teacherprofile
        except:
            return JsonResponse({'success': False, 'error': 'Access denied. Teacher account required.'}, status=403)
        
        data = json.loads(request.body)
        name = data.get('name')
        description = data.get('description', '')
        duration_minutes = data.get('duration_minutes')
        total_marks = data.get('total_marks', 0)
        language = data.get('language', 'English')
        
        if not name or not duration_minutes:
            return JsonResponse({'success': False, 'error': 'Name and duration are required'}, status=400)
        
        exam = Exam.objects.create(
            name=name,
            description=description,
            duration=timedelta(minutes=int(duration_minutes)),
            total_marks=float(total_marks) if total_marks else 0,
            language=language
        )
        
        return JsonResponse({
            'success': True,
            'exam_id': exam.id,
            'message': 'Exam created successfully'
        })
    
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


class UploadPaperView(LoginRequiredMixin, TemplateView):
    """Page to upload question papers from Excel"""
    template_name = 'teacher/upload_paper.html'
    
    def dispatch(self, request, *args, **kwargs):
        try:
            request.user.teacherprofile
        except:
            return redirect('/login/')
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['exams'] = Exam.objects.all().order_by('-id')
        return context


@csrf_exempt
@require_http_methods(["POST"])
@login_required
def upload_paper_api(request):
    """API endpoint to upload question papers from Excel"""
    try:
        # Check if user is a teacher
        try:
            request.user.teacherprofile
        except:
            return JsonResponse({'success': False, 'error': 'Access denied. Teacher account required.'}, status=403)
        
        if 'file' not in request.FILES:
            return JsonResponse({'success': False, 'error': 'No file uploaded'}, status=400)
        
        excel_file = request.FILES['file']
        exam_id = request.POST.get('exam_id')
        
        if not exam_id:
            return JsonResponse({'success': False, 'error': 'Exam ID is required'}, status=400)
        
        exam = get_object_or_404(Exam, id=exam_id)
        
        # Save file temporarily
        file_path = default_storage.save(f'temp/{excel_file.name}', ContentFile(excel_file.read()))
        full_path = default_storage.path(file_path)
        
        if not PANDAS_AVAILABLE:
            return JsonResponse({'success': False, 'error': 'pandas library is required. Please install it: pip install pandas openpyxl'}, status=500)
        
        errors = []
        created_count = 0
        
        try:
            # Read the Excel file
            df = pd.read_excel(full_path, sheet_name=None)
            
            # Extract exam details if Exam_Info sheet exists (optional - exam is already selected)
            exam_info = None
            if 'Exam_Info' in df:
                exam_info = df['Exam_Info'].iloc[0]
            
            # Process each test paper sheet
            for sheet_name, sheet_data in df.items():
                if sheet_name == 'Exam_Info':
                    continue
                
                # Validate required columns
                required_columns = ['Question Type', 'Question Number', 'Question Text']
                missing_columns = [col for col in required_columns if col not in sheet_data.columns]
                if missing_columns:
                    errors.append(f"Sheet '{sheet_name}': Missing required columns: {', '.join(missing_columns)}")
                    continue
                
                # Check if test paper already exists
                paper_code = sheet_name
                test_paper, created = TestPaper.objects.get_or_create(
                    exam=exam,
                    paper_code=paper_code,
                    defaults={'total_questions': len(sheet_data)}
                )
                
                if not created:
                    # Delete existing questions for this paper
                    Question_type_mcq.objects.filter(test_paper=test_paper).delete()
                    Question_type_msq.objects.filter(test_paper=test_paper).delete()
                    Question_type_numerical.objects.filter(test_paper=test_paper).delete()
                    test_paper.total_questions = len(sheet_data)
                    test_paper.save()
                
                # Process questions
                for index, row in sheet_data.iterrows():
                    try:
                        question_type = str(row['Question Type']).strip()
                        question_number = int(row['Question Number'])
                        question_text = str(row['Question Text']).strip()
                        
                        if not question_text:
                            errors.append(f"Sheet '{sheet_name}', Row {index + 2}: Empty question text")
                            continue
                        
                        question_image = None
                        if 'Question Image' in row and pd.notna(row['Question Image']):
                            question_image = str(row['Question Image']).strip()
                        
                        marks = float(row.get('Marks', 1.0)) if pd.notna(row.get('Marks')) else 1.0
                        negative_marks = float(row.get('Negative Marks', 0.0)) if pd.notna(row.get('Negative Marks')) else 0.0
                        topic = str(row.get('Topic', '')).strip() if pd.notna(row.get('Topic')) else None
                        
                        if question_type == 'MCQ':
                            if not all(col in row for col in ['Option A', 'Option B', 'Option C', 'Option D', 'Correct Option']):
                                errors.append(f"Sheet '{sheet_name}', Row {index + 2}: MCQ missing required columns")
                                continue
                            
                            Question_type_mcq.objects.create(
                                test_paper=test_paper,
                                question_number=question_number,
                                question_text=question_text,
                                question_image=question_image if question_image else None,
                                option_a=str(row['Option A']).strip(),
                                option_b=str(row['Option B']).strip(),
                                option_c=str(row['Option C']).strip(),
                                option_d=str(row['Option D']).strip(),
                                correct_option=str(row['Correct Option']).strip().upper(),
                                marks=marks,
                                negative_marks=negative_marks,
                                topic=topic or None
                            )
                            created_count += 1
                        
                        elif question_type == 'MSQ':
                            if not all(col in row for col in ['Option A', 'Option B', 'Option C', 'Option D', 'Correct Options']):
                                errors.append(f"Sheet '{sheet_name}', Row {index + 2}: MSQ missing required columns")
                                continue
                            
                            Question_type_msq.objects.create(
                                test_paper=test_paper,
                                question_number=question_number,
                                question_text=question_text,
                                question_image=question_image if question_image else None,
                                option_a=str(row['Option A']).strip(),
                                option_b=str(row['Option B']).strip(),
                                option_c=str(row['Option C']).strip(),
                                option_d=str(row['Option D']).strip(),
                                correct_options=str(row['Correct Options']).strip().upper(),
                                marks=marks,
                                negative_marks=negative_marks,
                                topic=topic or None
                            )
                            created_count += 1
                        
                        elif question_type == 'Numerical':
                            if 'Correct Answer' not in row:
                                errors.append(f"Sheet '{sheet_name}', Row {index + 2}: Numerical question missing Correct Answer")
                                continue
                            
                            try:
                                correct_answer = float(row['Correct Answer'])
                            except (ValueError, TypeError):
                                errors.append(f"Sheet '{sheet_name}', Row {index + 2}: Invalid Correct Answer value")
                                continue
                            
                            Question_type_numerical.objects.create(
                                test_paper=test_paper,
                                question_number=question_number,
                                question_text=question_text,
                                question_image=question_image if question_image else None,
                                correct_answer=correct_answer,
                                marks=marks,
                                negative_marks=negative_marks,
                                topic=topic or None
                            )
                            created_count += 1
                        
                        else:
                            errors.append(f"Sheet '{sheet_name}', Row {index + 2}: Unknown question type '{question_type}'")
                    
                    except Exception as e:
                        errors.append(f"Sheet '{sheet_name}', Row {index + 2}: {str(e)}")
        
        except Exception as e:
            return JsonResponse({'success': False, 'error': f'Error reading Excel file: {str(e)}'}, status=500)
        
        finally:
            # Clean up temporary file
            try:
                default_storage.delete(file_path)
            except:
                pass
        
        return JsonResponse({
            'success': True,
            'created_count': created_count,
            'errors': errors,
            'message': f'Successfully created {created_count} questions. {len(errors)} errors found.' if errors else f'Successfully created {created_count} questions.'
        })
    
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


class ManageExamsView(LoginRequiredMixin, TemplateView):
    """Page to view and manage exams"""
    template_name = 'teacher/manage_exams.html'
    
    def dispatch(self, request, *args, **kwargs):
        try:
            request.user.teacherprofile
        except:
            return redirect('/login/')
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['exams'] = Exam.objects.all().order_by('-id')
        return context
