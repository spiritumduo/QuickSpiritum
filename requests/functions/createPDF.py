#!/usr/bin/python3

import os
import docx
from docx import Document
from python_docx_replace import docx_replace
import shutil
import pexpect
import re
import docx2txt



templatePath = '/requests/templates/Salisbury/PFT_Salisbury.docx'
temporaryPath = '/requests/templates/Salisbury/patient1.docx'

ticked = u'\u2612'
unticked = u'\u2610'


doc = Document(templatePath)

my_dict = {
    "First name": "John",
    "Last name": "Smith",
    'Hospital ID' : '123456'
}

docx_replace(doc, **my_dict)
my_dict.clear()
doc.save(temporaryPath)

class docxManipulator():
    def __init__(self, templatePath, outputPath):
        self.templatePath = templatePath
        self.outputPath = outputPath
        return
    
    def get(self):
        variables = {}

        test_doc = docx2txt.process(self.templatePath)
        docu_Regex = re.compile(r'\$\{.*?\}')
        formVariables = docu_Regex.findall(test_doc)

        for key in formVariables:
            cleanedKey=re.sub("[${}]","",key)
            variables[cleanedKey] = ''
            #if '-' in cleanedKey:
                #print(cleanedKey)
                #splitKey = cleanedKey.split('-')
                #print(splitKey[0])
        return variables
    
    def replace(self, variables):
        doc = Document(self.templatePath)
        docx_replace(doc, **variables)
        doc.save(self.outputPath)
        return

"""
my_dict = {
    "First name": "John",
    "Last name": "Smith",
    'Hospital ID-integer' : '123456'
    }
"""

if __name__ == '__main__':
    print("running...")
    docxPtr = docxManipulator(templatePath, temporaryPath)
    variables = docxPtr.get()
    #print(variables)
    variables['First name'] = 'John'
    variables['Last name'] = 'Smith'
    variables['Hospital ID-integer'] = '123456'
    variables['Contraindications-radio-Yes'] = unticked
    variables['Contraindications-radio-No'] = ticked
    #print(variables)
    docxPtr.replace(variables)










"""
from docx import Document
import docxedit

document = Document('/requests/templates/test doc.docx')

# Replace all instances of the word 'Hello' in the document with 'Goodbye'
docxedit.replace_string(document, old_string='VVfirstnameVV', new_string='Mark')

# Replace all instances of the word 'Hello' in the document with 'Goodbye' but only
# up to paragraph 10
#docxedit.replace_string_up_to_paragraph(document, old_string='Hello', new_string='Goodbye', 
#                                        paragraph_number=10)

# Remove any line that contains the word 'Hello' along with the next 5 lines
#docxedit.remove_lines(document, first_line='Hello', number_of_lines=5)

fullText = []
for para in document.paragraphs:
    fullText.append(para.text)
print('\n'.join(fullText))

document.save('/requests/templates/patient1.docx')
"""

"""
def main():
    template_file_path = '/requests/templates/test doc.docx'
    output_file_path = '/requests/archieve/patient1.docx'

    variables = {
        "firstname": "Mark"
    }

    template_document = Document(template_file_path)

    for variable_key, variable_value in variables.items():
        for paragraph in template_document.paragraphs:
            print(paragraph)
            replace_text_in_paragraph(paragraph, variable_key, variable_value)

        for table in template_document.tables:
            for col in table.columns:
                for cell in col.cells:
                    for paragraph in cell.paragraphs:
                        replace_text_in_paragraph(paragraph, variable_key, variable_value)

    template_document.save(output_file_path)


def replace_text_in_paragraph(paragraph, key, value):
    if key in paragraph.text:
        inline = paragraph.runs
        for item in inline:
            if key in item.text:
                item.text = item.text.replace(key, value)


if __name__ == '__main__':
    main()
"""

"""
class createPDF:
    def __init__(self, template, outputLocation):
        self.template = f'{template}.docx'
        self.outputLocation = f'{outputLocation}.docx'

    def create(self, my_dict2):
        create the PDF
            :returns: None
            :rtype: None
        
        shutil.copyfile(self.template, self.outputLocation)

        doc = docx.Document(self.outputLocation)



        #docx_replace(doc, **my_dict2)
        #print(len(doc.paragraphs))

        fullText = []
        for para in doc.paragraphs:
            fullText.append(para.text)
        #print('\n'.join(fullText))

        for paragraph in doc.paragraphs:
            if '[[firstname]]' in paragraph.text:
                #print(paragraph.text)
                paragraph.text = paragraph.text.replace('[[firstname]]', 'Mark')

        doc.save(self.outputLocation)

        pexpect.run(f'doc2pdf {self.outputLocation}')

        os.remove(self.outputLocation)


if __name__ == '__main__':
    print("creating...")
    createPDFptr = createPDF(templatePath, temporaryPath)
    createPDFptr.create(my_dict)
"""