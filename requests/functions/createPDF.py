#!/usr/bin/python3

import os
import docx
from docx import Document
from python_docx_replace import docx_replace
import shutil
import pexpect
import re
import docx2txt
from docx2pdf import convert
from pathlib import Path


import constants as C

#TODO: try and move these to the contants module
TEMPLATE_DIR = os.getenv('TEMPLATE_DIR')
PDF_DIR = os.environ.get('PDF_DIR')



class docxManipulator():
    def __init__(self, templateDir: str, outputPath: str) -> None:
        self.templateDir: str = templateDir
        self.outputPath: str = outputPath
        return
    

    def getLocations(self) -> list[str] | None:
        locations: list[str] = []

        # list of all content in a directory, filtered so only directories are returned
        locations = [directory for directory in os.listdir(self.templateDir) if os.path.isdir(self.templateDir+directory)]
        return locations
    

    def getTypes(self, location: str) -> list[str]:
        types: list[str] = []
        typesPath = f'{self.templateDir}{location}/'

        #TODO: #2 need to check locations folder exists

        if not os.path.isdir(typesPath):
            raise Exception(f'"{typesPath}" is not a valid directory!')
            return None


        types = [f for f in os.listdir(typesPath) 
                 if os.path.isfile(f'{typesPath}{f}') 
                 and f.endswith(".docx") 
                 and not f.startswith('~')]

        return types
    

    def getVariables(self, location: str, type: str) -> dict[str,str]:
        variables: dict[str,str] = {}
        
        doc = docx2txt.process(f'{ self.templateDir }{ location }/{ type }.docx')
        doc_Regex = re.compile(r'\$\{.*?\}')
        formVariables = doc_Regex.findall(doc)

        for key in formVariables:
            cleanedKey=re.sub("[${}]","",key)
            variables[cleanedKey] = ''
            #if '-' in cleanedKey:
                #print(cleanedKey)
                #splitKey = cleanedKey.split('-')
                #print(splitKey[0])
        return variables
    

    def createPDF(self, location: str, type: str, variables: dict[str,str], demographics: str) -> str | None:
        templatePath: str = f'{ self.templateDir }{ location }/{ type }.docx'
        tempDocxDir: str = f'{ self.outputPath }{ location }/temp/'
        tempDocxPath: str = f'{ tempDocxDir }{ type }_{ demographics }_'
        PDFPath: str = ''
        n: int = 1

        #TODO: need to check location folder exists
        #TODO: need to check type template file exists.
        
        # Make directory with sub-folders if needed
        if not os.path.isdir(tempDocxDir):
            Path(tempDocxDir).mkdir(parents=True, exist_ok=True)

        #TODO: Need to check demographics are ok for location naming eg no  / or \

        while n < 10000:
            if os.path.exists(f'{ self.outputPath }{ location }/{ type }_{ demographics }_{ n }.pdf'):
                n = n + 1
            else:
                break

        if n >= 10000:
            raise Exception('Filename increment over ran!')
            return None
        

        tempDocxPath =f'{ tempDocxPath }{ n }.docx'
        PDFDir: str = f'{ self.outputPath }{ location }'
        PDFPath = f'{ self.outputPath }{ location }/{ type }_{ demographics }_{ n }.pdf'

        try:
            doc = Document(templatePath)
            docx_replace(doc, **variables)
            doc.save(tempDocxPath)
        except:
            raise Exception(f'Could not create the .docx file "{ tempDocxPath }"!')
            return None
    
        if not os.path.isfile(tempDocxPath):
            raise Exception(f'"{tempDocxPath}" is not a valid filename!')
            return False

        libreofficeOutput = pexpect.spawn(f'libreoffice --headless --convert-to pdf "{ tempDocxPath }" --outdir "{ PDFDir }"')
        
        if libreofficeOutput.read()[0:7] != b'convert':
            raise Exception(f'Error with PDF creation via LibreOffice')
            return False


        #pexpect.run(f'libreoffice --headless --convert-to pdf "{ tempDocxPath }" --outdir "{ PDFDir }"')
        #list_files = subprocess.run(['libreoffice' , '--headless', '--convert-to', 'pdf' ,'/requests/archive/Salisbury/temp/Lung function test_Smith, John, 1234567_1.docx', '--outdir', '/requests/archive/Salisbury'])
        #print("The exit code was: %d" % list_files.returncode)
        #print(f'unoconvert "{ tempDocxPath }" "{ PDFPath }"')

        os.remove(tempDocxPath)
        return True

        


if __name__ == '__main__':
    print("Running...")
    
    docxPtr = docxManipulator(TEMPLATE_DIR, PDF_DIR)
    # Get the different locations
    print(f'Locations: { docxPtr.getLocations() }')
    
    # Get the types of requests in a the Salisbury trust
    print(f'Available requests in Salisbury: { docxPtr.getTypes("Salisbury") }')
    
    # Get variables from
    variables = docxPtr.getVariables('Salisbury', 'Lung function test')

    #print(variables)
    variables['First name'] = 'John'
    variables['Last name'] = 'Smith'
    variables['Hospital ID-integer'] = '123456'
    variables['Contraindications-radio-Yes'] = C.UNCHECKED
    variables['Contraindications-radio-No'] = C.CHECKED

    """print('Placeholders for Lung function tests at Salisbury are:')
    for v in variables:
        print(v)"""
    
    tempDocxPath = docxPtr.createPDF('Salisbury', 'Lung function test', variables, "Smith, John, 1234567")
