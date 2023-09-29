import unittest
import sys
import os
sys.path.append('/requests/functions')
from create_pdf import CreatePDF
from diff_pdf_visually import pdf_similar

test_template_dir: str = '/requests/tests/test_templates/'
test_template_dir_no_locations: str = '/requests/tests/test_templates_no_locations/'
test_pdf_dir: str = '/requests/tests/test_pdfs/'
test_signature_file: str = '/requests/tests/test_signatures/Peter_Smith.jpg'
test_pdf_output_path: str = '/requests/tests/test_pdfs/location_1/test_template_1_Picasso_Pablo_12345_1.pdf'
comparison_pdf_path: str = '/requests/tests/compare_pdfs/location_1/test_template_1_Picasso_Pablo_12345_1.pdf'

expected_placeholders_return: list[list[str]] = [['Hospital address', '', 'Hospital address'], 
        ['GP name', '', 'GP name'], ['GP address', '', 'GP address'], 
        ['now', '', 'now'], ['First name', '', 'First name'], 
        ['Last name', '', 'Last name'], 
        ['Hospital ID|integer', '', 'Hospital ID', 'integer'], 
        ['Date of birth|date', '', 'Date of birth', 'date'], 
        ['Main diagnoses', '', 'Main diagnoses'], 
        ['Plan', '', 'Plan'], 
        ['Medications', '', 'Medications'], 
        ['Main body', '', 'Main body'],
        ['signature|picture', '', 'signature', 'picture'],
        ['Your name', '', 'Your name'], 
        ['Your postnominals', '', 'Your postnominals'], 
        ['Your position', '', 'Your position'],
        ['configuration | emailTo:mark.bailey5@nhs.net', '', 'configuration', 'emailTo:mark.bailey5@nhs.net']]

test_placeholders: list[list[str]] = [['Hospital address', 'Hospital Road', 'Hospital address'], 
        ['GP name', 'Dr Bob', 'GP name'], ['GP address', '', 'GP address'], 
        ['now', '02/02/1945', 'now'], 
        ['First name', 'Pablo', 'First name'], 
        ['Last name', 'Picasso', 'Last name'], 
        ['Hospital ID|integer', '12345', 'Hospital ID', 'integer'], 
        ['Date of birth|date', '25/10/1881', 'Date of birth', 'date'], 
        ['Main diagnoses', 'Head Flu', 'Main diagnoses'], 
        ['Plan', 'Time', 'Plan'], 
        ['Medications', 'Nil', 'Medications'], 
        ['Main body', 'Pablo had a cold. He is already feeling better', 'Main body'], 
        ['signature|picture', test_signature_file, 'signature', 'picture'],
        ['Your name', 'Dr Peter Smith', 'Your name'], 
        ['Your postnominals', 'MB', 'Your postnominals'], 
        ['Your position', 'Consultant', 'Your position'],
        ['configuration | emailTo:mark.bailey5@nhs.net', '']]
