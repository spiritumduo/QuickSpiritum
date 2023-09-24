from diff_pdf_visually import pdf_similar
import sys
#import filecmp
sys.path.append('/requests/functions')
from create_pdf import CreatePDF

test_template_dir: str = '/requests/tests/test templates/'
test_pdf_dir: str = '/requests/tests/test PDFs/'
test_signature_file: str = '/requests/tests/test signatures/Picasso.png'
test_pdf_output_path: str = '/requests/tests/test PDFs/Location 1/Test template 1_Doe, John, 12345_1.pdf'
comparison_pdf_path: str = '/requests/tests/compare PDFs/Location 1/Test template 1_Doe, John, 12345_1.pdf'


# Returns True or False
#print(pdf_similar(test_pdf_output_path, comparison_pdf_path))

docxPtr = CreatePDF(f'{test_template_dir}Location 1/', test_pdf_dir)
locations = docxPtr.get_locations()
print(locations)