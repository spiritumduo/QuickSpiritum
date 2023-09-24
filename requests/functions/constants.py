"""constants for createPDF.py

"""

import os

TEMPLATE_DIR: str | None = os.getenv('TEMPLATE_DIR')
PDF_DIR: str | None = os.environ.get('PDF_DIR')

CHECKED: str = u'\u2612'
UNCHECKED: str = u'\u2610'

DELIMITER: str = '|'