class TestCreatePDF(unittest.TestCase):

    def test_init(self):
        """
            Test that __init__ works
        """
        
        CreatePDF(test_template_dir, test_pdf_dir)


    def test_init_bad_paths(self):
        """
            Test that __init__ fails if env not defined or bad path for 1st arg
        """
        
        with self.assertRaises(ValueError):
            CreatePDF(None, test_pdf_dir)
        
        with self.assertRaises(ValueError):
            CreatePDF('abc123', test_pdf_dir)
        
        with self.assertRaises(ValueError):
            CreatePDF(test_template_dir, None)


    def test_get_locations(self):
        """
            Test what locations are available
        """
        locations: list[str] = []

        docxPtr = CreatePDF(test_template_dir, test_pdf_dir)
        locations = docxPtr.get_locations()

        self.assertEqual(sorted(locations), ['location_1', 'location_2'])


    def test_get_locations_no_locations(self):
        """
            Check that RuntimeError is raised when no subfolders found in template
        """

        docxPtr = CreatePDF(test_template_dir_no_locations, test_pdf_dir)
        
        with self.assertRaises(RuntimeError):
            locations = docxPtr.get_locations()


    def test_check_template(self):
        """
            Check the templates checker runs without issue
        """

        template_pass_state: list[str] = []

        docxPtr = CreatePDF(test_template_dir, test_pdf_dir)
        template_pass_state = docxPtr.check_template(test_template_dir)

        self.assertEqual(template_pass_state,
                         {'/requests/tests/test_templates/location_1/test_template_2_errors.docx': 'FW', 
                          '/requests/tests/test_templates/location_1/test_template_1.docx': '..'})


    def test_check_template_bad_search_location(self):
        """
            Check the templates checker runs without issue
        """

        docxPtr = CreatePDF(test_template_dir, test_pdf_dir)

        with self.assertRaises(RuntimeError):
            docxPtr.check_template('bad location')


    def test_get_types(self):
        """
            Test what request types are available at location
        """

        docxPtr = CreatePDF(test_template_dir, test_pdf_dir)
        types = docxPtr.get_types('location_1')
        self.assertEqual(sorted(types), ['test_template_1', 'test_template_2_errors'])


    def test_get_types_no_types(self):
        """
            Test that fails if no request types in folder (location_2)
        """
        
        docxPtr = CreatePDF(test_template_dir, test_pdf_dir)
        
        with self.assertRaises(RuntimeError):
            docxPtr.get_types('location_2')


    def test_get_types_bad_location(self):
        """
            Test fails if a bad location is given.
        """

        docxPtr = CreatePDF(test_template_dir, test_pdf_dir)
        
        with self.assertRaises(RuntimeError):
            docxPtr.get_types('location_3')


    def test_get_placeholders(self):
        """
            Test return for placeholders in Location 1, Bronchoscopy 1
        """

        docxPtr = CreatePDF(test_template_dir, test_pdf_dir)
        placeholders = docxPtr.get_placeholders('location_1', ['test_template_1'])
        self.assertEqual(placeholders, expected_placeholders_return)


    def test_get_placeholders_check_no_duplicates(self):
        """
            Test no duplicates return, even if the same placeholders are seen in several templates
        """

        docxPtr = CreatePDF(test_template_dir, test_pdf_dir)
        placeholders = docxPtr.get_placeholders('location_1', ['test_template_1', 'test_template_1'])
        self.assertEqual(placeholders, expected_placeholders_return)


    def test_get_placeholders_bad_location(self):
        """
            Test fails if bad location given
        """

        docxPtr = CreatePDF(test_template_dir, test_pdf_dir)
        
        with self.assertRaises(RuntimeError):
            docxPtr.get_placeholders('location_3', [])


    def test_get_placeholders_bad_template_provided(self):
        """
            Test fails for bad template given
        """
        
        docxPtr = CreatePDF(test_template_dir, test_pdf_dir)
        
        with self.assertRaises(RuntimeError):
            docxPtr.get_placeholders('location_1', ['test_template_2'])


    def test_get_placeholders_no_templates_specified(self):
        """
            Test fails if no templates in list provided
        """
        
        docxPtr = CreatePDF(test_template_dir, test_pdf_dir)
        
        with self.assertRaises(RuntimeError):
            docxPtr.get_placeholders('location_1', [])


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

        function_return: str = ''  
        
        old_placeholders: list[list[str]] = test_placeholders.copy()

        if os.path.isfile(test_pdf_output_path):
            os.remove(test_pdf_output_path)

        docxPtr = CreatePDF(test_template_dir, test_pdf_dir)
        function_return = docxPtr.create('location_1', 'test_template_1', 
                        test_placeholders, 'Picasso_Pablo_12345')

        self.assertEqual(function_return, test_pdf_output_path)
        self.assertEqual(test_placeholders, old_placeholders)
        self.assertTrue(pdf_similar(test_pdf_output_path, comparison_pdf_path))

        #os.remove(function_return)


    def test_create_bad_location(self):
        """
            Check that fails if bad location given
        """

        docxPtr = CreatePDF(test_template_dir, test_pdf_dir)
        
        with self.assertRaises(RuntimeError):
            docxPtr.create('location_3', 'test_template_1', test_placeholders, 
                           'Picasso_Pablo_12345')
            
         
    def test_create_bad_template(self):
        """
            Check that fails if bad location given
        """

        docxPtr = CreatePDF(test_template_dir, test_pdf_dir)
        
        with self.assertRaises(RuntimeError):
            docxPtr.create('location_1', 'test_template_2', test_placeholders, 
                           'Picasso_Pablo_12345')
            
    
    def test_create_no_placeholders_provided(self):
        """
            Check that fails if placeholders is empty
        """

        docxPtr = CreatePDF(test_template_dir, test_pdf_dir)
        
        with self.assertRaises(RuntimeError):
            docxPtr.create('location_1', 'test_template_1', [], 
                           'Picasso_Pablo_12345')
    

    def test_create_bad_demographics(self):
        """
            Check that fails with bad character '/' in
        """

        reserved_filename_characters: str = '<>?:"/\\|?*,'

        docxPtr = CreatePDF(test_template_dir, test_pdf_dir)
        
        for c in reserved_filename_characters:
            with self.assertRaises(RuntimeError):
                docxPtr.create('location_1', 'test_template_1', test_placeholders, 
                            f'Picasso_Pablo_12345{ c }')
    

    def test_add_picture(self):
        """
            Check if a PDF is created and matches previously made PDF
        """

        #TODO: May remove this function later

if __name__ == '__main__':
    unittest.main()