from django.db import models

# Create your models here.
class Exam(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    total_marks = models.FloatField()
    duration = models.DurationField()
    language = models.CharField(max_length=50, default='English')
    description = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return self.name

class TestPaper(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='test_papers')
    paper_code = models.CharField(max_length=20, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    total_questions = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.exam.name} - Paper {self.paper_code}"

class Question_type_mcq(models.Model):
    test_paper = models.ForeignKey(TestPaper, on_delete=models.CASCADE, related_name='mcq_questions')
    question_number = models.IntegerField()  # to maintain order of questions
    question_text = models.TextField()
    question_image = models.ImageField(upload_to='question_images/', null=True, blank=True)
    option_a = models.CharField(max_length=255)
    option_b = models.CharField(max_length=255)
    option_c = models.CharField(max_length=255)
    option_d = models.CharField(max_length=255)
    correct_option = models.CharField(max_length=1, choices=[('A', 'Option A'), ('B', 'Option B'), ('C', 'Option C'), ('D', 'Option D')])
    marks = models.FloatField(default=1.0)
    negative_marks = models.FloatField(default=0.0)
    topic = models.CharField(max_length=100, null=True, blank=True)
    
    class Meta:
        ordering = ['question_number']
    
    def __str__(self):
        return f"MCQ {self.question_number}: {self.question_text[:50]}..."

class Question_type_msq(models.Model):
    test_paper = models.ForeignKey(TestPaper, on_delete=models.CASCADE, related_name='msq_questions')
    question_number = models.IntegerField()
    question_text = models.TextField()
    question_image = models.ImageField(upload_to='question_images/', null=True, blank=True)
    option_a = models.CharField(max_length=255)
    option_b = models.CharField(max_length=255)
    option_c = models.CharField(max_length=255)
    option_d = models.CharField(max_length=255)
    correct_options = models.CharField(max_length=4)
    marks = models.FloatField(default=1.0)
    negative_marks = models.FloatField(default=0.0)
    topic = models.CharField(max_length=100, null=True, blank=True)
    
    class Meta:
        ordering = ['question_number']
    
    def __str__(self):
        return f"MSQ {self.question_number}: {self.question_text[:50]}..."

class Question_type_numerical(models.Model):
    test_paper = models.ForeignKey(TestPaper, on_delete=models.CASCADE, related_name='numerical_questions')
    question_number = models.IntegerField()
    question_text = models.TextField()
    question_image = models.ImageField(upload_to='question_images/', null=True, blank=True)
    correct_answer = models.FloatField()
    marks = models.FloatField(default=1.0)
    negative_marks = models.FloatField(default=0.0)
    topic = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        ordering = ['question_number']

    def __str__(self):
        return f"Numerical {self.question_number}: {self.question_text[:50]}..."