from django.shortcuts import render, get_object_or_404, redirect
from django.conf import settings
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework import generics
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.utils import timezone
from django.db.models import Q
from datetime import timedelta
import json
from exam.models import Exam, TestPaper, Question_type_mcq, Question_type_msq, Question_type_numerical
from student.models import ExamAttempt, QuestionAnswer, StudentProfile
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


class CoursesView(TemplateView):
    template_name = 'courses.html'

    def dispatch(self, request, *args, **kwargs):
        # Publicly accessible: allow viewing courses without login,
        # but hydrate user from JWT if present so is_authenticated works in template
        jwt_auth = JWTAuthentication()
        try:
            validated_token = jwt_auth.get_validated_token(request.COOKIES.get('jwt', ''))
            request.user = jwt_auth.get_user(validated_token)
        except Exception:
            pass
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['courses'] = Exam.objects.all().order_by('name')
        return context


class CourseExamsView(TemplateView):
    template_name = 'course_exams.html'

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
        exam_id = self.kwargs.get('exam_id')
        exam = get_object_or_404(Exam, id=exam_id)
        test_papers = exam.test_papers.all().order_by('-is_active', 'id') if hasattr(exam, 'test_papers') else []
        context['exam'] = exam
        context['test_papers'] = test_papers
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
                    'uid': f"mcq-{q.id}",
                    'type': 'mcq',
                    'number': q.question_number,
                    'text': q.question_text,
                    'image': q.question_image.url if q.question_image else None,
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
                    'uid': f"msq-{q.id}",
                    'type': 'msq',
                    'number': q.question_number,
                    'text': q.question_text,
                    'image': q.question_image.url if q.question_image else None,
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
                    'uid': f"numerical-{q.id}",
                    'type': 'numerical',
                    'number': q.question_number,
                    'text': q.question_text,
                    'image': q.question_image.url if q.question_image else None,
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
        
        # Include topics in questions for results analysis
        for q in context['questions']:
            if q['type'] == 'mcq':
                mcq_obj = Question_type_mcq.objects.get(id=q['id'])
                q['topic'] = mcq_obj.topic or 'General'
            elif q['type'] == 'msq':
                msq_obj = Question_type_msq.objects.get(id=q['id'])
                q['topic'] = msq_obj.topic or 'General'
            elif q['type'] == 'numerical':
                num_obj = Question_type_numerical.objects.get(id=q['id'])
                q['topic'] = num_obj.topic or 'General'
        
        # Serialize questions as JSON for frontend
        context['questions_json'] = json.dumps(context['questions'])

        # Ads config: show only for non-premium students
        is_premium = False
        try:
            is_premium = bool(StudentProfile.objects.filter(user=self.request.user).values_list('is_premium', flat=True).first())
        except Exception:
            is_premium = False
        context['show_ads'] = (not is_premium)
        context['adsense_client'] = getattr(settings, 'ADSENSE_CLIENT', '')
        context['adsense_slot_exam'] = getattr(settings, 'ADSENSE_SLOT_EXAM', '')
        
        return context


