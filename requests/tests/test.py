"""import unittest
import sys
import os
import filecmp
sys.path.append('/requests/functions')
from create_pdf import CreatePDF

test_template_dir: str = '/requests/tests/test templates/'
test_pdf_dir: str = '/requests/tests/test PDFs/'
test_signature_file: str = '/requests/tests/test signatures/Picasso.png'
test_pdf_output_path: str = '/requests/tests/test PDFs/Location 1/Bronchoscopy 1_Smith, John, 123456_1.pdf'
comparison_pdf_path: str = '/requests/tests/compare PDFs/Location 1/Bronchoscopy 1_Smith, John, 123456_1.pdf'



docxPtr = CreatePDF(test_template_dir, test_pdf_dir)
placeholders = docxPtr.get_placeholders('Location 1', ['Test template 1'])
print(placeholders)"""