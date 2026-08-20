#!/usr/bin/env python3
"""
Generate subject-specific CSV files from the main IBPS daily questions file.
"""

import csv

BASE = "C:/Users/admin/Downloads/"

# Read the main daily questions CSV
with open(BASE + "ibps_po_daily_questions.csv", "r") as f:
    reader = csv.DictReader(f)
    rows = list(reader)

# Separate by subject
english = [r for r in rows if r['subject'] == 'English']
quantitative = [r for r in rows if r['subject'] == 'Quant']
reasoning = [r for r in rows if r['subject'] == 'Reasoning']

# Write English CSV (50 questions)
with open(BASE + "ibps_po_english.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=['id','subject','topic','questionText','options','correctAnswer'])
    writer.writeheader()
    for row in english[:50]:
        writer.writerow({
            'id': row['id'],
            'subject': row['subject'],
            'topic': row['topic'],
            'questionText': row['questionText'],
            'options': row['options'],
            'correctAnswer': row['correctAnswer']
        })
print(f"Generated ibps_po_english.csv: {len(english)} questions")

# Write Quantitative CSV (50 questions)
with open(BASE + "ibps_po_quant.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=['id','subject','topic','questionText','options','correctAnswer'])
    writer.writeheader()
    for row in quantitative[:50]:
        writer.writerow({
            'id': row['id'],
            'subject': row['subject'],
            'topic': row['topic'],
            'questionText': row['questionText'],
            'options': row['options'],
            'correctAnswer': row['correctAnswer']
        })
print(f"Generated ibps_po_quant.csv: {len(quantitative)} questions")

# Write Reasoning CSV (50 questions)
with open(BASE + "ibps_po_reasoning.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=['id','subject','topic','questionText','options','correctAnswer'])
    writer.writeheader()
    for row in reasoning[:50]:
        writer.writerow({
            'id': row['id'],
            'subject': row['subject'],
            'topic': row['topic'],
            'questionText': row['questionText'],
            'options': row['options'],
            'correctAnswer': row['correctAnswer']
        })
print(f"Generated ibps_po_reasoning.csv: {len(reasoning)} questions")

print("\nAll subject-specific CSV files generated successfully!")