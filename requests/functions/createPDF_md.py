#!/usr/bin/python3

from Markdown2docx import Markdown2docx

templatePath = '/requests/templates/test doc 4'
temporaryPath = '/requests/templates/patient1.odt'
#temporaryPath = '/requests/archieve/patient1.odt'

project = Markdown2docx(templatePath)
project.eat_soup()
project.save()