#!/usr/bin/python3

from odf import text, teletype
from odf.opendocument import load

templatePath = '/requests/templates/test doc 2.odt'
temporaryPath = '/requests/templates/patient1.odt'
#temporaryPath = '/requests/archieve/patient1.odt'

from bs4 import BeautifulSoup 

# Reading the data inside the xml file to a variable under the name  data
with open(templatePath, 'r') as f:
    data = f.read() 

# Passing the stored data inside the beautifulsoup parser 
bs_data = BeautifulSoup(data, 'xml') 

# Finding all instances of tag   
b_unique = bs_data.find_all('firstname') 
print(b_unique) 

# Using find() to extract attributes of the first instance of the tag 
b_name = bs_data.find('child', {'name':'Acer'}) 
print(b_name) 

# Extracting the data stored in a specific attribute of the `child` tag 
value = b_name.get('qty') 
print(value)