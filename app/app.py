#!/usr/bin/python3

""" Web app to collect patient information for creating PDFs of request forms

"""

from flask import Flask, request, render_template, redirect, url_for, session
import sys
import os
sys.path.append('/requests/functions')
from create_pdf import CreatePDF
sys.path.append('/app/modules')
from formElements import formElements

#TODO: need to have a data cleanser that fixes illegal characters in the placeholders received from the docx file (eg ' and ")

import constants as C

trans = {'yes':'qui', 'no':'noi', 'portal': 'portal'}
users = [
    ["mark.bailey", "Mark Bailey"],
    ["john.williams" , "John Williams"]
]

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
    try:
        session.pop('placeholders')
        session.pop('requestsChecked')
    except:
        pass

    if 'locations' in request.form:
        if request.form['locations'] != lastSelectedLocation:
            lastSelectedLocation = request.form['locations']
    
    docxPtr = CreatePDF(C.TEMPLATE_DIR, C.PDF_DIR)


    locationOptionsHTML = locationOptionsHTMLF()
    
    clinicalRequestTypes = docxPtr.get_types(lastSelectedLocation)
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

    docxPtr = CreatePDF(C.TEMPLATE_DIR, C.PDF_DIR)
    #get_locations = docxPtr.get_locations()

    #print(session['clinicalRequests'])
    for r in session['clinicalRequests']:
        #print(r)
        if request.form.get(r) != None:
            requestsChecked.append(r)
            #print(f'{ r } was selected!')
        else:
            #print(f'{ r } was NOT selected!')
            pass
    
    placeholders.extend(docxPtr.get_placeholders(lastSelectedLocation, requestsChecked))
    
    session['placeholders'] = placeholders
    session['requestsChecked'] = requestsChecked

    locationOptionsHTML = locationOptionsHTMLF()

    preparedFormElements = formElements()
    formHTML = preparedFormElements.createElements(placeholders, users, 0)


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
    demographicsForPDF: str = ''
    firstname:str = ''
    lastname:str = ''
    hospitalID:str = ''

    if request.method == 'POST':
        locationOptionsHTML:str = ''
        

        locationOptionsHTML = locationOptionsHTMLF()

        #print(session['placeholders'])
        preparedFormElements = formElements()
        placeHoldersUpdated = preparedFormElements.extractResults(session['placeholders'], request)

        
        #for r in placeHoldersUpdated:
        #    print(r)


        for index, item in enumerate(placeHoldersUpdated):
            if item[2].lower() == "hospital id":
                hospitalID = item[1]
            elif item[2].lower() == "first name":
                firstname = item[1]
            elif item[2].lower() == "last name":
                lastname = item[1]
        
        demographicsForPDF = f'{ lastname }_{ firstname }_{ hospitalID }'

        docxPtr = CreatePDF(C.TEMPLATE_DIR, C.PDF_DIR)

        placeHoldersUpdated['signature|picture'] = '/requests/signatures/Mark Bailey.jpeg'
        
        for r in session['requestsChecked']:
            PDFPath = docxPtr.create(lastSelectedLocation, r, placeHoldersUpdated, demographicsForPDF)

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

    docxPtr = CreatePDF(C.TEMPLATE_DIR, C.PDF_DIR)
    get_locations = docxPtr.get_locations()

    if len(get_locations) == 0:
        raise Exception(f'No locations found in templates folder!')
        return

    session['clinicalRequests'] = docxPtr.get_types(lastSelectedLocation)

    for location in get_locations:
        if location == lastSelectedLocation:
            locationOptionsHTML += f"""<option selected="selected" value="{ location }">{ location }</option>\n"""
        else:
            locationOptionsHTML += f"""<option value="{ location }">{ location }</option>\n"""
    
    return locationOptionsHTML


 
if __name__ == '__main__':
    app.run(debug=True, port=1111, host="0.0.0.0")
