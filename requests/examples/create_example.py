"""
    Prints out the request types in the test templates folder
"""

import sys
import os
sys.path.append('/requests/functions')
from create_pdf import CreatePDF

template_dir: str = '/requests/tests/test_templates/'
pdf_dir: str = '/requests/examples/'
test_signature_file: str = '/requests/tests/test_signatures/Peter_Smith.jpg'

placeholders: list[list[str]] = [
        ['Hospital address', 'Hospital Road', 'Hospital address'], 
        ['GP name', 'Dr Bob', 'GP name'], ['GP address', '', 'GP address'], 
        ['now', '02/02/1945', 'now'], 
        ['First name', 'Pablo', 'First name'], 
        ['Last name', 'Picasso', 'Last name'], 
        ['Hospital ID|integer', '12345', 'Hospital ID', 'integer'], 
        ['Date of birth|date', '25/10/1881', 'Date of birth', 'date'], 
        ['Main diagnoses', 'Head Flu', 'Main diagnoses'], 
        ['Plan', 'Time', 'Plan'], 
        ['Medications', 'Nil', 'Medications'], 
        ['Main body', 'Pablo had a cold. He is already feeling better', 'Main body'], 
        ['signature|picture', test_signature_file, 'signature', 'picture'],
        ['Your name', 'Dr Peter Smith', 'Your name'], 
        ['Your postnominals', 'MB', 'Your postnominals'], 
        ['Your position', 'Consultant', 'Your position'],
        ['configuration | emailTo:mark.bailey5@nhs.net', '']
        ]

docxPtr = CreatePDF(template_dir, pdf_dir)

pdf_path = docxPtr.create('location_1', 'test_template_1', placeholders, "Smith_John_123456")
print(pdf_path)