@csrf_exempt
def submit_exam(request, exam_id):
    """Handle exam submission and calculate results"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    # Authenticate user
    jwt_auth = JWTAuthentication()
    try:
        validated_token = jwt_auth.get_validated_token(request.COOKIES.get('jwt', ''))
        user = jwt_auth.get_user(validated_token)
    except Exception:
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'Authentication required'}, status=401)
        user = request.user
    
    try:
        exam = get_object_or_404(Exam, id=exam_id)
        student_profile = user.studentprofile
        
        # Get submission data
        data = json.loads(request.body)
        answers = data.get('answers', {})
        time_spent = data.get('time_spent', {})
        start_time = data.get('start_time')
        total_time = data.get('total_time', 0)  # in seconds
        
        # Calculate attempt number
        existing_attempts = ExamAttempt.objects.filter(student=student_profile, exam=exam).count()
        attempt_number = existing_attempts + 1
        
        # Get test paper and questions
        test_paper = exam.test_papers.filter(is_active=True).first()
        if not test_paper:
            return JsonResponse({'error': 'No active test paper found'}, status=400)
        
        # Collect all questions
        all_mcq = Question_type_mcq.objects.filter(test_paper=test_paper)
        all_msq = Question_type_msq.objects.filter(test_paper=test_paper)
        all_numerical = Question_type_numerical.objects.filter(test_paper=test_paper)
        
        mcq_questions = {q.id: q for q in all_mcq}
        msq_questions = {q.id: q for q in all_msq}
        numerical_questions = {q.id: q for q in all_numerical}
        
        # Calculate scores
        total_score = 0
        total_marks = 0
        question_answers = []
        processed_question_ids = set()
        
        # Process answered questions
        for raw_key, answer in answers.items():
            # Support keys in format "type-id" (preferred) or plain numeric id (legacy)
            q_type = None
            q_id = None
            uid = str(raw_key)
            if '-' in uid:
                parts = uid.split('-', 1)
                q_type = parts[0]
                try:
                    q_id = int(parts[1])
                except ValueError:
                    continue
            else:
                try:
                    q_id = int(uid)
                except ValueError:
                    continue
            question_obj = None
            correct_answer = None
            is_correct = False
            marks_obtained = 0
            
            if q_id in mcq_questions:
                q_type = 'mcq'
                question_obj = mcq_questions[q_id]
                correct_answer = question_obj.correct_option
                is_correct = (answer == correct_answer)
                if is_correct:
                    marks_obtained = question_obj.marks
                else:
                    marks_obtained = -question_obj.negative_marks
            elif q_id in msq_questions:
                q_type = 'msq'
                question_obj = msq_questions[q_id]
                correct_answer = question_obj.correct_options
                # For MSQ, check if answer matches (assuming comma-separated)
                user_selected = sorted(answer.split(',')) if answer else []
                correct_selected = sorted(list(correct_answer))
                is_correct = (user_selected == correct_selected)
                if is_correct:
                    marks_obtained = question_obj.marks
                else:
                    marks_obtained = -question_obj.negative_marks
            elif q_id in numerical_questions:
                q_type = 'numerical'
                question_obj = numerical_questions[q_id]
                correct_answer = question_obj.correct_answer
                try:
                    user_ans = float(answer) if answer else None
                    is_correct = (user_ans is not None and abs(user_ans - correct_answer) < 0.01)
                except:
                    is_correct = False
                if is_correct:
                    marks_obtained = question_obj.marks
                else:
                    marks_obtained = -question_obj.negative_marks
            
            if question_obj:
                total_marks += question_obj.marks
                total_score += marks_obtained
                topic = getattr(question_obj, 'topic', None) or 'General'
                processed_question_ids.add(q_id)
                
                question_answers.append({
                    'question_id': q_id,
                    'question_type': q_type,
                    'user_answer': answer,
                    'is_correct': is_correct,
                    'marks_obtained': marks_obtained,
                    'time_spent': time_spent.get(uid, time_spent.get(str(q_id), 0)),
                    'topic': topic
                })
        
        # Process unanswered questions
        for q_id, question_obj in mcq_questions.items():
            if q_id not in processed_question_ids:
                total_marks += question_obj.marks
                topic = getattr(question_obj, 'topic', None) or 'General'
                question_answers.append({
                    'question_id': q_id,
                    'question_type': 'mcq',
                    'user_answer': None,
                    'is_correct': False,
                    'marks_obtained': 0,
                    'time_spent': time_spent.get(f'mcq-{q_id}', time_spent.get(str(q_id), 0)),
                    'topic': topic
                })
        
        for q_id, question_obj in msq_questions.items():
            if q_id not in processed_question_ids:
                total_marks += question_obj.marks
                topic = getattr(question_obj, 'topic', None) or 'General'
                question_answers.append({
                    'question_id': q_id,
                    'question_type': 'msq',
                    'user_answer': None,
                    'is_correct': False,
                    'marks_obtained': 0,
                    'time_spent': time_spent.get(f'msq-{q_id}', time_spent.get(str(q_id), 0)),
                    'topic': topic
                })
        
        for q_id, question_obj in numerical_questions.items():
            if q_id not in processed_question_ids:
                total_marks += question_obj.marks
                topic = getattr(question_obj, 'topic', None) or 'General'
                question_answers.append({
                    'question_id': q_id,
                    'question_type': 'numerical',
                    'user_answer': None,
                    'is_correct': False,
                    'marks_obtained': 0,
                    'time_spent': time_spent.get(f'numerical-{q_id}', time_spent.get(str(q_id), 0)),
                    'topic': topic
                })
        
        # Calculate percentage
        percentage = (total_score / total_marks * 100) if total_marks > 0 else 0
        
        # Create exam attempt
        time_taken = timedelta(seconds=total_time)
        attempt = ExamAttempt.objects.create(
            student=student_profile,
            exam=exam,
            attempt_number=attempt_number,
            score=total_score,
            total_marks=total_marks,
            percentage=percentage,
            time_taken=time_taken,
            answers_json=json.dumps(answers),
            time_spent_json=json.dumps(time_spent)
        )
        
        # Create question answer records
        for qa_data in question_answers:
            QuestionAnswer.objects.create(
                attempt=attempt,
                question_id=qa_data['question_id'],
                question_type=qa_data['question_type'],
                user_answer=qa_data['user_answer'],
                is_correct=qa_data['is_correct'],
                marks_obtained=qa_data['marks_obtained'],
                time_spent_seconds=qa_data['time_spent'],
                topic=qa_data['topic']
            )
        
        return JsonResponse({
            'success': True,
            'attempt_id': attempt.id,
            'redirect_url': f'/exam/{exam_id}/results/{attempt.id}/'
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


class ExamResultsView(TemplateView):
    template_name = 'exam_results.html'
    
    def dispatch(self, request, *args, **kwargs):
        # Try JWT authentication first
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
        exam_id = self.kwargs.get('exam_id')
        attempt_id = self.kwargs.get('attempt_id')
        
        attempt = get_object_or_404(ExamAttempt, id=attempt_id, exam_id=exam_id)
        
        # Verify the attempt belongs to the current user
        if attempt.student.user != self.request.user:
            from django.core.exceptions import PermissionDenied
            raise PermissionDenied
        
        # Get question answers
        question_answers = QuestionAnswer.objects.filter(attempt=attempt).order_by('question_id')
        
        # Calculate topic-wise statistics
        topic_stats = {}
        for qa in question_answers:
            topic = qa.topic or 'General'
            if topic not in topic_stats:
                topic_stats[topic] = {
                    'total': 0,
                    'correct': 0,
                    'incorrect': 0,
                    'unanswered': 0,
                    'marks_obtained': 0,
                    'total_marks': 0,
                    'time_spent': 0,
                    'questions': []
                }
            
            topic_stats[topic]['total'] += 1
            # Calculate total marks for this topic (sum of marks from all questions in this topic)
            topic_stats[topic]['total_marks'] += attempt.exam.total_marks / len(question_answers) if question_answers else 0
            topic_stats[topic]['time_spent'] += qa.time_spent_seconds
            
            if qa.user_answer:
                if qa.is_correct:
                    topic_stats[topic]['correct'] += 1
                else:
                    topic_stats[topic]['incorrect'] += 1
            else:
                topic_stats[topic]['unanswered'] += 1
            
            topic_stats[topic]['marks_obtained'] += qa.marks_obtained
            topic_stats[topic]['questions'].append(qa)
        
        # Calculate average time per question
        total_time = sum(qa.time_spent_seconds for qa in question_answers)
        avg_time = total_time / len(question_answers) if question_answers else 0
        
        # Identify weak topics (topics with low accuracy)
        weak_topics = []
        for topic, stats in topic_stats.items():
            accuracy = (stats['correct'] / stats['total'] * 100) if stats['total'] > 0 else 0
            if accuracy < 50:  # Less than 50% accuracy
                weak_topics.append({
                    'topic': topic,
                    'accuracy': round(accuracy, 1),
                    'correct': stats['correct'],
                    'total': stats['total']
                })
        
        # Sort weak topics by accuracy
        weak_topics.sort(key=lambda x: x['accuracy'])
        
        # Identify missed topics (topics with unanswered questions)
        missed_topics = []
        for topic, stats in topic_stats.items():
            if stats['unanswered'] > 0:
                missed_topics.append({
                    'topic': topic,
                    'unanswered': stats['unanswered'],
                    'total': stats['total']
                })
        
        # Get time spent dictionary
        time_spent = attempt.get_time_spent()
        
        context['attempt'] = attempt
        context['exam'] = attempt.exam
        context['question_answers'] = question_answers
        context['topic_stats'] = topic_stats
        context['avg_time_per_question'] = round(avg_time, 1)
        context['weak_topics'] = weak_topics
        context['missed_topics'] = missed_topics
        context['total_questions'] = len(question_answers)
        context['answered_count'] = sum(1 for qa in question_answers if qa.user_answer)
        context['correct_count'] = sum(1 for qa in question_answers if qa.is_correct)
        context['incorrect_count'] = sum(1 for qa in question_answers if qa.user_answer and not qa.is_correct)

        # Ads config: show only for non-premium students
        is_premium = False
        try:
            is_premium = bool(StudentProfile.objects.filter(user=self.request.user).values_list('is_premium', flat=True).first())
        except Exception:
            is_premium = False
        context['show_ads'] = (not is_premium)
        context['adsense_client'] = getattr(settings, 'ADSENSE_CLIENT', '')
        context['adsense_slot_results'] = getattr(settings, 'ADSENSE_SLOT_RESULTS', '')
        
        return context
