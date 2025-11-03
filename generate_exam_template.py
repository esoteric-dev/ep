"""
Script to generate an Excel template for importing exam papers.
Run this script to create a template file: exam_import_template.xlsx
"""
import pandas as pd
from datetime import timedelta

def generate_exam_template():
    """Generate an Excel template for importing exam papers"""
    
    # Create Excel writer object
    output_file = 'exam_import_template.xlsx'
    writer = pd.ExcelWriter(output_file, engine='openpyxl')
    
    # Sheet 1: Exam_Info
    exam_info_data = {
        'Exam Name': ['Mathematics Midterm Exam'],
        'Description': ['Midterm examination covering algebra and calculus topics'],
        'Duration (minutes)': [90],
        'Total Marks': [100],
        'Language': ['English']
    }
    exam_info_df = pd.DataFrame(exam_info_data)
    exam_info_df.to_excel(writer, sheet_name='Exam_Info', index=False)
    
    # Sheet 2: Test Paper 1 - Sample questions
    paper1_data = {
        'Question Type': ['MCQ', 'MSQ', 'Numerical', 'MCQ'],
        'Question Number': [1, 2, 3, 4],
        'Question Text': [
            'What is the derivative of x^2?',
            'Which of the following are prime numbers?',
            'Solve for x: 2x + 5 = 13',
            'What is the value of sin(90°)?'
        ],
        'Question Image': ['', '', '', ''],  # Leave empty or provide image path
        'Option A': [
            '2x',
            '2',
            '',
            '0'
        ],
        'Option B': [
            'x',
            '3',
            '',
            '1'
        ],
        'Option C': [
            '2',
            '4',
            '',
            '0.5'
        ],
        'Option D': [
            'x^2',
            '5',
            '',
            '-1'
        ],
        'Correct Option': ['A', '', '', 'B'],  # For MCQ: A, B, C, or D
        'Correct Options': ['', 'ABD', '', ''],  # For MSQ: e.g., 'AB', 'ABC', 'ABCD'
        'Correct Answer': ['', '', 4, ''],  # For Numerical: numeric value
        'Marks': [2.0, 3.0, 2.0, 1.0],
        'Negative Marks': [0.5, 1.0, 0.5, 0.25],
        'Topic': ['Calculus', 'Number Theory', 'Algebra', 'Trigonometry']
    }
    paper1_df = pd.DataFrame(paper1_data)
    paper1_df.to_excel(writer, sheet_name='PAPER001', index=False)
    
    # Sheet 3: Test Paper 2 - More examples
    paper2_data = {
        'Question Type': ['MCQ', 'Numerical'],
        'Question Number': [1, 2],
        'Question Text': [
            'What is the integral of 1/x?',
            'Find the value of log(100)'
        ],
        'Question Image': ['', ''],
        'Option A': ['x', ''],
        'Option B': ['ln(x)', ''],
        'Option C': ['1/x', ''],
        'Option D': ['x^2', ''],
        'Correct Option': ['B', ''],
        'Correct Options': ['', ''],
        'Correct Answer': ['', 2.0],
        'Marks': [2.0, 1.0],
        'Negative Marks': [0.5, 0.25],
        'Topic': ['Calculus', 'Logarithms']
    }
    paper2_df = pd.DataFrame(paper2_data)
    paper2_df.to_excel(writer, sheet_name='PAPER002', index=False)
    
    # Save the file
    writer.close()
    
    print(f"Excel template generated successfully: {output_file}")
    print("\nTemplate Structure:")
    print("- Sheet 1: 'Exam_Info' - Contains exam details (one row)")
    print("- Sheet 2+: Test paper sheets (named with paper code like 'PAPER001', 'PAPER002', etc.)")
    print("\nColumn Guidelines:")
    print("- Question Type: Must be 'MCQ', 'MSQ', or 'Numerical'")
    print("- Question Number: Sequential number for ordering questions")
    print("- Question Text: The question statement")
    print("- Question Image: Leave empty or provide path to image file")
    print("- Option A/B/C/D: Required for MCQ and MSQ, leave empty for Numerical")
    print("- Correct Option: For MCQ only, use A, B, C, or D")
    print("- Correct Options: For MSQ only, use combinations like 'AB', 'ABC', 'ABCD'")
    print("- Correct Answer: For Numerical only, provide numeric value")
    print("- Marks: Positive marks for correct answer (default: 1.0)")
    print("- Negative Marks: Marks deducted for wrong answer (default: 0.0)")
    print("- Topic: Optional topic/category name")

if __name__ == '__main__':
    try:
        generate_exam_template()
    except ImportError:
        print("Error: Please install required packages:")
        print("pip install pandas openpyxl")
    except Exception as e:
        print(f"Error generating template: {e}")

