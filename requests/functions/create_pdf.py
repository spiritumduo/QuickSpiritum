#!/usr/bin/python3

""" Takes a docx file with placeholders and fills in placeholders and creates a PDF

"""

import os
from pathlib import Path
from docx import Document
from python_docx_replace import docx_replace
import pexpect
import re
import docx2txt
import constants as C

#TODO: try and move these to the contants module


from docxtpl import DocxTemplate, InlineImage
from docx.shared import Mm



class CreatePDF():
    """ Extract information from docx template and also create PDF with required information
    
    """
    def __init__(self, template_dir: str | None, output_path: str | None) -> None:
        if template_dir == None:
            raise Exception(f'No template directory stored in environmental file .env')
            return None
        
        if output_path == None:
            raise Exception(f'No output path stored in environmental file .env')
            return None
        
        self.template_dir: str = str(template_dir)
        self.output_path: str = str(output_path)
        return None
    

    def get_locations(self) -> list:
        """ Get the 'locations' (physical or virtual) for a collection of different clinical requests

        """
        locations: list[str] = []

        # list of all content in a directory, filtered so only directories are returned
        locations = [directory for directory in os.listdir(self.template_dir)
                     if os.path.isdir(self.template_dir+directory)]
        return locations
    
    #TODO: Perhaps can use docx_get_keys() instead to get keys
    def get_types(self, location: str) -> list[str]:
        """ Get the types of tests available for a location
        
        """
        types: list[str] = []
        types_path = f'{self.template_dir}{location}/'

        #TODO: #2 need to check locations folder exists

        if not os.path.isdir(types_path):
            raise Exception(f'"{types_path}" is not a valid directory!')
            return None


        types = [f for f in os.listdir(types_path) 
                 if os.path.isfile(f'{types_path}{f}') 
                 and f.endswith(".docx") 
                 and not f.startswith('~')]
        
        types = [x.removesuffix('.docx') for x in types]

        return types
    
    #TODO: will need return hint type
    def get_placeholders(self, location: str, requests: list[str]) -> list[list[str]]:
        """ Gets placeholders and remove any duplicates as they appear
            
                Args:
                location: locations of requests (either physical or virtual)
                *argv: one or more request types
            returns:
                list[str]
        """
        #TODO: #4 might want to make this a dictionary of lists (for easier searching)
        placeholders_final: list[list[str]] = []
        raw_placeholders: list[str] = []
        cleaned_placeholder: str = ''
        
        for request in requests:
            doc = docx2txt.process(f'{ self.template_dir }{ location }/{ request }.docx')
            #TODO: need to check if above file exists!
            doc_Regex = re.compile(r'\$\{.*?\}')
            raw_placeholders = doc_Regex.findall(doc)

            for raw_placeholder in raw_placeholders:
                cleaned_placeholder = re.sub("[${}]", "", raw_placeholder)
                
                if len(placeholders_final) == 0:
                    self.sub_list_extract(placeholders_final, cleaned_placeholder)
                elif not any(cleaned_placeholder in ph for ph in placeholders_final):
                    self.sub_list_extract(placeholders_final, cleaned_placeholder)

        return placeholders_final
    

    def sub_list_extract(self, placeholders_final: list[list[str]], cleaned_placeholder: str) -> None:
        """ sub routine to split via piped delimiter 
        
        """

        subList: list[str] = []

        subList.append(cleaned_placeholder)
        subList.append('')

        splitKey = cleaned_placeholder.split(C.DELIMITER)
        for s in splitKey:
            subList.append(s.strip())
        
        placeholders_final.append(list(subList))
        return None


    #TODO: could rewrite this to use the python-docx-template library
    def create(self, location: str, type: str, variables, demographics: str, signature_path) -> None | str:
        """ Actually create the PDF
        
        """

        template_path: str = f'{ self.template_dir }{ location }/{ type }.docx'
        temp_docx_dir: str = f'{ self.output_path }{ location }/temp/'
        temp_docx_path: str = f'{ temp_docx_dir }{ type }_{ demographics }_'
        n: int = 1
        pdf_dir: str = ''
        pdf_path: str = ''
        variables_dict: dict[str,str] = {}
        locations: list[str] | None = []
        #TODO: libreoffice_output: type[pexpect]

        locations = self.get_locations()

        if not location in locations:
            raise Exception('Location does not exist!')
            return None

        if not os.path.exists(template_path):
            raise Exception(f'Template docx file "{ template_path }" does not exist!')
            return None
        
        if any(illegal in demographics for illegal in "\\/"):
            raise Exception(f'Illegal character in demographics - "{ demographics }"')
            return None

        # Make directory with sub-folders if needed
        if not os.path.isdir(temp_docx_dir):
            Path(temp_docx_dir).mkdir(parents=True, exist_ok=True)

        while n < 10000:
            if os.path.exists(f'{ self.output_path }{ location }/{ type }_{ demographics }_{ n }.pdf'):
                n = n + 1
            else:
                break

        if n >= 10000:
            raise Exception('Filename increment over ran!')
            return None
        
        temp_docx_path =f'{ temp_docx_path }{ n }.docx'
        pdf_dir = f'{ self.output_path }{ location }'
        pdf_path = f'{ self.output_path }{ location }/{ type }_{ demographics }_{ n }.pdf'

        for x in range(len(variables)):
            variables_dict[variables[x][0]] = variables[x][1]

        try:
            doc = Document(template_path)
            docx_replace(doc, **variables_dict)
            doc.save(temp_docx_path)
        except:
            raise Exception(f'Could not create the .docx file "{ temp_docx_path }"!')
            return None
        
        # Double check that the file has been created
        if not os.path.isfile(temp_docx_path):
            raise Exception(f'Error - file {temp_docx_path}" has not been created!')
            return None
        
        self.addPicture(temp_docx_path, signature_path)

        libreoffice_output = pexpect.spawn(f'libreoffice --headless --convert-to pdf "{ temp_docx_path }" --outdir "{ pdf_dir }"')
        
        #TODO: print(type(libreoffice_output))

        if libreoffice_output.read()[0:7] != b'convert':
            raise Exception(f'Error with PDF creation via LibreOffice')
            return None

        os.remove(temp_docx_path)

        return pdf_path
    

    def addPicture(self, file: str, image: str, placeholder: str = "signature", 
                   width = Mm(20)) -> None:
        """ For adding pictures to docx. May be able to join this with 'create'
            by using the python-docx-template module
        
        """
        
        doc: type[docxtpl]

        if not os.path.exists(file):
            raise Exception(f'Docx filename "{ file }" does not exist')
            return None
        if not os.path.exists(image):
            raise Exception(f'Image filename "{ image }" does not exist')
            return None

        doc = DocxTemplate(file)
        context = {placeholder: InlineImage(doc, image, width = width)}
        doc.render(context)
        doc.save(file)

        return None



if __name__ == '__main__':
    print("Running...")
    
    docxPtr = CreatePDF(C.TEMPLATE_DIR, C.PDF_DIR)
    # Get the different locations
    #print(f'Locations: { docxPtr.get_locations() }')
    
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
    #pdf_path = docxPtr.create('Salisbury', 'Lung function test', variables, "Smith, John, 1234567")
    #print(pdf_path)

    #docxPtr.addPicture('/requests/testing/Lung function test.docx', '/requests/signatures/Mark Bailey.jpeg')