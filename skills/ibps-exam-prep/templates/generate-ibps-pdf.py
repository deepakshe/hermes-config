#!/usr/bin/env python3
"""
Generate IBPS PO/CLERK Practice Questions PDF from CSV files.
Uses fpdf2 library to create 11-page practice set with all 150 questions.
"""

from fpdf import FPDF
import csv

# Configuration
BASE = "C:/Users/admin/Downloads/"
QUESTION_COLOR = (0, 0, 0)  # Black
ANSWER_COLOR = (0, 100, 0)  # Dark green for answers
QUESTION_FONTS = [("Arial", "B", 9), ("Arial", "", 9)]
ANSWER_FONTS = [("Arial", "I", 8), ("Arial", "", 8)]


def write_question_row(pdf, question_num, question_text, options, correct_answer, topic):
    """Write a single question row to the PDF."""
    correct_option = chr(65 + int(correct_answer))
    
    # Question text
    pdf.multi_cell(0, 5, f"Q{question_num}: {question_text}")
    
    # Options
    pdf.set_font("Arial", "", 8)
    for j, opt in enumerate(options):
        pdf.cell(25, 5, f"  {chr(65+j)}.", ln=0)
        pdf.cell(0, 5, f" {opt}", ln=1)
    pdf.ln(2)
    
    # Answer line
    pdf.set_font("Arial", "I", 8)
    pdf.cell(0, 5, f"Answer: Option {correct_option} | Topic: {topic}", ln=1)
    pdf.ln(3)


def generate_ibps_pdf(csv_english, csv_quant, csv_reasoning, output_path):
    """Generate the complete IBPS practice questions PDF."""
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # ===== ENGLISH SECTION =====
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "IBPS PO/CLERK EXAM: PRACTICE QUESTIONS", ln=1, align="C")
    pdf.set_font("Arial", "I", 12)
    pdf.cell(0, 10, "English Language - Error Detection", ln=1, align="C")
    pdf.ln(5)
    
    with open(csv_english, "r") as f:
        questions = list(csv.DictReader(f))
    
    pdf.set_font("Arial", "B", 10)
    pdf.cell(0, 8, f"Total Questions: {len(questions)}", ln=1)
    pdf.ln(3)
    
    pdf.set_font("Arial", "", 9)
    for i, q in enumerate(questions, 1):
        question_text = q["questionText"]
        options = q["options"].split("|")
        correct = int(q["correctAnswer"])
        correct_option = chr(65 + correct)
        
        pdf.multi_cell(0, 5, f"Q{i}: {question_text}")
        pdf.set_font("Arial", "", 8)
        for j, opt in enumerate(options):
            pdf.cell(25, 5, f"  {chr(65+j)}.", ln=0)
        pdf.ln()
        pdf.set_font("Arial", "I", 8)
        pdf.cell(0, 5, f"Answer: Option {correct_option} | Topic: {q['topic']}", ln=1)
        pdf.ln(2)
    
    # ===== QUANTITATIVE SECTION =====
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "IBPS PO/CLERK EXAM: PRACTICE QUESTIONS", ln=1, align="C")
    pdf.set_font("Arial", "I", 12)
    pdf.cell(0, 10, "Quantitative Aptitude", ln=1, align="C")
    pdf.ln(5)
    
    with open(csv_quant, "r") as f:
        questions = list(csv.DictReader(f))
    
    pdf.set_font("Arial", "B", 10)
    pdf.cell(0, 8, f"Total Questions: {len(questions)}", ln=1)
    pdf.ln(3)
    
    pdf.set_font("Arial", "", 9)
    for i, q in enumerate(questions, 1):
        question_text = q["questionText"]
        options = q["options"].split("|")
        correct = int(q["correctAnswer"])
        correct_option = chr(65 + correct)
        
        pdf.multi_cell(0, 5, f"Q{i}: {question_text}")
        pdf.set_font("Arial", "", 8)
        for j, opt in enumerate(options):
            pdf.cell(25, 5, f"  {chr(65+j)}.", ln=0)
        pdf.ln()
        pdf.set_font("Arial", "I", 8)
        pdf.cell(0, 5, f"Answer: Option {correct_option} | Topic: {q['topic']}", ln=1)
        pdf.ln(2)
    
    # ===== REASONING SECTION =====
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "IBPS PO/CLERK EXAM: PRACTICE QUESTIONS", ln=1, align="C")
    pdf.set_font("Arial", "I", 12)
    pdf.cell(0, 10, "Reasoning Ability", ln=1, align="C")
    pdf.ln(5)
    
    with open(csv_reasoning, "r") as f:
        questions = list(csv.DictReader(f))
    
    pdf.set_font("Arial", "B", 10)
    pdf.cell(0, 8, f"Total Questions: {len(questions)}", ln=1)
    pdf.ln(3)
    
    pdf.set_font("Arial", "", 9)
    for i, q in enumerate(questions, 1):
        question_text = q["questionText"]
        options = q["options"].split("|")
        correct = int(q["correctAnswer"])
        correct_option = chr(65 + correct)
        
        pdf.multi_cell(0, 5, f"Q{i}: {question_text}")
        pdf.set_font("Arial", "", 8)
        for j, opt in enumerate(options):
            pdf.cell(25, 5, f"  {chr(65+j)}.", ln=0)
        pdf.ln()
        pdf.set_font("Arial", "I", 8)
        pdf.cell(0, 5, f"Answer: Option {correct_option} | Topic: {q['topic']}", ln=1)
        pdf.ln(2)
    
    # Save PDF
    pdf.output(output_path)
    print(f"PDF created successfully: {output_path}")
    print(f"Total pages: {pdf.page_no()}")
    
    return output_path


if __name__ == '__main__':
    # Generate PDF from existing CSV files
    generate_ibps_pdf(
        csv_english=BASE + "ibps_po_english.csv",
        csv_quant=BASE + "ibps_po_quant.csv",
        csv_reasoning=BASE + "ibps_po_reasoning.csv",
        output_path=BASE + "IBPS_PO_Clerk_Practice_Questions.pdf"
    )