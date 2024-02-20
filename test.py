# Small example program to test functionality in app.py

import os
import requests

# Create glossary
url = 'http://127.0.0.1:5000/glossary'
data = {"glossaryName":"Tech Acronyms",
         "sourceLang":"en-acronym",
         "targetLang":"en",
         "entries": "HTML\tHyperText Markup Language\nUSB\tUniversal Serial Bus\n"}
x = requests.post(url, json = data)
print(x.text + "\n")

# Add to pre-existing glossary
data = {"glossaryName":"Tech Acronyms",
         "entries": "IP\tInternet Protocol\n"}
x = requests.post(url, json = data)
print(x.text + "\n")

# Show example request data that should be posted to API
url = 'http://127.0.0.1:5000/postGlossary'
data = {"glossaryName":"Tech Acronyms"}
x = requests.get(url, data)
print(x.text + "\n")

os.remove("Tech Acronyms.dat")
os.remove("Tech Acronyms.tsv")