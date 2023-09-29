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

# These might not work any more as Lists instead of Dic are bring used.

"""variables[0][1] = '123456'
variables[2][1] = 'John'
variables[3][1] = 'Smith'
variables[5][1] = C.UNCHECKED
variables[6][1] = C.CHECKED"""

"""print('Placeholders for Lung function tests at Salisbury are:')
for v in variables:
    print(v)
"""
#pdf_path = docxPtr.create('Salisbury', 'Lung function test', variables, "Smith_John_1234567", '/requests/signatures/Mark Bailey.jpeg')
#print(pdf_path)

#docxPtr.add_picture('/requests/testing/Lung function test.docx', '/requests/signatures/Mark Bailey.jpeg')