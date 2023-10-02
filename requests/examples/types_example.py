"""
    Prints out the request types in the test templates folder
"""

import sys
import os
sys.path.append('/requests/functions')
from create_pdf import CreatePDF

test_template_dir: str = '/requests/tests/test_templates/'
test_pdf_dir: str = '/requests/examples'

docxPtr = CreatePDF(test_template_dir, test_pdf_dir)

print(f'Available requests for "location_1": { docxPtr.get_types("location_1") }')