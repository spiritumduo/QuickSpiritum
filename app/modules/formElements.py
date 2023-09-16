#!/usr/bin/python3

from datetime import date
import sys

sys.path.append('/requests/functions')
import constants as C

class formElements():
    def __init__(self) -> None:
        return
    
    def createElements(self, placeholders) -> str | None:
        formHTML: str = ''
        radioTitleHolder: str = ''
        radioTitleHolder: str = ''
        previousRadioSection: bool = False
        previousType: str = ''

        """ 
            [0] = full placeholder name
            [1] = return value, should be '' for now
            [2] = name of placeholder - first element of pipe separated string
            [3] = type of variable
            [4] = value of radio or checkbox
        """
        for placeholder in placeholders:
            #print(placeholder[0])
            PFull: str = placeholder[0]
            P2: str = placeholder[2].strip() #TODO: check if removing strip works, as now strip in createPDF.py getPlaceholders function
            p2: str = placeholder[2].lower()



            if p2 == 'line':
                formHTML += self.wrapHTML()

            elif p2 == 'signature':
                formHTML += self.wrapHTML(f'<label for="{ PFull }">Signature</label>', \
                                f'<input type="text" class="inputLarge" name="{ PFull }" value="">')
                
            elif p2 == 'configuration':
                None
                #print(f'{ placeholder[2] } holds configuration information')

            elif p2 == 'now':
                None
                #print(f'{ placeholder[2] } is to show today\'s date - {date.today().strftime("%d/%m/%Y") }')

            elif p2 == 'title':
                P3 = placeholder[3].strip() #TODO: check if removing strip works, as now strip in createPDF.py getPlaceholders function
                formHTML += self.wrapHTML()
                formHTML += self.wrapHTML('', f"""<div class="radioTitle">{ P3 }</div> \
                                          <input type="hidden" name="{ PFull }" value="">""")
                
            else:
                # If only one variable in placeholder, then this will default to a string.
                # NB: a single variable placeholder has its whole name, its return value and its name again
                # and hence length of 3 below.
                if len(placeholder) == 3:
                    formHTML += self.wrapHTML(f'<label for="{ PFull }">{ P2 }</label>', \
                                f'<input type="text" class="inputLarge" name="{ PFull }" value="">')
                if len(placeholder) >= 4:
                    p3 = placeholder[3].lower().strip()

                    if p3 == 'integer':
                        formHTML += self.wrapHTML(f'<label for="{ PFull }">{ P2 }</label>', \
                                f'<input type="number" class="inputLarge" name="{ PFull }" value="">')
                    elif p3 == 'date':
                        None
                        #print(f'{ placeholder[2] } is an date')
                    elif p3 == 'radio':
                        if len(placeholder) < 5:
                            raise Exception(f'Missing argument for radio button!')
                            return None
                        

                        if radioTitleHolder == '' or radioTitleHolder != P2:
                            radioTitleHolder = P2
                            formHTML += self.wrapHTML('', f'<div class="radioTitle">{ P2 }</div>')
                            previousRadioSection = True
                        elif radioTitleHolder == P2:
                            pass
                        else:
                            radioTitleHolder = ''

                        P4 = placeholder[4].strip()

                        formHTML += self.wrapHTML('', \
                f"""<div>
                        <input type="radio" class="inputLarge" name="{ PFull }" value="">
                        <label for="{ PFull }">{ P4 }</label>
                    </div>""")
                        
                    elif p3 == 'checkbox':
                        formHTML += self.wrapHTML('', f"""<div>
                    <input type="checkbox" class="inputLarge" name="{ PFull }" value="">
                <label for="{ PFull }">{ P2 }</label></div>""")
                        
                    else:
                        None
                        """raise Exception(f'placeholder type (e.g. radio, string, integer) is incorrect!')
                        return None"""
        return formHTML
    
    def wrapHTML(self, LItem: str ='', RItem: str = '') -> str:
        wrappedHTML: str = f"""        <div class='row'>
            <div class='columnL'>
                { LItem }
            </div>
            <div class='columnR'>
                { RItem }
            </div>
        </div>\n"""

        return wrappedHTML

    def extractResults(self, pHolders, request):

        #TODO: verify the above arguments

        for x in range(len(pHolders)):
            if len(pHolders[x]) == 3:
                pHolders[x][1] = request.form.get(pHolders[x][0])
            if len(pHolders[x]) >= 4:
                if any([y in pHolders[x][3] for y in ['radio', 'checkbox']]):
                    if request.form.get(pHolders[x][0]) != None:
                        pHolders[x][1] = C.CHECKED
                    else:
                        pHolders[x][1] = C.UNCHECKED
                
                else:
                    pHolders[x][1] = request.form.get(pHolders[x][0])
                    #print(f'{ requestS} - { request.form.get(requestS[0]) }')



        return pHolders