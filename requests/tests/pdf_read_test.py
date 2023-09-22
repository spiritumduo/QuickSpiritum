"""from PyPDF2 import PdfReader
import cv2
import numpy as np
from pdf2image import convert_from_path
import pypdfium2 as pdfium"""

pic_1 = 'Lung function test_Baker, Monika, 0208815_1.pdf'
pic_2 = 'Lung function test_Baker, Monika, 0208815_1 copy.pdf'

"""reader = PdfReader("Bronchoscopy 1_Smith, John, 123456_1.pdf")
for page in reader.pages:
    print(page.extract_text())

for page in reader.pages:
    for image_file_object in page.images:
        print(image_file_object.name)"""


 
"""pdf = pdfium.PdfDocument(pic_1)
n_pages = len(pdf)
for page_number in range(n_pages):
    page = pdf.get_page(page_number)
    pil_image = page.render_topil(
        scale=1,
        rotation=0,
        crop=(0, 0, 0, 0),
        colour=(255, 255, 255, 255),
        annotations=True,
        greyscale=False,
        optimise_mode=pdfium.OptimiseMode.NONE,
    )
    pil_image.save(f"image_{page_number+1}.png") """


"""a = cv2.imread(pic_1)
b = cv2.imread(pic_2)
difference = cv2.subtract(a, b)    
result = not np.any(difference)
if result is True:
    print("Pictures are the same")
else:
    cv2.imwrite("ed.jpg", difference )
    print("Pictures are different, the difference is stored as ed.jpg")"""
