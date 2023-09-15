#!/usr/bin/python3

# import flask module

from flask import Flask, request, render_template
import sys
import os
sys.path.append('/requests/functions')
from createPDF import createPDF
sys.path.append('/app/modules')
from formElements import formElements

#TODO: need to have a data cleanser that fixes illegal characters in the placeholders received from the docx file (eg ' and ")

import constants as C
TEMPLATE_DIR = os.getenv('TEMPLATE_DIR')
PDF_DIR = os.environ.get('PDF_DIR')

trans = {'yes':'qui', 'no':'noi', 'portal': 'portal'}
 

# A temporary variable. This needs to be in a database and associated with a user
lastSelectedLocation = 'Salisbury'

# instance of flask application
app = Flask(__name__)
 

@app.route("/")
def index():
    locationOptionsHTML: str = ''
    linicalRequestTypes: str = ''

    docxPtr = createPDF(TEMPLATE_DIR, PDF_DIR)
    # Get the different locations
    #print(f'Locations: { docxPtr.getLocations() }')

    getLocations = docxPtr.getLocations()
    variables = docxPtr.getPlaceholders('Salisbury', 'Lung function test')

    if len(getLocations) == 0:
        raise Exception(f'No locations found in templates folder!')
        return

    for location in getLocations:
        if location == lastSelectedLocation:
            locationOptionsHTML += f"""<option selected="selected" value="{ location }">{ location }</option>\n"""
        else:
            locationOptionsHTML += f"""<option value="{ location }">{ location }</option>\n"""
    
    clinicalRequestTypes = docxPtr.getTypes("Salisbury")
    print(clinicalRequestTypes)
    return render_template('index.html', 
                           trans=trans, 
                           locationOptionsHTML=locationOptionsHTML,
                           locationDropDown=locationDropDown,
                           clinicalRequestTypes=clinicalRequestTypes)



@app.route("/clinicalRequesting")
def clinicalRequesting():
    locationOptionsHTML:str = ''

    docxPtr = createPDF(TEMPLATE_DIR, PDF_DIR)
    # Get the different locations
    #print(f'Locations: { docxPtr.getLocations() }')

    getLocations = docxPtr.getLocations()
    variables = docxPtr.getPlaceholders('Salisbury', 'Lung function test')

    if len(getLocations) == 0:
        raise Exception(f'No locations found in templates folder!')
        return

    for location in getLocations:
        if location == lastSelectedLocation:
            locationOptionsHTML += f"""<option selected="selected" value="{ location }">{ location }</option>\n"""
        else:
            locationOptionsHTML += f"""<option value="{ location }">{ location }</option>\n"""

    locationDropDown = f"""<div class="locationSelect-div-padding">
                                <select class="locationSelect" name="locations" id="location">
                                    { locationOptionsHTML }
                                </select>
                            </div>"""
    
    preparedFormElements = formElements()
    formHTML = preparedFormElements.createElements(variables)

    context = {}
    context['trans'] = trans
    return render_template('index.html', 
                           trans=trans, 
                           locationDropDown=locationDropDown, 
                           variables=variables,
                           formHTML=formHTML)




@app.route('/clinicalRequestSubmit', methods=['GET', 'POST'])
def clinicalRequestSubmit():
    if request.method == 'POST':
        return render_template('clinicalRequestSubmitted.html', trans=trans, shortcode=request.form['shortcode'])
    elif request.method == 'GET':
        return render_template('500.html', trans=trans)
    else:
        return render_template('500.html', trans=trans)
    

 
if __name__ == '__main__':
    app.run(debug=True, port=1111, host="0.0.0.0")
