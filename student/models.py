from django.db import models
from django.contrib.auth.models import User
from exam.models import Exam


class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    course_enrolled = models.CharField(max_length=100, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return self.user.username


class ExamAttempt(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='exam_attempts')
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='attempts')
    attempt_number = models.PositiveIntegerField()
    score = models.FloatField()
    date_taken = models.DateTimeField(auto_now_add=True)
    time_taken = models.DurationField()

    class Meta:
        unique_together = ['student', 'exam', 'attempt_number']
        ordering = ['-date_taken']

    def __str__(self):
        return f"{self.student.user.username} - {self.exam.name} - Attempt {self.attempt_number}"
