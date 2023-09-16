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



class createPDF():
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
        
        types = [x.removesuffix('.docx') for x in types]

        return types
    
    #TODO: will need return hint type
    def getPlaceholders(self, location: str, requests: list[str]):
        """ Gets placeholders and remove any duplicates as they appear
            
                Args:
                location: locations of requests (either physical or virtual)
                *argv: one or more request types
            returns:
                list[str]
        """
        variables = [] #TODO: hint thype for 2D lists??
        subList: list[str] = []
        
        #TODO: Need to make sure argv provides correct data and there is more than one arg provided

        #print(requests)
        for request in requests:
            #print(f'***{request}')
            doc = docx2txt.process(f'{ self.templateDir }{ location }/{ request }.docx')
            doc_Regex = re.compile(r'\$\{.*?\}')
            formVariables = doc_Regex.findall(doc)

            for key in formVariables:
                cleanedKey = re.sub("[${}]", "", key)
                
                if len(variables) == 0:
                    subList.append(cleanedKey)
                    subList.append('')

                    splitKey = cleanedKey.split('|')
                    for s in splitKey:
                        subList.append(s.strip())
                    
                    variables.append(list(subList))
                    subList.clear()
                else:
                    # needed to use 'any' to check if an item is present in a 2D list.
                    if not any(cleanedKey in subl for subl in variables):
                        subList.append(cleanedKey)
                        subList.append('')

                        splitKey = cleanedKey.split('|')
                        for s in splitKey:
                            subList.append(s)
                        
                        variables.append(list(subList))
                        subList.clear()
                
        #for c in variables:
        #    print(c[0])
            
        return variables
    

    def create(self, location: str, type: str, variables, demographics: str):
        templatePath: str = f'{ self.templateDir }{ location }/{ type }.docx'
        tempDocxDir: str = f'{ self.outputPath }{ location }/temp/'
        tempDocxPath: str = f'{ tempDocxDir }{ type }_{ demographics }_'
        PDFPath: str = ''
        n: int = 1
        variablesDict: dict[str,str] = {}

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


        for x in range(len(variables)):
            variablesDict[variables[x][0]] = variables[x][1]

        #try:
        doc = Document(templatePath)
        docx_replace(doc, **variablesDict)
        doc.save(tempDocxPath)
        """except:
            raise Exception(f'Could not create the .docx file "{ tempDocxPath }"!')
            return None"""
    
        if not os.path.isfile(tempDocxPath):
            raise Exception(f'"{tempDocxPath}" is not a valid filename!')
            return None

        libreofficeOutput = pexpect.spawn(f'libreoffice --headless --convert-to pdf "{ tempDocxPath }" --outdir "{ PDFDir }"')
        
        if libreofficeOutput.read()[0:7] != b'convert':
            raise Exception(f'Error with PDF creation via LibreOffice')
            return None


        #pexpect.run(f'libreoffice --headless --convert-to pdf "{ tempDocxPath }" --outdir "{ PDFDir }"')
        #list_files = subprocess.run(['libreoffice' , '--headless', '--convert-to', 'pdf' ,'/requests/archive/Salisbury/temp/Lung function test_Smith, John, 1234567_1.docx', '--outdir', '/requests/archive/Salisbury'])
        #print("The exit code was: %d" % list_files.returncode)
        #print(f'unoconvert "{ tempDocxPath }" "{ PDFPath }"')

        os.remove(tempDocxPath)
        return PDFPath

        


if __name__ == '__main__':
    print("Running...")
    
    docxPtr = createPDF(TEMPLATE_DIR, PDF_DIR)
    # Get the different locations
    #print(f'Locations: { docxPtr.getLocations() }')
    
    # Get the types of requests in a the Salisbury trust
    #print(f'Available requests in Salisbury: { docxPtr.getTypes("Salisbury") }')
    
    # Get variables from
    #requests = ['Bronchoscopy 1', 'Bronchoscopy 2', 'Bronchoscopy 3']
    variables = docxPtr.getPlaceholders('Salisbury', ['Lung function test'])
    #print(variables)

    # These might not work any more as Lists instead of Dic are bring used.

    variables[0][1] = '123456'
    variables[2][1] = 'John'
    variables[3][1] = 'Smith'
    variables[5][1] = C.UNCHECKED
    variables[6][1] = C.CHECKED

    """print('Placeholders for Lung function tests at Salisbury are:')
    for v in variables:
        print(v)
    """
    PDFPath = docxPtr.create('Salisbury', 'Lung function test', variables, "Smith, John, 1234567")
    print(PDFPath)