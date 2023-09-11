#!/usr/bin/python3

from odf import text, teletype
from odf.opendocument import load

templatePath = '/requests/templates/test doc 2.odt'
temporaryPath = '/requests/templates/patient1.odt'
#temporaryPath = '/requests/archieve/patient1.odt'

textdoc = load(templatePath)
texts = textdoc.getElementsByType(text.P)
s = len(texts)
for i in range(s):
    old_text = teletype.extractText(texts[i])
    new_text = old_text.replace('firstname','Mark')
    new_S = text.P()
    new_S.setAttribute("stylename",texts[i].getAttribute("stylename"))
    new_S.addText(new_text)
    texts[i].parentNode.insertBefore(new_S,texts[i])
    texts[i].parentNode.removeChild(texts[i])
textdoc.save(temporaryPath)