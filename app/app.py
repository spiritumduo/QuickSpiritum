#!/usr/bin/python3

# import flask module

from flask import Flask, request, render_template, redirect, url_for, session
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
lastSelectedLocation: str = 'Salisbury'

# instance of flask application
app = Flask(__name__)
app.secret_key = os.getenv('FLASK_KEY')
 

@app.route("/", methods=['GET', 'POST'])
def index():
    global lastSelectedLocation
    locationOptionsHTML: str = ''
    clinicalRequestTypes: str = ''
    clinicalRequestTypesHTML: str = ''

    #TODO: clear out session info before starting start page

    if 'locations' in request.form:
        if request.form['locations'] != lastSelectedLocation:
            lastSelectedLocation = request.form['locations']
    
    docxPtr = createPDF(TEMPLATE_DIR, PDF_DIR)


    locationOptionsHTML = locationOptionsHTMLF()
    
    clinicalRequestTypes = docxPtr.getTypes(lastSelectedLocation)
    preparedFormElements = formElements()

    

    for c in clinicalRequestTypes:
        clinicalRequestTypesHTML += preparedFormElements.wrapHTML('',f"""<div>
                    <input type="checkbox" class="inputLarge" name="{ c }" value="">
                <label for="{ c }">{ c }</label></div>""")
    
    return render_template('index.html', 
                           trans=trans, 
                           locationOptionsHTML=locationOptionsHTML,
                           clinicalRequestTypes=clinicalRequestTypes,
                           clinicalRequestTypesHTML=clinicalRequestTypesHTML)



@app.route("/clinicalRequesting", methods=['GET', 'POST'])
def clinicalRequesting():
    locationOptionsHTML:str = ''
    locationDropDown: str = ''
    placeholders: list[str] = []
    requestsChecked: list[str] = []
    #TODO: need to initiatise all local variables

    if request.method == 'POST':
        pass
    elif request.method == 'GET':
        return redirect(url_for('index'))
    else:
        return render_template('500.html', trans=trans)

    docxPtr = createPDF(TEMPLATE_DIR, PDF_DIR)
    #getLocations = docxPtr.getLocations()

    #print(session['clinicalRequests'])
    for r in session['clinicalRequests']:
        #print(r)
        if request.form.get(r) != None:
            requestsChecked.append(r)
            #print(f'{ r } was selected!')
        else:
            #print(f'{ r } was NOT selected!')
            pass
    
    placeholders.extend(docxPtr.getPlaceholders(lastSelectedLocation, requestsChecked))
    
    session['placeholders'] = placeholders
    session['requestsChecked'] = requestsChecked

    #TODO: likely need to add this to next page or index page after submission
    #session.pop('clinicalRequests')

    locationOptionsHTML = locationOptionsHTMLF()

    preparedFormElements = formElements()
    formHTML = preparedFormElements.createElements(placeholders)


    return render_template('clinicalRequesting.html', 
                           trans=trans,
                           requestsChecked=requestsChecked,
                           locationOptionsHTML=locationOptionsHTML,
                           locationDropDown=locationDropDown,
                           formHTML=formHTML)




@app.route('/clinicalRequestSubmit', methods=['GET', 'POST'])
def clinicalRequestSubmit():
    placeHoldersUpdated = []
    PDFPath: str = ''

    if request.method == 'POST':
        locationOptionsHTML:str = ''
        

        locationOptionsHTML = locationOptionsHTMLF()

        #print(session['placeholders'])
        preparedFormElements = formElements()
        placeHoldersUpdated = preparedFormElements.extractResults(session['placeholders'], request)

        
        #for r in placeHoldersUpdated:
        #    print(r)

        docxPtr = createPDF(TEMPLATE_DIR, PDF_DIR)

        for r in session['requestsChecked']:
            PDFPath = docxPtr.create(lastSelectedLocation, r, placeHoldersUpdated, "Smith, John, 1234567", '/requests/signatures/Mark Bailey.jpeg')
            #print(PDFPath)

        return render_template('clinicalRequestSubmitted.html', 
                                locationOptionsHTML=locationOptionsHTML,
                                trans=trans)
    
    elif request.method == 'GET':
        return render_template('500.html', 
                               trans=trans)
    
    else:
        return render_template('500.html', 
                               trans=trans)
    

def locationOptionsHTMLF():
    locationOptionsHTML: str = ''

    docxPtr = createPDF(TEMPLATE_DIR, PDF_DIR)
    getLocations = docxPtr.getLocations()

    if len(getLocations) == 0:
        raise Exception(f'No locations found in templates folder!')
        return

    session['clinicalRequests'] = docxPtr.getTypes(lastSelectedLocation)

    for location in getLocations:
        if location == lastSelectedLocation:
            locationOptionsHTML += f"""<option selected="selected" value="{ location }">{ location }</option>\n"""
        else:
            locationOptionsHTML += f"""<option value="{ location }">{ location }</option>\n"""
    
    return locationOptionsHTML


 
if __name__ == '__main__':
    app.run(debug=True, port=1111, host="0.0.0.0")
