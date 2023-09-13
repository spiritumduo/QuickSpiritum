#!/usr/bin/python3

# import flask module

from flask import Flask
from flask import render_template
import sys
import os
sys.path.append('/requests/functions')
from createPDF import docxManipulator



import constants as C
TEMPLATE_DIR = os.getenv('TEMPLATE_DIR')
PDF_DIR = os.environ.get('PDF_DIR')


 
# instance of flask application
app = Flask(__name__)
 
# home route that returns below text
# when root url is accessed
@app.route("/")
def index():
    name='you'
    trans = {'yes':'qui', 'no':'noi', 'portal': 'portal'}

    docxPtr = docxManipulator(TEMPLATE_DIR, PDF_DIR)
    # Get the different locations
    print(f'Locations: { docxPtr.getLocations() }')

    getLocations = docxPtr.getLocations()
    variables = docxPtr.getVariables('Salisbury', 'Lung function test')
    context = {}
    context['trans'] = trans
    return render_template('index.html', trans=trans, getLocations=getLocations, variables=variables)
    #return "<p>Hello, World!</p>"

 
if __name__ == '__main__':
    app.run(debug=True, port=1111, host="0.0.0.0")
