from django.db import models
from django.contrib.auth.models import User
from exam.models import Exam
import json


class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    course_enrolled = models.CharField(max_length=100, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    is_premium = models.BooleanField(default=False)
    
    def __str__(self):
        return self.user.username


class ExamAttempt(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='exam_attempts')
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='attempts')
    attempt_number = models.PositiveIntegerField()
    score = models.FloatField()
    date_taken = models.DateTimeField(auto_now_add=True)
    time_taken = models.DurationField()
    total_marks = models.FloatField(default=0)
    percentage = models.FloatField(default=0)
    answers_json = models.TextField(default='{}')  # Store all answers as JSON
    time_spent_json = models.TextField(default='{}')  # Store time spent per question as JSON

    class Meta:
        unique_together = ['student', 'exam', 'attempt_number']
        ordering = ['-date_taken']

    def __str__(self):
        return f"{self.student.user.username} - {self.exam.name} - Attempt {self.attempt_number}"
    
    def get_answers(self):
        """Return answers as dictionary"""
        try:
            return json.loads(self.answers_json)
        except:
            return {}
    
    def get_time_spent(self):
        """Return time spent per question as dictionary"""
        try:
            return json.loads(self.time_spent_json)
        except:
            return {}


class QuestionAnswer(models.Model):
    """Individual question answer with detailed tracking"""
    attempt = models.ForeignKey(ExamAttempt, on_delete=models.CASCADE, related_name='question_answers')
    question_id = models.IntegerField()
    question_type = models.CharField(max_length=20, choices=[
        ('mcq', 'MCQ'),
        ('msq', 'MSQ'),
        ('numerical', 'Numerical')
    ])
    user_answer = models.TextField(null=True, blank=True)
    is_correct = models.BooleanField(default=False)
    marks_obtained = models.FloatField(default=0)
    time_spent_seconds = models.IntegerField(default=0)
    topic = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        ordering = ['question_id']
    
    def __str__(self):
        return f"Q{self.question_id} - Attempt {self.attempt.attempt_number}"
