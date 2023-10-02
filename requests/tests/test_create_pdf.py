import unittest
import sys
import os
import filecmp
sys.path.append('/requests/functions')
from create_pdf import CreatePDF

test_template_dir: str = '/requests/tests/test docs/'
test_pdf_dir: str = '/requests/tests/test PDFs/'
test_signature_file: str = '/requests/tests/test signatures/Picasso.png'
test_pdf_output_path: str = '/requests/tests/test PDFs/Location 1/Bronchoscopy 1_Smith, John, 123456_1.pdf'
comparison_pdf_path: str = '/requests/tests/compare PDFs/Location 1/Bronchoscopy 1_Smith, John, 123456_1.pdf'


class TestCreatePDF(unittest.TestCase):
    def test_get_locations(self):
        """
            Test what locations are available
        """
        locations: list[str] = []

        docxPtr = CreatePDF(test_template_dir, test_pdf_dir)
        locations = docxPtr.get_locations()
        self.assertEqual(locations, ['Location 2', 'Location 1'])


    def test_get_types(self):
        """
            Test what request types are available at location
        """

        docxPtr = CreatePDF(test_template_dir, test_pdf_dir)
        types = docxPtr.get_types('Location 1')
        self.assertEqual(types, ['Bronchoscopy 1'])


    def test_get_placeholders(self):
        """
            Test return for placeholders in Location 1, Bronchoscopy 1
        """
        expected_return: str = [['Hospital ID|integer', '', 'Hospital ID', 'integer'],
                            ['Date of Birth|date', '', 'Date of Birth', 'date'],
                            ['First name', '', 'First name'],
                            ['Last name', '', 'Last name']]

        docxPtr = CreatePDF(test_template_dir, test_pdf_dir)
        placeholders = docxPtr.get_placeholders('Location 1', ['Bronchoscopy 1'])
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

        placeholders: list[list[str]] = [
            ['Hospital ID|integer', '12345', 'Hospital ID', 'integer'],
                ['Date of Birth|date', '01/01/1999', 'Date of birth', 'date'],
                ['First name', 'John'],
                ['Last name', 'Smith']]
        
        old_placeholders: list[list[str]] = placeholders.copy()

        docxPtr = CreatePDF(test_template_dir, test_pdf_dir)
        function_return = docxPtr.create('Location 1', 'Bronchoscopy 1', placeholders, 'Smith, John, 123456', test_signature_file)

        self.assertEqual(function_return, test_pdf_output_path)
        self.assertEqual(placeholders, old_placeholders)
        #self.assertTrue(filecmp.cmp(test_pdf_output_path, comparison_pdf_path))
        #TODO: somehow need to compare PDF files

        os.remove(function_return)





if __name__ == '__main__':
    unittest.main()