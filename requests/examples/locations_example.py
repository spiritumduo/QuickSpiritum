"""
    Prints out the locations in the tests folder template
"""

import sys
import os
sys.path.append('/requests/functions')
from create_pdf import CreatePDF

test_template_dir: str = '/requests/tests/test_templates/'
test_pdf_dir: str = '/requests/examples'

docxPtr = CreatePDF(test_template_dir, test_pdf_dir)
# Get the different locations
print(f'Locations: { docxPtr.get_locations() }')
