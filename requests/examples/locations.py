
import sys
import os
sys.path.append('/requests/functions')
from create_pdf import CreatePDF

test_template_dir: str = '/requests/tests/test_templates/'
test_pdf_dir: str = '/requests/examples'

print("Running...")

docxPtr = CreatePDF(test_template_dir, test_pdf_dir)
# Get the different locations
print(f'Locations: { docxPtr.get_locations() }')

# Get the types of requests in a the Salisbury trust
#print(f'Available requests in Salisbury: { docxPtr.get_types("Salisbury") }')

# Get variables from
#requests = ['Bronchoscopy 1', 'Bronchoscopy 2', 'Bronchoscopy 3']
#variables = docxPtr.get_placeholders('Salisbury', ['Lung function test'])
#print(variables)

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