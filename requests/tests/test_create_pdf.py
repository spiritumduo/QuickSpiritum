import unittest
import sys
import os
import filecmp
sys.path.append('/requests/functions')
from create_pdf import CreatePDF

test_template_dir: str = '/requests/tests/test templates/'
test_pdf_dir: str = '/requests/tests/test PDFs/'
test_signature_file: str = '/requests/tests/test signatures/Picasso.png'
test_pdf_output_path: str = '/requests/tests/test PDFs/Location 1/Test template 1_Doe, John, 12345_1.pdf'
comparison_pdf_path: str = '/requests/tests/compare PDFs/Location 1/Test template 1_Doe, John, 12345_1.pdf'


class TestCreatePDF(unittest.TestCase):
    def test_get_locations(self):
        """
            Test what locations are available
        """
        locations: list[str] = []

        docxPtr = CreatePDF(test_template_dir, test_pdf_dir)
        locations = docxPtr.get_locations()
        #TODO: should somehow cater for list to be in opposite direction
        self.assertEqual(locations, ['Location 2', 'Location 1'])


    def test_get_types(self):
        """
            Test what request types are available at location
        """

        docxPtr = CreatePDF(test_template_dir, test_pdf_dir)
        types = docxPtr.get_types('Location 1')
        self.assertEqual(types, ['Test template 1'])


    def test_get_placeholders(self):
        """
            Test return for placeholders in Location 1, Bronchoscopy 1
        """
        expected_return: list[list[str]] = [['Hospital address', '', 'Hospital address'], 
                ['GP name', '', 'GP name'], ['GP address', '', 'GP address'], 
                ['now', '', 'now'], ['First name', '', 'First name'], 
                ['Last name', '', 'Last name'], 
                ['Hospital ID|integer', '', 'Hospital ID', 'integer'], 
                ['Date of birth|date', '', 'Date of birth', 'date'], 
                ['Main diagnoses', '', 'Main diagnoses'], 
                ['Plan', '', 'Plan'], 
                ['Medications', '', 'Medications'], 
                ['Main body', '', 'Main body'], 
                ['Your name', '', 'Your name'], 
                ['Your postnominals', '', 'Your postnominals'], 
                ['Your position', '', 'Your position']]

        docxPtr = CreatePDF(test_template_dir, test_pdf_dir)
        placeholders = docxPtr.get_placeholders('Location 1', ['Test template 1'])
        self.assertEqual(placeholders, expected_return)


    def test_sub_list_extract(self):
        """
            Test for this sub functions output
        """
        placeholders_final: list[list[str]] = [
                    ['Hospital ID|integer', '', 'Hospital ID', 'integer']]

        expected_list_result: list[list[str]] = [
                    ['Hospital ID|integer', '', 'Hospital ID', 'integer'],
                        ['Date of birth|date', '', 'Date of birth', 'date']]
        
        cleaned_placeholder = 'Date of birth|date'
        docxPtr = CreatePDF(test_template_dir, test_pdf_dir)
        function_return: Any = None

        function_return = docxPtr.sub_list_extract(placeholders_final, cleaned_placeholder)

        self.assertEqual(function_return, None)
        self.assertEqual(placeholders_final, expected_list_result)


    def test_create(self):
        """
            Check if a PDF is created and matches previously made PDF
        """

        function_return: Any = None   

        placeholders: list[list[str]] = [['Hospital address', 'Hospital Road', 'Hospital address'], 
                ['GP name', 'Dr Bob', 'GP name'], ['GP address', '', 'GP address'], 
                ['now', '--/--/--', 'now'], 
                ['First name', 'John', 'First name'], 
                ['Last name', 'Doe', 'Last name'], 
                ['Hospital ID|integer', '12345', 'Hospital ID', 'integer'], 
                ['Date of birth|date', '01/01/1990', 'Date of birth', 'date'], 
                ['Main diagnoses', 'Head Flu', 'Main diagnoses'], 
                ['Plan', 'Time', 'Plan'], 
                ['Medications', 'Nil', 'Medications'], 
                ['Main body', 'John had a cold. He is already feeling better', 'Main body'], 
                ['Your name', 'Dr Goodyear', 'Your name'], 
                ['Your postnominals', 'MB', 'Your postnominals'], 
                ['Your position', 'Consultant', 'Your position']]
        
        old_placeholders: list[list[str]] = placeholders.copy()

        if os.path.isfile(test_pdf_output_path):
            os.remove(test_pdf_output_path)

        docxPtr = CreatePDF(test_template_dir, test_pdf_dir)
        function_return = docxPtr.create('Location 1', 'Test template 1', placeholders, 'Doe, John, 12345', test_signature_file)

        self.assertEqual(function_return, test_pdf_output_path)
        #self.assertEqual(placeholders, old_placeholders)
        #self.assertTrue(filecmp.cmp(test_pdf_output_path, comparison_pdf_path))
        #TODO: somehow need to compare PDF files

        os.remove(function_return)





if __name__ == '__main__':
    unittest.main()