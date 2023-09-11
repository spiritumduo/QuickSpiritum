import os
import comtypes.client
wdFormatPDF = 17
x = 0
for f in os.listdir():
    if f.endswith(".docx"):
        in_file = os.path.abspath(f)
        out_file = os.path.abspath("demo" + str(x) + ".pdf")
        word = comtypes.client.CreateObject('Word.Application')
        doc = word.Documents.Open(in_file)
        doc.SaveAs(out_file, FileFormat=wdFormatPDF)
        doc.Close()
        x += 1
word.Quit()