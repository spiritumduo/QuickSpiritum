"""
    Prints out the request types in the test templates folder
"""

import sys
import os
sys.path.append('/requests/functions')
from create_pdf import CreatePDF

test_template_dir: str = '/requests/tests/test_templates/'
test_pdf_dir: str = '/requests/examples'

placeholders: list[list[str]] = []

docxPtr = CreatePDF(test_template_dir, test_pdf_dir)

requests = ['test_template_1', 'test_template_2_errors']
placeholders = docxPtr.get_placeholders('location_1', requests)

for ph in placeholders:
    print(ph[2])