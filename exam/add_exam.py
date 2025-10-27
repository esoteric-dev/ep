import pandas as pd

from exam.models import (
    Question_type_numerical,
    Question_type_mcq,
    Question_type_msq,
    TestPaper,
    Exam,
)

def add_exam_from_excel(file_path):
    # Read the Excel file
    df = pd.read_excel(file_path, sheet_name=None)

    # Extract exam details
    exam_info = df['Exam_Info'].iloc[0]
    exam_name = exam_info['Exam Name']
    exam_description = exam_info['Description']
    exam_duration = exam_info['Duration (minutes)']
    
    # Create Exam instance
    exam = Exam.objects.create(
        name=exam_name,
        description=exam_description,
        duration=exam_duration
    )

    # Process each test paper sheet
    for sheet_name, sheet_data in df.items():
        if sheet_name == 'Exam_Info':
            continue
        
        # Create TestPaper instance
        test_paper = TestPaper.objects.create(
            exam=exam,
            paper_code=sheet_name,
            total_questions=len(sheet_data)
        )

        # Process questions
        for index, row in sheet_data.iterrows():
            question_type = row['Question Type']
            question_number = row['Question Number']
            question_text = row['Question Text']
            question_image = row.get('Question Image', None)
            marks = row.get('Marks', 1.0)
            negative_marks = row.get('Negative Marks', 0.0)

            if question_type == 'MCQ':
                Question_type_mcq.objects.create(
                    test_paper=test_paper,
                    question_number=question_number,
                    question_text=question_text,
                    question_image=question_image,
                    option_a=row['Option A'],
                    option_b=row['Option B'],
                    option_c=row['Option C'],
                    option_d=row['Option D'],
                    correct_option=row['Correct Option'],
                    marks=marks,
                    negative_marks=negative_marks
                )
            elif question_type == 'MSQ':
                Question_type_msq.objects.create(
                    test_paper=test_paper,
                    question_number=question_number,
                    question_text=question_text,
                    question_image=question_image,
                    option_a=row['Option A'],
                    option_b=row['Option B'],
                    option_c=row['Option C'],
                    option_d=row['Option D'],
                    correct_options=row['Correct Options'],
                    marks=marks,
                    negative_marks=negative_marks
                )
            elif question_type == 'Numerical':
                Question_type_numerical.objects.create(
                    test_paper=test_paper,
                    question_number=question_number,
                    question_text=question_text,
                    question_image=question_image,
                    correct_answer=row['Correct Answer'],
                    marks=marks,
                    negative_marks=negative_marks
                )