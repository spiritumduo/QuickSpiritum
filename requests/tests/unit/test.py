from diff_pdf_visually import pdf_similar
import sys
#import filecmp
sys.path.append('/requests/functions')
from create_pdf import CreatePDF
from docxtpl import DocxTemplate

test_template_dir: str = '/requests/tests/test_templates/'
test_template_dir_no_locations: str = '/requests/tests/test_templates_no_locations/'
test_pdf_dir: str = '/requests/tests/test_pdfs/'
test_signature_file: str = '/requests/tests/test_signatures/Picasso.png'
test_pdf_output_path: str = '/requests/tests/test_pdfs/location_1/test_template_1_Doe,John,12345_1.pdf'
comparison_pdf_path: str = '/requests/tests/compare_pdfs/location_1/test_template_1_Doe,John,12345_1.pdf'

if True:
    print(f'Hello, how are you today. ' \
          f'I am fine thanks.')
    
    raise RuntimeError(
            f'Image filename "{ test_pdf_output_path }" '
            f'does not exist'
            )

"""docxPtr = CreatePDF('/requests/templates/', test_pdf_dir)

docxPtr.check_template()"""

#docxPtr.check_template('/requests/templates/Salisbury/Lung function test.docx')

#docxPtr.check_template('/requests/tests/test_templates/location_1/test_template_1.docx')

"""tpl=DocxTemplate('/requests/tests/test_templates/location_1/test_template_1.docx')
set_of_variables = tpl.get_undeclared_template_variables()
print(set_of_variables)"""



"""docxPtr = CreatePDF(test_template_dir, test_pdf_dir)
types = docxPtr.get_types('location_2')
print(types)"""