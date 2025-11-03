# Exam Paper Import Template Guide

This guide explains how to use the Excel template to import exam papers into the system.

## Generating the Template

Run the Python script to generate the template:

```bash
python generate_exam_template.py
```

This will create `exam_import_template.xlsx` in the current directory.

## Template Structure

The Excel file contains multiple sheets:

### 1. Exam_Info Sheet (Required)
Contains basic exam information:

| Column | Description | Example | Required |
|--------|-------------|---------|----------|
| Exam Name | Name of the exam | "Mathematics Midterm Exam" | Yes |
| Description | Exam description | "Midterm covering algebra and calculus" | No |
| Duration (minutes) | Exam duration in minutes | 90 | Yes |
| Total Marks | Total marks for the exam | 100 | No |
| Language | Exam language | "English" or "Hindi" | No |

**Note:** Only one row is required in this sheet.

### 2. Test Paper Sheets (One per test paper)
Each test paper gets its own sheet. Name the sheet with a unique paper code (e.g., "PAPER001", "PAPER002", "SET1", "SET2").

#### Column Structure

| Column | Description | MCQ | MSQ | Numerical | Required |
|--------|-------------|-----|-----|-----------|----------|
| Question Type | Type of question | "MCQ" | "MSQ" | "Numerical" | Yes |
| Question Number | Sequential number | Any integer | Any integer | Any integer | Yes |
| Question Text | The question statement | Required | Required | Required | Yes |
| Question Image | Image path (if any) | Optional | Optional | Optional | No |
| Option A | First option | Required | Required | Leave empty | Yes* |
| Option B | Second option | Required | Required | Leave empty | Yes* |
| Option C | Third option | Required | Required | Leave empty | Yes* |
| Option D | Fourth option | Required | Required | Leave empty | Yes* |
| Correct Option | Correct answer (MCQ) | A/B/C/D | Leave empty | Leave empty | Yes* |
| Correct Options | Correct answers (MSQ) | Leave empty | e.g., "AB", "ABC", "ABCD" | Leave empty | Yes* |
| Correct Answer | Correct answer (Numerical) | Leave empty | Leave empty | Numeric value | Yes* |
| Marks | Marks for correct answer | Default: 1.0 | Default: 1.0 | Default: 1.0 | No |
| Negative Marks | Marks deducted for wrong answer | Default: 0.0 | Default: 0.0 | Default: 0.0 | No |
| Topic | Question topic/category | Optional | Optional | Optional | No |

*Required based on question type

## Question Type Guidelines

### MCQ (Multiple Choice Question)
- **Question Type**: Must be exactly "MCQ"
- **Options**: Fill all four options (A, B, C, D)
- **Correct Option**: Exactly one letter - "A", "B", "C", or "D"
- **Correct Options**: Leave empty
- **Correct Answer**: Leave empty

**Example:**
```
Question Type: MCQ
Question Text: What is 2 + 2?
Option A: 3
Option B: 4
Option C: 5
Option D: 6
Correct Option: B
```

### MSQ (Multiple Select Question)
- **Question Type**: Must be exactly "MSQ"
- **Options**: Fill all four options (A, B, C, D)
- **Correct Options**: Combination of letters without spaces, e.g., "AB", "ABC", "ABCD", "BD"
- **Correct Option**: Leave empty
- **Correct Answer**: Leave empty

**Example:**
```
Question Type: MSQ
Question Text: Which are prime numbers?
Option A: 2
Option B: 3
Option C: 4
Option D: 5
Correct Options: ABD
```

### Numerical
- **Question Type**: Must be exactly "Numerical"
- **Options**: Leave all four options empty
- **Correct Answer**: Numeric value (can be decimal)
- **Correct Option**: Leave empty
- **Correct Options**: Leave empty

**Example:**
```
Question Type: Numerical
Question Text: Solve for x: 2x + 5 = 13
Correct Answer: 4
```

## Import Process

1. Generate the template using `generate_exam_template.py`
2. Fill in the `Exam_Info` sheet with your exam details
3. Create test paper sheets (rename them with your paper codes)
4. Fill in questions following the column structure
5. Save the Excel file
6. Use the import function in the admin panel or API

## Best Practices

1. **Paper Codes**: Use unique, descriptive names (e.g., "PAPER001", "SET_A", "MODEL1")
2. **Question Numbers**: Start from 1 and use sequential numbering
3. **Question Text**: Be clear and complete - avoid abbreviations that might confuse
4. **Marks**: Ensure marks and negative marks are reasonable (negative marks typically ≤ marks)
5. **Topics**: Use consistent topic names for better analytics (e.g., "Algebra", "Calculus", "Trigonometry")
6. **Images**: If using images, provide relative paths or full paths accessible by the system

## Common Errors to Avoid

1. ❌ Using wrong question type spelling (use exactly "MCQ", "MSQ", or "Numerical")
2. ❌ Filling wrong columns for question type (e.g., filling "Correct Answer" for MCQ)
3. ❌ Missing required options for MCQ/MSQ
4. ❌ Invalid correct option values (must be A/B/C/D for MCQ, combination for MSQ)
5. ❌ Non-numeric values in "Correct Answer" for Numerical questions
6. ❌ Missing question numbers or non-sequential numbering

## Example File Structure

```
exam_import_template.xlsx
├── Exam_Info (1 row)
├── PAPER001 (Multiple questions: MCQ, MSQ, Numerical)
├── PAPER002 (Multiple questions: MCQ, Numerical)
└── PAPER003 (Multiple questions: All types)
```

## Support

If you encounter issues:
1. Verify column names match exactly (case-sensitive)
2. Check that question types are spelled correctly
3. Ensure all required fields are filled for each question type
4. Validate numeric fields contain valid numbers
5. Review the sample data in the generated template

